extends "res://scripts/rooms/data_room.gd"
# Cockpit: the launch lever flies to the destination chosen on the navigation computer.

const Nav := preload("res://scripts/rooms/nav_screen.gd")


func setup(room_id: String) -> void:
	super.setup(room_id)
	get_hotspot("launch")["verbs"]["Walk to"] = _launch
	get_hotspot("launch")["verbs"]["Use"] = _launch
	get_hotspot("launch")["verbs"]["Pull"] = _launch
	get_hotspot("launch")["verbs"]["Push"] = _launch
	get_hotspot("launch")["verbs"]["Look at"] = _look_lever
	get_hotspot("launch")["verbs"]["Travel"] = _launch
	get_hotspot("computer")["verbs"]["Travel"] = func(m, _o): m.change_room("nav_screen", "start")


func _look_lever(m, _o) -> void:
	await m.say("The launch lever. Set a course on the computer first, unless you enjoy surprises.")


func _launch(m, _o) -> void:
	var d: Array = Nav.DESTS[int(GameState.flag("course_index", 0)) % Nav.DESTS.size()]
	await m.say("The Aluminum Mallard shudders, thinks it over, and heads for %s." % d[1])
	m.change_room(d[0], "start")
