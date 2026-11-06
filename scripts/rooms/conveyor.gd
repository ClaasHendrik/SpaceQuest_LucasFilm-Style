extends "res://scripts/rooms/data_room.gd"
# Act 1: the conveyor and the crusher. A clock runs while Roger is in here. The bucket takes him up to the rail;
# the drainage pipe is the quick way to the reactor cavern.


func setup(room_id: String) -> void:
	super.setup(room_id)
	remove_hotspots(["ladder"])
	add_hotspot({
		"id": "bucket", "name": "trash bucket", "rect": R(2, 50, 28, 40), "approach": P(30, 124), "default_verb": "Use",
		"verbs": {"Look at": _look_bucket, "Use": _bucket, "Open": _bucket, "Pull": _bucket, "Push": _bucket, "Pick up": _bucket, "Walk to": _bucket},
	})
	on_verbs("pipe", ["Walk to", "Use", "Open", "Push", "Pull"], _dive)
	on_verbs("crusher", ["Walk to", "Use", "Push", "Pull"], _crusher)


func on_enter(m) -> void:
	if m.fast:
		return
	_clock(m)


func _clock(m) -> void:
	for i in 26:
		await m.get_tree().create_timer(1.0).timeout
		if m.room != self or m.dead:
			return
		if i == 13:
			m.say("Somewhere above you, the crusher clears its throat. It has an appointment, and you are in it.")
		if i == 21:
			m.say("The crusher is coming down faster than your plan is coming together.")
	if m.room == self and not m.dead:
		await m.die("It Slices, It Dices...",
			"The crusher arrives with the punctuality of a bureaucrat and the warmth of a sales rep.\nRoger, afterwards, is considerably more compact and considerably less of a problem.")


func _look_bucket(m, _o) -> void:
	await m.say("A vertical trash bucket on a chain, rising into the dark. Every few minutes it hauls the junk up to the rail. Today it might haul you.")


func _bucket(m, _o) -> void:
	m.award("trash_bucket")
	await m.say("You climb into the bucket. It lurches upward with the grace of a bad idea.")
	m.change_room("rail_walk", "start")


func _dive(m, _o) -> void:
	await m.say("You dive into the drainage pipe, headfirst, because feet-first looked like a worse decision.")
	m.change_room("rat_lair", "pipe")


func _crusher(m, _o) -> void:
	await m.say("You do not walk toward the crusher. Nobody has ever won an argument with it.")
