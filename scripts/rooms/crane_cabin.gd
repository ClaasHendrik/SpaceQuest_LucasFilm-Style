extends "res://scripts/rooms/data_room.gd"
# Act 1: the crane cabin. The joystick aims the claw (left / over the pit / over the construction bay);
# the red button closes or opens it. The reactor goes from the pit to the bay.

const POS_X := [78.0, 102.0, 126.0]
const POS_NAME := ["the far left of the cavern", "directly over the reactor pit", "the construction bay"]


func setup(room_id: String) -> void:
	super.setup(room_id)
	on_verbs("stick", ["Use", "Push", "Pull"], _stick)
	get_hotspot("stick")["verbs"]["Push"] = _stick_right
	get_hotspot("stick")["verbs"]["Pull"] = _stick_left
	on_verbs("button", ["Use", "Push", "Pull", "Open", "Close"], _button)
	on_verbs("monitor", ["Look at", "What is"], _look_monitor)


func _draw() -> void:
	super._draw()
	var pos := int(GameState.flag("crane_pos", 0))
	var x: float = POS_X[pos] * 2.0
	var col := Color("ffffff") if not GameState.flag("crane_holding") else Color("55ff55")
	draw_rect(Rect2(x - 9, 142 - 7, 18, 14), col, false, 2.0)
	draw_line(Vector2(x - 12, 142), Vector2(x + 12, 142), col, 1.0)
	draw_line(Vector2(x, 142 - 10), Vector2(x, 142 + 10), col, 1.0)


func _look_monitor(m, _o) -> void:
	var pos := int(GameState.flag("crane_pos", 0))
	await m.say("The monitor shows a wireframe of the cavern and a reticle hovering over %s. The reactor, below, is a green smudge with ambitions." % POS_NAME[pos])


func _move(m, d: int) -> void:
	var pos := clampi(int(GameState.flag("crane_pos", 0)) + d, 0, 2)
	GameState.set_flag("crane_pos", pos)
	queue_redraw()
	await m.say("The crane hums towards %s. On the monitor, the reticle follows, slightly late and entirely committed." % POS_NAME[pos])


func _stick(m, _o) -> void:
	var pos := (int(GameState.flag("crane_pos", 0)) + 1) % 3
	GameState.set_flag("crane_pos", pos)
	queue_redraw()
	await m.say("You wag the stick. The crane drifts to %s." % POS_NAME[pos])


func _stick_right(m, _o) -> void:
	await _move(m, 1)


func _stick_left(m, _o) -> void:
	await _move(m, -1)


func _button(m, _o) -> void:
	var pos := int(GameState.flag("crane_pos", 0))
	if not GameState.flag("crane_holding"):
		if pos == 1 and not GameState.flag("reactor_taken"):
			GameState.set_flag("crane_holding")
			GameState.set_flag("reactor_taken")
			queue_redraw()
			m.award("get_reactor")
			await m.say("The claw drops, clamps the reactor and hoists it into the dark, glowing like a very expensive nightlight. The rat, unseen, files a complaint.")
		elif pos == 1:
			await m.say("The claw closes on the empty pit. The empty pit does not mind.")
		else:
			await m.say("The claw closes on nothing, which it does very well. It's had practice.")
		return
	if pos == 2:
		GameState.set_flag("crane_holding", false)
		GameState.set_flag("reactor_delivered")
		queue_redraw()
		await m.say("The reactor swings out over the construction bay and lands on the deck beside the Mallard, humming smugly.")
	else:
		GameState.set_flag("crane_holding", false)
		GameState.set_flag("reactor_taken", false)
		queue_redraw()
		await m.say("The claw opens in the wrong place. The reactor drops back into its pit with a thud that sounds like disappointment.")
