extends "res://scripts/rooms/data_room.gd"
# Act 1: the giant robot head. The broken eye is a way in (and a view of the Mallard); the chasm and the plate are ways out.


func setup(room_id: String) -> void:
	super.setup(room_id)
	on_verbs("eye", ["Use", "Open", "Pull", "Push"], _enter_eye)
	on_verbs("chasm", ["Walk to", "Use", "Open", "Push", "Pull"], _chasm)
	on_verbs("plate", ["Pick up", "Pull"], _plate)


func _enter_eye(m, _o) -> void:
	if GameState.flag("eye_done"):
		await m.say("You've seen what's in there. A great deal of dust, and a view.")
		return
	GameState.set_flag("eye_done")
	GameState.set_flag("saw_panel")
	m.award("robot_eye")
	await m.say("You squeeze through the crack in the eye. From in here, between the scrap, you can see a small ship with a maintenance panel hanging open. Also, the robot has not been dusted in years.")


func _chasm(m, _o) -> void:
	await m.die("Deceleration Trauma",
		"You step off the edge of the world and take the long way down.\nIt is very quiet, for a while. Then it is not, and then it is again.")


func _plate(m, _o) -> void:
	await m.die("One Way to Lower Your Blood Pressure",
		"You pick up the plate. It is sharper than it looks, which is remarkable, because it looks like a bad decision with edges.")
