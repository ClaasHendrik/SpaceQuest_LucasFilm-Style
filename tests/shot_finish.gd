extends RefCounted
# States and cutscene: SHOT_DIR=/dir xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x960 -- --shot-finish


func _save(m, name: String) -> void:
	await m.get_tree().process_frame
	await m.get_tree().process_frame
	var dir := OS.get_environment("SHOT_DIR") if OS.has_environment("SHOT_DIR") else "user://"
	m.get_viewport().get_texture().get_image().save_png("%s/fin_%s.png" % [dir, name])


func run(m) -> void:
	m.fast = true
	await m.get_tree().create_timer(0.3).timeout
	GameState.reset()
	m.change_room("tube_entrance", "west")
	await _save(m, "ladder")
	GameState.set_flag("ladder_taken")
	GameState.set_flag("wire_taken")
	m.change_room("wire_tube", "west")
	await _save(m, "tube_nowire")
	GameState.set_flag("motivator_installed")
	GameState.set_flag("ladder_placed")
	m.change_room("yard_ladder", "eye")
	await _save(m, "yard_installed")
	m.fast = false
	m.play_cutscene([["cut_blast", 5.0, "The lasers punch a doorway through the freighter, and the Mallard follows them out."]])
	await m.get_tree().create_timer(0.4).timeout
	await _save(m, "cutscene")
	m.fast = true
	await m.get_tree().create_timer(0.7).timeout
	m._close_overlay()
	GameState.set_flag("sys_engines")
	GameState.set_flag("sys_radar")
	m.change_room("cockpit", "start")
	m.room._menu(m)
	await _save(m, "flight")
	GameState.set_flag("sys_weapons")
	m.room._wall_menu(m)
	await _save(m, "weapons")
	m.get_tree().quit()
