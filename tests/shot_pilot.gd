extends RefCounted
# Pilot screens for the new look:  SHOT_DIR=/dir xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x960 -- --shot-pilot


func _save(m, name: String) -> void:
	await m.get_tree().process_frame
	await m.get_tree().process_frame
	var dir := OS.get_environment("SHOT_DIR") if OS.has_environment("SHOT_DIR") else "user://"
	m.get_viewport().get_texture().get_image().save_png("%s/pilot_%s.png" % [dir, name])
	print("saved ", name)


func _talk(m, text: String) -> void:
	m.message.text = text
	m.message.visible = true


func run(m) -> void:
	m.fast = true
	await m.get_tree().create_timer(0.3).timeout
	m.change_room("escape_pod", "start")
	m.player.position = Vector2(300, 250)
	m.player.walk_target = m.player.position
	m._update_sentence("wall locker")
	await _save(m, "1_pod")
	await m.act("Open", "hotspot", "locker")
	m.message.visible = false
	m.verb = "Pick up"
	m._update_sentence("pod manual")
	await _save(m, "2_locker_open")
	await m.act("Pick up", "hotspot", "manual")
	m.message.visible = false
	m.verb = "Use"
	m._update_sentence()
	await _save(m, "3_manual_in_inventory")
	m.message.visible = false
	await m.act("Open", "hotspot", "hatch")
	m.message.visible = false
	m.player.position = Vector2(320, 262)
	m.player.walk_target = m.player.position
	_talk(m, "A hill of crushed metal. Somewhere in there, a thousand dreams sit folded in half.")
	m.verb = "Look at"
	m._update_sentence("junk heap")
	await _save(m, "4_garbage_mountain")
	await m.act("Pick up", "hotspot", "wire")
	m.message.visible = false
	m.verb = "Walk to"
	m._update_sentence()
	m.player.position = Vector2(300, 262)
	await _save(m, "5_with_wire")
	m.get_tree().quit()
