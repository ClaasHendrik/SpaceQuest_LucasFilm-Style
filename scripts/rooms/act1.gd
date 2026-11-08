extends "res://scripts/rooms/data_room.gd"
# Act 1 on the original layout (docs/ACT1_PLAN.md). One script for all Act 1 rooms, dispatched by room id.

const Art2 := preload("res://scripts/art.gd")
const MOTIVATOR_X := 52.0
const PANEL_X := 130.0
var claw_x := 160.0
var riding := false
var grabber_tex: Texture2D


func setup(room_id: String) -> void:
	super.setup(room_id)
	match room_id:
		"crash_site":
			on_verbs("object", ["Pick up", "Pull"], _object_pick)
			on_verbs("console", ["Use", "Push", "Pull"], func(m, _o): await m.say("You waggle the stick. Nothing waggles back. It was never connected to anything, and it is very honest about it."))
			on_verbs("barrel", ["Open", "Push", "Pull"], func(m, _o): await m.say("You push the barrel. It rolls half a turn and returns, like a cat that wants you to know it could leave."))
		"tube_entrance":
			get_hotspot("ladder")["visible"] = func(): return not GameState.flag("ladder_taken")
			on_verbs("ladder", ["Pick up", "Pull", "Use"], _ladder_pick)
			get_hotspot("e")["verbs"]["Look at"] = func(m, _o): await m.say("A square hole in the floor with a ladder inside. Cold air comes up, and small, interested sounds.")
		"wire_tube":
			get_hotspot("wires")["visible"] = func(): return not GameState.flag("wire_taken")
			on_verbs("wires", ["Pick up", "Pull", "Use"], _wire_pick)
		"robot_head":
			on_verbs("eye", ["Use", "Open", "Pull", "Push", "Walk to"], _eye)
			on_verbs("chasm", ["Walk to", "Use", "Open", "Push", "Pull"], _chasm)
			on_verbs("door", ["Open", "Push", "Pull", "Use"], func(m, _o): await m.say("The green panel does not open. It has been bent into a shape that has no interest in doors."))
		"yard", "yard_ladder":
			_setup_yard(room_id)
		"junk_tower":
			on_verbs("lift", ["Use", "Open", "Push", "Pull", "Walk to"], _lift)
		"conveyor":
			on_verbs("rail", ["Use", "Open", "Pull", "Push", "Walk to"], _jump)
			on_verbs("shredder", ["Walk to", "Use", "Push", "Pull"], func(m, _o): await m.say("You do not walk toward the shredder. Nobody has ever won an argument with it."))
		"rail_west":
			on_verbs("chute", ["Use", "Walk to", "Open", "Push"], _chute)
			get_hotspot("e")["verbs"]["Walk to"] = func(m, _o): await m.say("The rail runs on east into a part of the freighter you have no reason to see.")
		"rail_tower":
			on_verbs("grabber", ["Use", "Open", "Pull", "Push"], _mount)
		"dark_room":
			get_hotspot("reactor")["visible"] = func(): return not GameState.flag("reactor_taken")
			on_verbs("reactor", ["Pick up", "Pull", "Use", "Push"], _reactor_pick)


func current_bg() -> String:
	if id == "yard" and GameState.flag("ladder_placed"):
		return "yard_ladder"
	return id


func on_enter(m) -> void:
	match id:
		"wire_tube":
			if GameState.has_item("reactor") and not GameState.flag("rat_done"):
				_rat_steal(m)
		"conveyor":
			if not m.fast:
				_shredder(m)
		"dark_room":
			if not m.fast:
				_rats(m)
		"yard", "yard_ladder":
			if GameState.flag("riding") and not riding:
				_start_riding(m)


# ---------------------------------------------------------------- crash site and tube
func _object_pick(m, _o) -> void:
	await m.say("You pick up the small object, look at it with great attention, and put it back exactly where it was. You will remember where. It feels important to somebody, probably.")


func _wire_pick(m, _o) -> void:
	GameState.give_item("wire")
	GameState.set_flag("wire_taken")
	m.award("wire")
	await m.say("You pull a wire from the ceiling. It comes away with a small, tired spark. Not yet a plan, but certainly a start.")


func _ladder_pick(m, _o) -> void:
	GameState.give_item("ladder")
	GameState.set_flag("ladder_taken")
	queue_redraw()
	m.award("get_ladder")
	await m.say("You pick up the ladder. It is light and plain and the first thing in this freighter that looks as if it wants to help.")


func _rat_steal(m) -> void:
	GameState.set_flag("rat_done")
	await m.get_tree().create_timer(0.1 if m.fast else 1.5).timeout
	if GameState.has_item("reactor"):
		GameState.take_item("reactor")
		GameState.set_flag("reactor_taken", false)
	if GameState.has_item("wire"):
		GameState.take_item("wire")
		GameState.set_flag("wire_taken", false)
		queue_redraw()
	await m.say("Something fast and furry drops from the ceiling, takes the reactor and the wire in its teeth, and is gone down the tube with the speed of a rumour. It is a rat, and it is going to be a nuisance.")


