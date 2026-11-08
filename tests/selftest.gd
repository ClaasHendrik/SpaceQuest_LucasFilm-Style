extends RefCounted
# Headless self-test: godot --headless --path . -- --selftest
# Drives the real game logic through the same entry points the UI uses.

var failures: Array = []


func check(cond: bool, msg: String) -> void:
	if cond:
		print("  ok   ", msg)
	else:
		print("  FAIL ", msg)
		failures.append(msg)


func run(m) -> void:
	m.fast = true
	GameState.reset()
	GameState.set_flag("x")  # touch API
	GameState.flags = {}
	print("--- data")
	check(GameState.max_score == 738, "point list sums to 738 (got %d)" % GameState.max_score)
	check(GameState.points.size() == 40, "40 score events")

	print("--- escape pod")
	m.change_room("escape_pod", "start")
	check(m.room.id == "escape_pod", "starts in the escape pod")
	await m.act("Open", "hotspot", "locker")
	check(GameState.flag("locker_open"), "locker opens")
	await m.act("Pick up", "hotspot", "manual")
	check(GameState.has_item("manual"), "pod manual in inventory")
	await m.act("Look at", "item", "manual")
	check(not m.busy, "reading the manual completes")
	await m.act("Open", "hotspot", "hatch")
	check(m.room.id == "crash_site", "hatch leads to the crash site")

	print("--- scoring")
	m.change_room("wire_tube", "west")
	await m.act("Pick up", "hotspot", "wires")
	check(GameState.has_item("wire"), "wire picked up")
	check(GameState.score == 5, "wire awards 5 points (score %d)" % GameState.score)
	m.award("wire")
	check(GameState.score == 5, "no double award")
	check(GameState.add_score("not_an_event") == 0, "unknown event gives 0")

	print("--- save / restore")
	GameState.player_pos = m.player.position
	check(GameState.save_slot("selftest"), "save works")
	GameState.score = 999
	GameState.inventory = []
	check(GameState.load_slot("selftest"), "load works")
	check(GameState.score == 5 and GameState.has_item("wire") and GameState.current_room == "wire_tube", "state restored")

	print("--- two-step verb")
	await m.act("Use", "item", "wire", "hotspot", "w")
	check(not m.busy, "use item on hotspot completes")
	await m.act("What is", "item", "wire")
	check(not m.busy, "What is on an item completes")

	print("--- death")
	m._on_restart()
	check(GameState.score == 0 and GameState.inventory.is_empty(), "restart resets state")
	m.change_room("robot_head", "start")
	m.act("Walk to", "hotspot", "chasm")  # not awaited: die() never returns
	await m.get_tree().create_timer(0.5).timeout
	check(m.dead and m.overlay != null, "the chasm is fatal and shows the death screen")
	m._on_restart()
	check(not m.dead and m.overlay == null, "restart leaves the death screen")

	print("--- world")
	var data: Array = []
	for path in ["res://data/rooms.json", "res://data/act1_rooms.json"]:
		var f := FileAccess.open(path, FileAccess.READ)
		data.append_array(JSON.parse_string(f.get_as_text()))
	var ids := {"escape_pod": true}
	for r in data:
		ids[r["id"]] = true
	check(m.room_ids.size() == ids.size(), "room list covers all %d rooms" % ids.size())
	var graph := {"escape_pod": ["crash_site"]}
	var bad_exits := 0
	var bad_rects := 0
	for r in data:
		graph[r["id"]] = []
		for h in r["hotspots"]:
			if h.has("exit"):
				graph[r["id"]].append(h["exit"]["room"])
				if not ids.has(h["exit"]["room"]):
					bad_exits += 1
			var rc: Array = h["rect"]
			if rc[0] < 0 or rc[1] < 0 or rc[0] + rc[2] > 320 or rc[1] + rc[3] > 160:
				bad_rects += 1
	check(bad_exits == 0, "every exit leads to an existing room")
	check(bad_rects == 0, "every hotspot lies inside the 320x160 stage")
	# links made by the Act 1 scripts rather than by data exits
	graph["robot_head"].append("yard")
	graph["junk_tower"].append("conveyor")
	graph["conveyor"].append("rail_west")
	graph["rail_tower"].append("yard")
	graph["yard"].append("rail_west")
	graph["rail_west"].append("dark_room")
	graph["yard_ladder"].append("cockpit")
	graph["cockpit"].append("nav_screen")
	for d in ["landing_strip", "monolith_exterior", "ortega_crater", "pestulon_exterior"]:
		graph["cockpit"].append(d)   # reached through the navigation computer and launch lever
	graph["yard"].append("yard_ladder")
	var seen := {"escape_pod": true}
	var queue := ["escape_pod"]
	while not queue.is_empty():
		var cur: String = queue.pop_front()
		for nxt in graph.get(cur, []):
			if not seen.has(nxt):
				seen[nxt] = true
				queue.append(nxt)
	# only the cockpit shortcut links the ship to later acts; everything must be reachable from the start
	var unreachable: Array = []
	for rid in ids:
		if not seen.has(rid):
			unreachable.append(rid)
	check(unreachable.is_empty(), "every room is reachable from the start (unreachable: %s)" % str(unreachable))
	var missing_art := 0
	for rid in m.room_ids:
		m.change_room(rid, "start")
		var t = m.room.Art.tex("res://assets/backgrounds/%s.png" % m.room.current_bg())
		if t == null or t.get_width() != 320 or (t.get_height() != 144 and t.get_height() != 160):
			missing_art += 1
			print("   bad art for ", rid)
		var inside: bool = m.room.no_player or Geometry2D.is_point_in_polygon(m.player.position, m.room.walk_poly)
		if not inside:
			print("   entry outside walk area: ", rid)
			missing_art += 1
	check(missing_art == 0, "every room loads 320x144 or 320x160 art and starts Roger on walkable ground")

	print("--- interface")
	m.change_room("escape_pod", "start")
	check(not m.verb_enabled("Talk to") and not m.verb_enabled("Travel"), "Talk to and Travel are greyed out in the escape pod")
	check(m.verb_buttons["Talk to"].disabled, "the greyed verb buttons are disabled")
	m.change_room("cockpit", "start")
	check(m.verb_enabled("Travel"), "Travel is active in the cockpit")
	check(not m.verb_buttons["Travel"].disabled, "the Travel button is enabled there")

	print("--- space travel")
	m._on_restart()
	m.change_room("nav_screen", "start")
	for i in 2:
		await m.act("Use", "hotspot", "course")
	check(int(GameState.flag("course_index")) == 2, "set course twice selects Ortega")
	m.change_room("cockpit", "start")
	await m.act("Use", "hotspot", "launch")
	check(m.room.id == "cockpit", "the launch lever does nothing before the freighter escape")
	GameState.set_flag("escaped_freighter")
	await m.act("Use", "hotspot", "launch")
	check(m.room.id == "ortega_crater", "launch lever flies to the chosen planet after the escape")

	await _act1(m)

	print("RESULT: ", "PASS" if failures.is_empty() else "FAIL (%d)" % failures.size())
	m.get_tree().quit(0 if failures.is_empty() else 1)


