extends RefCounted
# Visual check: godot --path . -- --shot  -> saves screenshots to $SHOT_DIR (or user://)
var steps := 0
func run(m) -> void:
	m.fast = true
	await m.get_tree().create_timer(0.5).timeout
	_save(m, "1_start")
	await m.act("Open", "hotspot", "locker")
	m.message.visible = false
	await m.get_tree().process_frame
	_save(m, "2_locker_open")
	await m.act("Pick up", "hotspot", "uniform")
	await m.get_tree().process_frame
	m.verb = "Use"; m._update_sentence("uniform")
	await m.get_tree().process_frame
	_save(m, "3_inventory")
	m.get_tree().quit()
func _save(m, name: String) -> void:
	var img: Image = m.get_viewport().get_texture().get_image()
	print("saving ", name, " ", img.get_size())
	img.save_png(OS.get_environment("SHOT_DIR") + "/shot_%s.png" % name if OS.has_environment("SHOT_DIR") else "user://shot_%s.png" % name)