# ---------------------------------------------------------------- robot head and yard
func _eye(m, _o) -> void:
	if not GameState.flag("eye_done"):
		GameState.set_flag("eye_done")
		m.award("robot_eye")
	await m.say("You squeeze through the crack in the eye and scramble up. From here, you can see a small shuttle in the junk, with a panel hanging open. The robot is not pleased and is too tired to say so.")
	m.change_room("yard", "eye")


func _chasm(m, _o) -> void:
	await m.die("Deceleration Trauma", "You step off the edge of the world and take the long way down.\nIt is very quiet, for a while. Then it is not, and then it is again.")


func _setup_yard(room_id: String) -> void:
	grabber_tex = Art2.tex("res://assets/sprites/grabber.png")
	on_verbs("motivator", ["Pick up", "Pull", "Push", "Use"], _motivator_click)
	on_verbs("panel", ["Use", "Push", "Pull", "Open"], _panel_click)
	get_hotspot("platform")["verbs"]["Walk to"] = _platform
	get_hotspot("platform")["verbs"]["Use"] = _platform
	on_verbs("ship", ["Use"], _use_ship)
	if room_id == "yard_ladder":
		on_verbs("ladder_on", ["Use", "Pull", "Push", "Walk to"], func(m, _o): await m.say("You climb the ladder a few rungs and consider your life choices. The hatch is within reach from here."))
		on_verbs("hatch", ["Open", "Use", "Pull"], _open_hatch)
		get_hotspot("panel")["verbs"]["Use"] = _use_panel
		get_hotspot("panel")["verbs"]["Look at"] = _look_power
		get_hotspot("hatch")["visible"] = func(): return not GameState.flag("hatch_open")
		get_hotspot("panel")["visible"] = func(): return GameState.flag("hatch_open")
		add_hotspot({"id": "to_cockpit", "name": "cockpit", "rect": R(150, 56, 60, 22), "approach": P(190, 128), "default_verb": "Open",
			"visible": func(): return GameState.flag("hatch_open"),
			"verbs": {"Look at": func(m, _o): await m.say("The shuttle's cockpit, through the open hatch."), "Open": _go_cockpit, "Use": _go_cockpit, "Walk to": _go_cockpit}})


func _draw() -> void:
	super._draw()
	if (id == "yard" or id == "yard_ladder") and (riding or GameState.flag("riding")):
		var x := claw_x * 2.0
		draw_line(Vector2(x, 0), Vector2(x, 86), Color("c8d0dc"), 3.0)
		draw_rect(Rect2(x - 16, 80, 32, 14), Color("c04848"))
		draw_rect(Rect2(x - 16, 80, 32, 3), Color("ff9a9a"))
		var held: bool = GameState.flag("motivator_held")
		if held:
			draw_rect(Rect2(x - 14, 96, 28, 18), Color("e8f0ee"))
			draw_rect(Rect2(x - 5, 100, 10, 10), Color("1a2a30"))
		else:
			draw_line(Vector2(x - 14, 94), Vector2(x - 8, 110), Color("c04848"), 3.0)
			draw_line(Vector2(x + 14, 94), Vector2(x + 8, 110), Color("c04848"), 3.0)


func _start_riding(m) -> void:
	riding = true
	m.player.visible = false
	claw_x = float(GameState.flag("claw_x", 160.0))
	queue_redraw()


func walk_request(m, pos: Vector2) -> bool:
	if riding:
		claw_x = clampf(pos.x / 2.0, 12.0, 308.0)
		GameState.set_flag("claw_x", claw_x)
		queue_redraw()
		return true
	if id == "rail_west" or id == "rail_window" or id == "rail_tower":
		if pos.y > 2.0 * 118.0:
			await m.die("Deceleration Trauma", "You step off the rail. The floor, far below, has been looking forward to this since the freighter was built.")
			return true
	return false


func _press(m) -> void:
	if GameState.flag("motivator_held"):
		if absf(claw_x - PANEL_X) <= 22.0:
			GameState.set_flag("motivator_held", false)
			GameState.set_flag("motivator_installed")
			queue_redraw()
			m.award("install_motivator")
			await m.say("The claw lowers the motivator into the open panel. It seats with a satisfying clunk. Somewhere, an engine begins to think about it.")
		else:
			await m.say("The claw dangles over nothing in particular and holds the motivator like a trophy it has nowhere to put.")
	else:
		if GameState.flag("motivator_installed"):
			await m.say("The claw closes on thin air and opens again, a little embarrassed.")
		elif absf(claw_x - MOTIVATOR_X) <= 22.0:
			GameState.set_flag("motivator_held")
			queue_redraw()
			m.award("grab_motivator")
			await m.say("The claw drops, grips the warp motivator and lifts it out of the rubble with a little mechanical sigh of satisfaction.")
		else:
			await m.say("The claw closes on thin air and opens again, a little embarrassed.")


func _motivator_click(m, _o) -> void:
	if riding:
		await _press(m)
	else:
		await m.say("You tug at it. It tugs back with the combined stubbornness of several tons. Clearly this is a job for something with a claw.")


func _panel_click(m, _o) -> void:
	if riding:
		await _press(m)
	else:
		await m.say("An open panel on the shuttle, with a gap for something big. You would need to drop it in from above.")


