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

	print("RESULT: ", "PASS" if failures.is_empty() else "FAIL (%d)" % failures.size())
	m.get_tree().quit(0 if failures.is_empty() else 1)
