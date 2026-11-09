extends RefCounted
# Animation check: SHOT_DIR=/dir xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x960 -- --shot-anim


func _save(m, name: String) -> void:
	await m.get_tree().process_frame
	await m.get_tree().process_frame
	var dir := OS.get_environment("SHOT_DIR") if OS.has_environment("SHOT_DIR") else "user://"
	m.get_viewport().get_texture().get_image().save_png("%s/anim_%s.png" % [dir, name])


func run(m) -> void:
	m.fast = true
	await m.get_tree().create_timer(0.3).timeout
	GameState.reset()
	m.change_room("crash_site", "start")
	m.player.position = Vector2(300, 270)
	m.player.face("front")
	await _save(m, "front")
	m.player.face("back")
	await _save(m, "back")
	m.player.face("side")
	m.player.action = 1
	m.player.queue_redraw()
	await _save(m, "crouch")
	m.player.action = -1
	m.change_room("dark_room", "chute")
	m.room.t_anim = 0.5
	m.room.queue_redraw()
	await _save(m, "rats")
	m.change_room("conveyor", "start")
	m.room.t_anim = 0.0
	m.room.queue_redraw()
	await _save(m, "belt0")
	m.room.t_anim = 0.3
	m.room.queue_redraw()
	await _save(m, "belt1")
	m.change_room("dark_room", "chute")
	m.room.t_anim = 1.55
	m.room.queue_redraw()
	await _save(m, "rats_b")
	m.get_tree().quit()
