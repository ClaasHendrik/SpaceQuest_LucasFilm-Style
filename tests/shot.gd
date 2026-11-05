extends RefCounted
# Visual check / gallery source: renders every room at the window size and saves PNGs.
#   SHOT_DIR=/some/dir xvfb-run -a godot --path . --rendering-driver opengl3 --windowed --resolution 1280x800 -- --shot
var _keep


func run(m) -> void:
	m.fast = true
	var dir := OS.get_environment("SHOT_DIR") if OS.has_environment("SHOT_DIR") else "user://"
	await m.get_tree().create_timer(0.3).timeout
	for rid in m.room_ids:
		m.change_room(rid, "start")
		await m.get_tree().process_frame
		await m.get_tree().process_frame
		var img: Image = m.get_viewport().get_texture().get_image()
		img.save_png("%s/%s.png" % [dir, rid])
		print("saved ", rid)
	m.get_tree().quit()
