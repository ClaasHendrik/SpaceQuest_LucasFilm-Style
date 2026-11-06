extends "res://scripts/rooms/data_room.gd"
# Act 1: the construction bay. Prop the ladder against the hull, open the top hatch, fit the reactor and the wire
# into the panel. With the motivator already seated, the ship has power and the ramp comes down.


func setup(room_id: String) -> void:
	super.setup(room_id)
	entries["west"] = P(40, 126)
	on_verbs("ship", ["Use"], _use_ship)
	on_verbs("ramp", ["Walk to", "Open", "Use", "Push", "Pull"], _ramp)
	add_hotspot({
		"id": "ladder", "name": "ladder", "rect": R(202, 36, 30, 84), "approach": P(214, 128),
		"visible": func(): return GameState.flag("ladder_placed"),
		"verbs": {"Look at": _look_ladder, "Use": _climb, "Pull": _climb, "Push": _climb},
	})
	add_hotspot({
		"id": "tophatch", "name": "top hatch", "rect": R(136, 30, 58, 14), "approach": P(214, 128),
		"visible": func(): return GameState.flag("ladder_placed") and not GameState.flag("hatch_open"),
		"verbs": {"Look at": _look_hatch, "Open": _open_hatch, "Use": _open_hatch, "Pull": _open_hatch},
	})
	add_hotspot({
		"id": "panel", "name": "engine panel", "rect": R(136, 28, 58, 16), "approach": P(214, 128),
		"visible": func(): return GameState.flag("hatch_open"),
		"verbs": {"Look at": _look_panel, "Use": _use_panel},
	})
	add_hotspot({
		"id": "reactor", "name": "reactor", "rect": R(236, 94, 30, 34), "approach": P(250, 132),
		"visible": func(): return _reactor_on_floor(),
		"verbs": {"Look at": _look_reactor, "Pick up": _take_reactor, "Pull": _take_reactor},
	})
	add_hotspot({
		"id": "door", "name": "service door", "rect": R(0, 46, 18, 76), "approach": P(24, 128),
		"verbs": {"Look at": _look_door, "Open": _go_door, "Walk to": _go_door, "Use": _go_door},
	})


func _reactor_on_floor() -> bool:
	return GameState.flag("reactor_delivered") and not GameState.has_item("reactor") and not GameState.flag("reactor_installed")


func current_bg() -> String:
	var l: bool = GameState.flag("ladder_placed")
	var r: bool = _reactor_on_floor()
	if l and r:
		return "mallard_bay_lr"
	if l:
		return "mallard_bay_l"
	if r:
		return "mallard_bay_r"
	return "mallard_bay"


func _powered() -> bool:
	return GameState.flag("motivator_installed") and GameState.flag("reactor_installed") and GameState.flag("wire_installed")


func _use_ship(m, other: Dictionary) -> void:
	if other.is_empty():
		await m.say("You pat the hull. It rattles, in a friendly way.")
		return
	match other["id"]:
		"ladder":
			if GameState.flag("ladder_placed"):
				await m.say("The ladder's already up. Don't push your luck.")
				return
			GameState.take_item("ladder")
			GameState.set_flag("ladder_placed")
			queue_redraw()
			m.award("ladder_ship_top")
			await m.say("You lean the ladder against the hull, up to a small hatch on top. The ship accepts this with the dignity of a patient in a gown.")
		"reactor", "wire":
			await m.say("Not on the hull. Whatever you plan to put in, it goes in through the panel on top.")
		_:
			await m.say("The ship has no use for that. It has no use for much, to be fair.")


func _look_ladder(m, _o) -> void:
	await m.say("Your ladder, leaning on the ship. It has already seen more use than it was ever promised.")


func _climb(m, _o) -> void:
	await m.say("You climb the ladder a few rungs and consider your life choices. The hatch is within reach from here.")


func _look_hatch(m, _o) -> void:
	await m.say("A small maintenance hatch on the roof of the ship, held shut by a latch and long habit.")


func _open_hatch(m, _o) -> void:
	GameState.set_flag("hatch_open")
	m.award("open_hatch")
	await m.say("You climb up and pop the hatch. Underneath: a power panel with a reactor-shaped hole and a wire-shaped hole, and a faint smell of old toast.")


func _look_panel(m, _o) -> void:
	var s := "The power panel. "
	s += "The reactor is in. " if GameState.flag("reactor_installed") else "It wants a reactor. "
	s += "The wire is connected." if GameState.flag("wire_installed") else "It wants a wire."
	await m.say(s)


func _use_panel(m, other: Dictionary) -> void:
	if other.is_empty():
		await m.say("You poke at the panel with a finger. A finger, it turns out, is neither a reactor nor a wire.")
		return
	match other["id"]:
		"reactor":
			GameState.take_item("reactor")
			GameState.set_flag("reactor_installed")
			queue_redraw()
			m.award("install_reactor")
			await m.say("You lower the reactor into the panel. It clicks home, and the ship's lights hum on, a pale amber, like a thought in the dark.")
		"wire":
			GameState.take_item("wire")
			GameState.set_flag("wire_installed")
			m.award("install_wire")
			await m.say("You fit the wire between the reactor and the panel. A small spark thanks you and goes out.")
		_:
			await m.say("That doesn't fit. Nothing else does either; you checked.")


func _look_reactor(m, _o) -> void:
	await m.say("The reactor the crane left on the deck. It is glowing at you, a little reproachfully.")


func _take_reactor(m, _o) -> void:
	GameState.give_item("reactor")
	queue_redraw()
	await m.say("You pick up the reactor. It's heavy, warm, and tells you nothing at all, which is how you'd like all your conversations with machinery to go.")


func _look_door(m, _o) -> void:
	await m.say("A service door back to the conveyor. It opens when it likes.")


func _go_door(m, _o) -> void:
	m.change_room("conveyor", "west")


func _ramp(m, _o) -> void:
	if _powered():
		await m.say("The boarding ramp whirrs down with a sigh. The Aluminum Mallard is, at last, ready to be wrong in a new direction.")
		m.change_room("cockpit", "start")
	elif not GameState.flag("hatch_open"):
		await m.say("The ramp stays up. The ship has the electrical personality of a boulder, and the hatch on top is still shut.")
	else:
		await m.say("The ramp stays up. The panel still wants something: a warp motivator, a reactor or a wire, or all three.")