func _platform(m, _o) -> void:
	if riding:
		riding = false
		GameState.set_flag("riding", false)
		m.player.visible = true
		m.change_room("rail_west", "west")
		await m.say("You climb off the grabber onto the rail platform. A blue chute gapes at one end, and a railing at the other.")
	else:
		await m.say("The far end of the platform. Better to leave it to the rail, which knows its way.")


func _use_ship(m, other: Dictionary) -> void:
	if other.is_empty():
		await m.say("You pat the hull. It rattles, in a friendly way.")
		return
	match other["id"]:
		"ladder":
			if GameState.flag("ladder_placed"):
				await m.say("The ladder is already up. Don't push your luck.")
				return
			GameState.take_item("ladder")
			GameState.set_flag("ladder_placed")
			queue_redraw()
			m.award("ladder_ship_top")
			m.change_room("yard_ladder", "eye")
			await m.say("You lean the ladder against the hull, up to a small hatch on top. The ship accepts this with the dignity of a patient in a gown.")
		"reactor", "wire":
			await m.say("Not on the hull. Whatever you plan to put in, it goes in through the panel.")
		_:
			await m.say("The ship has no use for that. It has no use for much, to be fair.")


func _open_hatch(m, _o) -> void:
	GameState.set_flag("hatch_open")
	m.award("open_hatch")
	await m.say("You climb up and pop the hatch. Underneath: a power panel with a reactor-shaped hole and a wire-shaped hole, and a faint smell of old toast.")


func _look_power(m, _o) -> void:
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
			m.award("install_reactor")
			await m.say("You lower the reactor into the panel. It clicks home, and the ship's lights hum on, a pale amber, like a thought in the dark.")
		"wire":
			GameState.take_item("wire")
			GameState.set_flag("wire_installed")
			m.award("install_wire")
			await m.say("You fit the wire between the reactor and the panel. A small spark thanks you and goes out.")
		_:
			await m.say("That doesn't fit. Nothing else does either; you checked.")


func _go_cockpit(m, _o) -> void:
	m.change_room("cockpit", "start")


# ---------------------------------------------------------------- lift, conveyor, rail, chute
func _lift(m, _o) -> void:
	m.award("trash_bucket")
	await m.say("You step into the little bucket on the lift. It lurches upward with the grace of a bad idea.")
	m.change_room("conveyor", "lift")


func _shredder(m) -> void:
	for i in 26:
		await m.get_tree().create_timer(1.0).timeout
		if m.room != self or m.dead:
			return
		if i == 13:
			m.say("Somewhere ahead, the shredder clears its throat. It has an appointment, and you are in it.")
		if i == 21:
			m.say("The shredder is getting closer faster than your plan is getting together.")
	if m.room == self and not m.dead:
		await m.die("It Slices, It Dices...", "The shredder arrives with the punctuality of a bureaucrat and the warmth of a sales rep.\nRoger, afterwards, is considerably more compact and considerably less of a problem.")


func _jump(m, _o) -> void:
	if not GameState.flag("jumped_rail"):
		GameState.set_flag("jumped_rail")
		m.award("jump_rail")
	await m.say("You stand up, jump, catch the glowing rail and scramble onto it. You immediately regret looking down.")
	m.change_room("rail_west", "jump")


func _mount(m, _o) -> void:
	GameState.set_flag("riding", true)
	await m.say("You climb down onto the grabber. It hums, as if it has been waiting. Click along the yard to move the claw; push the motivator or the panel when the claw is over it.")
	m.change_room("yard_ladder" if GameState.flag("ladder_placed") else "yard", "claw")


func _chute(m, _o) -> void:
	if not GameState.flag("fell_chute"):
		GameState.set_flag("fell_chute")
		m.award("fall_chute")
	await m.say("You step into the chute. It takes you the way a rumour takes a town.")
	m.change_room("dark_room", "chute")


# ---------------------------------------------------------------- dark room
func _reactor_pick(m, _o) -> void:
	GameState.give_item("reactor")
	GameState.set_flag("reactor_taken")
	queue_redraw()
	if not GameState.flag("got_reactor_once"):
		GameState.set_flag("got_reactor_once")
		m.award("get_reactor")
	await m.say("You lift the reactor out of its hole. It is heavy, warm, and tells you nothing, which is how you would like all your conversations with machinery to go.")
	if GameState.flag("rat_done") and not GameState.has_item("wire") and not GameState.flag("wire_installed"):
		GameState.give_item("wire")
		GameState.set_flag("wire_taken")
		await m.say("The wire is down here too, the way the rat left it. You take it as well.")


func _rats(m) -> void:
	for i in 40:
		await m.get_tree().create_timer(1.0).timeout
		if m.room != self or m.dead:
			return
		if i == 20:
			m.say("Something in the corner is breathing. Slowly, and with interest.")
		if i == 32:
			m.say("The breathing has stopped. That is worse.")
	if m.room == self and not m.dead:
		await m.die("Rats!", "The rat reaches you first. It is large, patient and has been waiting a very long time for someone exactly this unlucky.")