# ---------------------------------------------------------------------------- Act 1, start to finish
func _act1(m) -> void:
	print("--- Act 1 playthrough (original layout)")
	m._on_restart()
	var at := func(room_id: String): check(m.room.id == room_id, "now in " + room_id)
	# the pod: the manual, then out through the hatch
	await m.act("Open", "hotspot", "locker")
	await m.act("Pick up", "hotspot", "manual")
	await m.act("Open", "hotspot", "hatch")
	at.call("crash_site")
	# east, into the tube: the wire
	await m.act("Walk to", "hotspot", "e")
	at.call("tube_entrance")
	await m.act("Open", "hotspot", "arches")
	at.call("wire_tube")
	await m.act("Pick up", "hotspot", "wires")
	check(GameState.has_item("wire"), "wire taken in the tube")
	# robot head: through the eye, see the shuttle, and back down
	await m.act("Walk to", "hotspot", "e")
	at.call("robot_head")
	await m.act("Use", "hotspot", "eye")
	at.call("yard")
	check(GameState.flag("eye_done"), "the eye leads up to the shuttle")
	await m.act("Walk to", "hotspot", "ladder")
	at.call("robot_head")
	# back to the pod place, south and east to the lift
	await m.act("Walk to", "hotspot", "w")
	await m.act("Walk to", "hotspot", "w")
	await m.act("Walk to", "hotspot", "w")
	at.call("crash_site")
	await m.act("Walk to", "hotspot", "s")
	at.call("junk_field")
	await m.act("Walk to", "hotspot", "e")
	at.call("junk_tower")
	await m.act("Use", "hotspot", "lift")
	at.call("conveyor")
	await m.act("Use", "hotspot", "rail")
	at.call("rail_west")
	await m.act("Walk to", "hotspot", "w")
	at.call("rail_window")
	await m.act("Walk to", "hotspot", "w")
	at.call("rail_tower")
	# the grabber: the claw over the yard
	await m.act("Use", "hotspot", "grabber")
	at.call("yard")
	check(m.room.riding, "Roger rides the grabber")
	m.room.claw_x = 52.0
	await m.act("Push", "hotspot", "motivator")
	check(GameState.flag("motivator_held"), "the claw takes the warp motivator")
	m.room.claw_x = 130.0
	await m.act("Push", "hotspot", "panel")
	check(GameState.flag("motivator_installed"), "the motivator is set into the open panel")
	await m.act("Walk to", "hotspot", "platform")
	at.call("rail_west")
	await m.act("Use", "hotspot", "chute")
	at.call("dark_room")
	await m.act("Pick up", "hotspot", "reactor")
	check(GameState.has_item("reactor"), "the reactor is taken from the hole")
	await m.act("Open", "hotspot", "ladder")
	at.call("tube_entrance")
	# the rat takes the reactor and the wire in the tube
	await m.act("Open", "hotspot", "arches")
	at.call("wire_tube")
	await m.get_tree().create_timer(0.3).timeout
	check(not GameState.has_item("reactor") and not GameState.has_item("wire"), "the rat steals the reactor and the wire")
	# fetch them again
	await m.act("Walk to", "hotspot", "w")
	await m.act("Open", "hotspot", "e")
	at.call("dark_room")
	await m.act("Pick up", "hotspot", "reactor")
	check(GameState.has_item("reactor") and GameState.has_item("wire"), "reactor and wire are back in hand")
	await m.act("Open", "hotspot", "ladder")
	await m.act("Pick up", "hotspot", "ladder")
	check(GameState.has_item("ladder"), "the ladder at the tube entrance")
	await m.act("Open", "hotspot", "arches")
	await m.act("Walk to", "hotspot", "e")
	at.call("robot_head")
	await m.act("Use", "hotspot", "eye")
	at.call("yard")
	await m.act("Use", "item", "ladder", "hotspot", "ship")
	at.call("yard_ladder")
	await m.act("Open", "hotspot", "hatch")
	await m.act("Use", "item", "reactor", "hotspot", "panel")
	await m.act("Use", "item", "wire", "hotspot", "panel")
	await m.act("Open", "hotspot", "to_cockpit")
	at.call("cockpit")
	await m.act("Use", "hotspot", "seat")
	check(GameState.has_item("buckazoids"), "buckazoids found in the pilot's seat")
	for f in ["sys_engines", "sys_radar", "sys_weapons", "sys_front"]:
		GameState.set_flag(f)
	m.room._takeoff(m)
	m.room._fire(m)
	await m.get_tree().create_timer(0.2).timeout
	check(GameState.flag("escaped_freighter"), "the Mallard blasts out of the freighter")
	check(GameState.score == 145, "Act 1 is worth exactly 145 points (score %d)" % GameState.score)
	# deaths
	m._on_restart()
	m.change_room("robot_head", "west")
	m.act("Walk to", "hotspot", "chasm")
	await m.get_tree().create_timer(0.4).timeout
	check(m.dead, "walking into the chasm kills Roger")
	m._on_restart()
	m.change_room("cockpit", "start")
	for f in ["sys_engines", "sys_weapons", "motivator_installed", "reactor_installed", "wire_installed"]:
		GameState.set_flag(f)
	m.room._takeoff(m)
	await m.get_tree().create_timer(0.2).timeout
	check(m.dead, "taking off without radar kills Roger")
	m._on_restart()
