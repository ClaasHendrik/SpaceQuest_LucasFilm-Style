extends RefCounted
# Act 1 screens:  SHOT_DIR=/dir xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x960 -- --shot-act1


func _save(m, name: String) -> void:
	await m.get_tree().process_frame
	await m.get_tree().process_frame
	var dir := OS.get_environment("SHOT_DIR") if OS.has_environment("SHOT_DIR") else "user://"
	m.get_viewport().get_texture().get_image().save_png("%s/a1_%s.png" % [dir, name])
	print("saved ", name)


func _talk(m, text: String) -> void:
	m.message.text = text
	m.message.visible = true


func run(m) -> void:
	m.fast = true
	await m.get_tree().create_timer(0.3).timeout
	GameState.reset()
	# 0. the pod, with the locker open
	m.change_room("escape_pod", "start")
	await m.act("Open", "hotspot", "locker")
	m.message.visible = false
	m.verb = "Pick up"
	m._update_sentence("pod manual")
	await _save(m, "0_pod")
	# 1. the conveyor, with the crusher's warning
	m.change_room("conveyor", "start")
	_talk(m, "Somewhere above you, the crusher clears its throat. It has an appointment, and you are in it.")
	m.verb = "Use"
	m._update_sentence("trash bucket")
	await _save(m, "1_conveyor")
	# 2. on the rail, riding the grabber to the pedestal
	m.message.visible = false
	m.verb = "Walk to"
	m.change_room("rail_walk", "start")
	await m.act("Use", "hotspot", "rail")
	await m.act("Use", "hotspot", "grabber")
	m.room.set_grabber(38.0)
	m.message.visible = false
	m._update_sentence("grabber")
	await _save(m, "2_rail_ride")
	await m.act("Push", "hotspot", "grabber")
	m.room.set_grabber(283.0)
	_talk(m, "The claw lowers the motivator into the open panel. It seats with a satisfying clunk.")
	await _save(m, "3_motivator_installed")
	# 4. reactor cavern with the ladder, rat warning
	m.message.visible = false
	GameState.set_flag("on_rail", false)
	m.change_room("rat_lair", "pipe")
	_talk(m, "The breathing has stopped. That's worse.")
	m.verb = "Pick up"
	m._update_sentence("ladder")
	await _save(m, "4_rat_lair")
	# 5. the crane, with the reticle over the pit
	m.message.visible = false
	m.change_room("crane_cabin", "start")
	GameState.set_flag("crane_pos", 1)
	GameState.set_flag("crane_holding", true)
	m.room.queue_redraw()
	m.verb = "Push"
	m._update_sentence("red button")
	await _save(m, "5_crane")
	# 6. the bay with ladder and reactor
	GameState.set_flag("crane_holding", false)
	GameState.set_flag("reactor_delivered")
	GameState.set_flag("ladder_placed")
	m.change_room("mallard_bay", "start")
	m.verb = "Pick up"
	m._update_sentence("reactor")
	await _save(m, "6_bay")
	# 7. the ship's computer
	GameState.set_flag("sys_engines")
	m.change_room("cockpit", "start")
	m.room._menu(m)
	await _save(m, "7_computer")
	m._close_overlay()
	m.room._wall_menu(m)
	await _save(m, "8_takeoff")
	m._close_overlay()
	# 9. deaths
	m.change_room("robot_head", "start")
	m.act("Walk to", "hotspot", "chasm")
	await m.get_tree().create_timer(0.6).timeout
	await _save(m, "9_death")
	m._on_restart()
	m.change_room("robot_head", "start")
	m.act("Pick up", "hotspot", "plate")
	await m.get_tree().create_timer(0.6).timeout
	await _save(m, "10_death_plate")
	m.get_tree().quit()
