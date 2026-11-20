extends RefCounted
# Records the main animations in the real engine, one after the other, printing "CLIP name frame" marks.
#   xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 640x480 --write-movie out.avi --fixed-fps 30 -- --clips


func _mark(m, name: String) -> void:
	print("CLIP ", name, " ", Engine.get_frames_drawn())


func _wait(m, s: float) -> void:
	await m.get_tree().create_timer(s).timeout


func run(m) -> void:
	m.fast = false
	await _wait(m, 0.5)
	GameState.reset()
	m.message.visible = false

	_mark(m, "walk")
	m.change_room("crash_site", "start")
	await _wait(m, 0.4)
	await m.walk_to(Vector2(520, 300))
	await m.walk_to(Vector2(520, 380))
	await m.walk_to(Vector2(140, 380))
	await m.walk_to(Vector2(140, 270))
	await _wait(m, 0.3)

	_mark(m, "pickup")
	await m.player.reach()
	await _wait(m, 0.5)

	_mark(m, "talk")
	m.player.face("front")
	m.say("\"Well, that could have gone worse. I think.\"")
	await _wait(m, 2.6)
	m.player.face("side")
	await _wait(m, 0.3)

	_mark(m, "climb")
	m.change_room("yard_ladder", "eye")
	await _wait(m, 0.3)
	m.player.position = Vector2(404, 250)
	m.player.face("back")
	await m.room._open_hatch(m, null)
	await _wait(m, 0.3)

	_mark(m, "fall")
	m.change_room("rail_west", "jump")
	await _wait(m, 0.5)
	await m.player.fall(260.0)
	await _wait(m, 0.4)
	m.player.mode = ""

	_mark(m, "shredder")
	m.change_room("conveyor", "start")
	await _wait(m, 0.3)
	m.player.position = Vector2(110, 262)
	m.player.face("side")
	for i in 26:
		m.room.shred = i / 26.0
		await _wait(m, 0.2)
	m.room.shred = 1.0
	await m.walk_to(Vector2(356.0, 262.0))
	m.player.visible = false
	await _wait(m, 1.0)

	_mark(m, "rat")
	m.change_room("wire_tube", "start")
	await _wait(m, 0.6)
	await m.room._rat_run(m, 228.0, 700.0, -60.0, 1.1)
	await _wait(m, 0.4)
	m.change_room("dark_room", "chute")
	await _wait(m, 0.5)
	await m.room._rat_run(m, m.player.position.y, 640.0, m.player.position.x + 26.0, 1.2)
	await _wait(m, 0.8)
	_mark(m, "end")
	m.get_tree().quit()
