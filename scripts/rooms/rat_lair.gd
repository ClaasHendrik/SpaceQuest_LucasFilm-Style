extends "res://scripts/rooms/data_room.gd"
# Act 1: the reactor cavern and the rat's lair. A portable ladder lies on the platform. The rat arrives on a timer.


func setup(room_id: String) -> void:
	super.setup(room_id)
	get_hotspot("reactor")["visible"] = func(): return not GameState.flag("reactor_taken")
	on_verbs("reactor", ["Pick up", "Pull", "Use", "Push"], _reactor)
	add_hotspot({
		"id": "portable", "name": "ladder", "rect": R(100, 38, 36, 46), "approach": P(112, 100), "default_verb": "Pick up",
		"visible": func(): return not GameState.flag("ladder_taken"),
		"verbs": {"Look at": _look_ladder, "Pick up": _take_ladder, "Pull": _take_ladder},
	})


func current_bg() -> String:
	var r: bool = GameState.flag("reactor_taken")
	var l: bool = GameState.flag("ladder_taken")
	if r and l:
		return "rat_lair_empty"
	if r:
		return "rat_lair_noreactor"
	if l:
		return "rat_lair_noladder"
	return "rat_lair"


func on_enter(m) -> void:
	if m.fast:
		return
	_rat(m)


func _rat(m) -> void:
	for i in 28:
		await m.get_tree().create_timer(1.0).timeout
		if m.room != self or m.dead:
			return
		if i == 14:
			m.say("Something in the pipe is breathing. Slowly, and with interest.")
		if i == 22:
			m.say("The breathing has stopped. That's worse.")
	if m.room == self and not m.dead:
		await m.die("Rats!",
			"The rat reaches you first. It is large, patient and has been waiting a very long time for someone exactly this unlucky.")


func _reactor(m, _o) -> void:
	await m.say("You hold your hand near the reactor. The hair on your arm leaves without saying goodbye. Not by hand.")


func _look_ladder(m, _o) -> void:
	await m.say("A light ladder, left on the platform by someone who knew the value of being able to leave.")


func _take_ladder(m, _o) -> void:
	GameState.give_item("ladder")
	GameState.set_flag("ladder_taken")
	queue_redraw()
	m.award("get_ladder")
	await m.say("You pick up the ladder. It's light and plain and the first thing in the freighter that looks like it wants to help.")
