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

	print("--- escape pod puzzle")
	m.change_room("escape_pod", "start")
	check(m.room.id == "escape_pod", "starts in the escape pod")
	await m.act("Open", "hotspot", "locker")
	check(GameState.flag("locker_open"), "locker opens")
	await m.act("Pick up", "hotspot", "uniform")
	check(GameState.has_item("uniform"), "uniform in inventory")
	await m.act("Use", "item", "uniform")
	check(GameState.flag("wearing_uniform") and not GameState.has_item("uniform"), "uniform worn")
	await m.act("Open", "hotspot", "hatch")
	check(m.room.id == "garbage_mountain", "hatch leads to the garbage mountain")

	print("--- scoring")
	await m.act("Pick up", "hotspot", "wire")
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
	check(GameState.score == 5 and GameState.has_item("wire") and GameState.current_room == "garbage_mountain", "state restored")

	print("--- two-step verb")
	await m.act("Use", "item", "wire", "hotspot", "heap")
	check(not m.busy, "use item on hotspot completes")
	await m.act("What is", "item", "wire")
	check(not m.busy, "What is on an item completes")

	print("--- death")
	m._on_restart()
	check(GameState.score == 0 and GameState.inventory.is_empty(), "restart resets state")
	m.act("Open", "hotspot", "hatch")  # not awaited: die() never returns
	await m.get_tree().create_timer(0.5).timeout
	check(m.dead and m.overlay != null, "walking out in underwear is fatal and shows the death screen")
	m._on_restart()
	check(not m.dead and m.overlay == null, "restart leaves the death screen")

	print("--- world")
	var f := FileAccess.open("res://data/rooms.json", FileAccess.READ)
	var data: Array = JSON.parse_string(f.get_as_text())
	var ids := {"escape_pod": true, "garbage_mountain": true}
	for r in data:
		ids[r["id"]] = true
	check(m.room_ids.size() == ids.size(), "room list covers all %d rooms" % ids.size())
	var graph := {"escape_pod": ["garbage_mountain"], "garbage_mountain": ["escape_pod", "robot_head", "conveyor"]}
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
			if rc[0] < 0 or rc[1] < 0 or rc[0] + rc[2] > 320 or rc[1] + rc[3] > 144:
				bad_rects += 1
	check(bad_exits == 0, "every exit leads to an existing room")
	check(bad_rects == 0, "every hotspot lies inside the 320x144 stage")
	for d in ["landing_strip", "monolith_exterior", "ortega_crater", "pestulon_exterior"]:
		graph["cockpit"].append(d)   # reached through the navigation computer and launch lever
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
		if t == null or t.get_width() != 320 or t.get_height() != 144:
			missing_art += 1
			print("   bad art for ", rid)
		var inside: bool = m.room.no_player or Geometry2D.is_point_in_polygon(m.player.position, m.room.walk_poly)
		if not inside:
			print("   entry outside walk area: ", rid)
			missing_art += 1
	check(missing_art == 0, "every room loads 320x144 art and starts Roger on walkable ground")

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
	print("--- Act 1 playthrough")
	m._on_restart()
	var seq := func(room_id: String): check(m.room.id == room_id, "now in " + room_id)
	# the escape pod: no uniform, no future
	await m.act("Open", "hotspot", "locker")
	await m.act("Pick up", "hotspot", "uniform")
	await m.act("Use", "item", "uniform")
	await m.act("Open", "hotspot", "hatch")
	seq.call("garbage_mountain")
	await m.act("Pick up", "hotspot", "wire")
	# the robot head: through the broken eye
	await m.act("Walk to", "hotspot", "east")
	seq.call("robot_head")
	await m.act("Use", "hotspot", "eye")
	check(GameState.flag("saw_panel"), "the robot eye shows the Mallard's open panel")
	await m.act("Walk to", "hotspot", "w")
	await m.act("Walk to", "hotspot", "south")
	seq.call("conveyor")
	# the trash bucket takes Roger up to the rail
	await m.act("Use", "hotspot", "bucket")
	seq.call("rail_walk")
	# on the rail: jump, ride the grabber, lift the motivator from the pedestal and drop it in the ship's panel
	await m.act("Use", "hotspot", "grabber")
	check(not m.room.riding, "can't ride the grabber from the floor")
	await m.act("Use", "hotspot", "rail")
	check(GameState.flag("on_rail"), "Roger is up on the rail")
	await m.act("Use", "hotspot", "grabber")
	check(m.room.riding, "Roger rides the grabber")
	m.room.set_grabber(38.0)
	await m.act("Push", "hotspot", "grabber")
	check(GameState.flag("motivator_held"), "the claw takes the warp motivator")
	m.room.set_grabber(283.0)
	await m.act("Push", "hotspot", "grabber")
	check(GameState.flag("motivator_installed"), "the motivator is set into the ship's panel")
	await m.act("Use", "hotspot", "grabber")
	await m.act("Use", "hotspot", "chute")
	seq.call("rat_lair")
	# the reactor cavern: take the ladder, climb to the crane
	await m.act("Pick up", "hotspot", "portable")
	check(GameState.has_item("ladder"), "the portable ladder is in the inventory")
	await m.act("Use", "hotspot", "ladder")
	seq.call("crane_cabin")
	# the crane: over the pit, grab the reactor, over the bay, drop it
	await m.act("Push", "hotspot", "stick")
	await m.act("Push", "hotspot", "button")
	check(GameState.flag("crane_holding"), "the claw holds the reactor")
	await m.act("Push", "hotspot", "stick")
	await m.act("Push", "hotspot", "button")
	check(GameState.flag("reactor_delivered"), "the reactor is delivered to the bay")
	await m.act("Walk to", "hotspot", "hatch")
	seq.call("mallard_bay")
	await m.act("Open", "hotspot", "ramp")
	check(m.room.id == "mallard_bay", "the ramp stays up while the ship has no power")
	await m.act("Pick up", "hotspot", "reactor")
	check(GameState.has_item("reactor"), "Roger picks up the reactor")
	await m.act("Use", "item", "ladder", "hotspot", "ship")
	check(GameState.flag("ladder_placed"), "the ladder is propped against the hull")
	await m.act("Open", "hotspot", "tophatch")
	await m.act("Use", "item", "reactor", "hotspot", "panel")
	await m.act("Use", "item", "wire", "hotspot", "panel")
	await m.act("Open", "hotspot", "ramp")
	seq.call("cockpit")
	# the cockpit: buckazoids in the cushion, then power-up and the escape
	await m.act("Use", "hotspot", "seat")
	check(GameState.has_item("buckazoids"), "buckazoids found in the pilot's seat")
	for f in ["sys_engines", "sys_radar", "sys_weapons", "sys_front"]:
		GameState.set_flag(f)
	m.room._takeoff(m)
	m.room._fire(m)
	await m.get_tree().create_timer(0.2).timeout
	check(GameState.flag("escaped_freighter"), "the Mallard blasts out of the freighter")
	check(GameState.score == 145, "Act 1 is worth exactly 145 points (score %d)" % GameState.score)
	# deaths on the way
	m._on_restart()
	m.change_room("robot_head", "start")
	m.act("Walk to", "hotspot", "chasm")
	await m.get_tree().create_timer(0.4).timeout
	check(m.dead, "walking into the chasm kills Roger")
	m._on_restart()
	m.change_room("cockpit", "start")
	for f in ["sys_engines", "sys_weapons"]:
		GameState.set_flag(f)
	m.room._takeoff(m)
	await m.get_tree().create_timer(0.2).timeout
	check(m.dead, "taking off without radar kills Roger")
	m._on_restart()
