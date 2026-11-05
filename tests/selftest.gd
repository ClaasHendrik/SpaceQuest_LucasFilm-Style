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
	await m.act("Wear", "item", "uniform")
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
	await m.act("Wear", "item", "wire")
	check(not m.busy, "wearing a non-wearable item completes")

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
			if rc[0] < 0 or rc[1] < 0 or rc[0] + rc[2] > 320 or rc[1] + rc[3] > 132:
				bad_rects += 1
	check(bad_exits == 0, "every exit leads to an existing room")
	check(bad_rects == 0, "every hotspot lies inside the 320x132 stage")
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
		if t == null or t.get_width() != 320 or t.get_height() != 132:
			missing_art += 1
			print("   bad art for ", rid)
		var inside: bool = m.room.no_player or Geometry2D.is_point_in_polygon(m.player.position, m.room.walk_poly)
		if not inside:
			print("   entry outside walk area: ", rid)
			missing_art += 1
	check(missing_art == 0, "every room loads 320x132 art and starts Roger on walkable ground")

	print("--- space travel")
	m._on_restart()
	m.change_room("nav_screen", "start")
	for i in 2:
		await m.act("Use", "hotspot", "course")
	check(int(GameState.flag("course_index")) == 2, "set course twice selects Ortega")
	m.change_room("cockpit", "start")
	await m.act("Use", "hotspot", "launch")
	check(m.room.id == "ortega_crater", "launch lever flies to the chosen planet")

	print("RESULT: ", "PASS" if failures.is_empty() else "FAIL (%d)" % failures.size())
	m.get_tree().quit(0 if failures.is_empty() else 1)
