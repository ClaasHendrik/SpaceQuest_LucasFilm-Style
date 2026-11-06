extends "res://scripts/rooms/data_room.gd"
# Act 1: the overhead rail. Jump onto the rail, ride the grabber, lift the warp motivator from its pedestal
# and set it into the Mallard's open panel. Stepping off the rail is the quickest way to the floor.

const GRABBER_Y := 66          # top of the grabber sprite (art pixels)
const SPOT_PEDESTAL := 38.0
const SPOT_PANEL := 283.0
const LEFT := 14.0
const RIGHT := 308.0

var gx := 198.0
var target := 198.0
var riding := false
var deck_poly := PackedVector2Array()
var grabber_tex: Texture2D


func setup(room_id: String) -> void:
	super.setup(room_id)
	deck_poly = walk_poly
	gx = float(GameState.flag("grabber_x", 198.0))
	target = gx
	GameState.set_flag("on_rail", false)
	remove_hotspots(["rail", "grabber"])
	get_hotspot("w")["visible"] = func(): return not GameState.flag("on_rail")
	add_hotspot({
		"id": "rail", "name": "cyan rail", "rect": R(0, 68, 320, 16), "approach": P(160, 76), "default_verb": "Use",
		"verbs": {"Look at": _look_rail, "Use": _jump, "Open": _jump, "Pull": _jump, "Push": _jump, "Walk to": _rail_walk},
	})
	add_hotspot({
		"id": "grabber", "name": "grabber", "rect": R(gx - 12, 62, 26, 50), "approach": P(gx, 76), "default_verb": "Use",
		"verbs": {"Look at": _look_grabber, "Use": _mount, "Push": _button, "Pull": _button, "What is": _look_grabber},
	})
	add_hotspot({
		"id": "motivator", "name": "warp motivator", "rect": R(26, 90, 26, 40), "approach": P(60, 126),
		"visible": func(): return not GameState.flag("motivator_held") and not GameState.flag("motivator_installed"),
		"verbs": {"Look at": _look_motivator, "Pick up": _heavy, "Pull": _heavy},
	})
	add_hotspot({
		"id": "panel", "name": "open panel", "rect": R(262, 92, 44, 24), "approach": P(270, 126),
		"verbs": {"Look at": _look_panel},
	})
	add_hotspot({
		"id": "chute", "name": "blue chute", "rect": R(0, 52, 30, 46), "approach": P(20, 76), "default_verb": "Use",
		"verbs": {"Look at": _look_chute, "Use": _chute, "Open": _chute, "Walk to": _chute, "Push": _chute},
	})
	grabber_tex = Art.tex("res://assets/sprites/grabber.png")


func current_bg() -> String:
	if GameState.flag("motivator_installed"):
		return "rail_walk_installed"
	if GameState.flag("motivator_held"):
		return "rail_walk_gone"
	return "rail_walk"


func _process(delta: float) -> void:
	if gx != target:
		gx = move_toward(gx, target, 80.0 * delta)
		GameState.set_flag("grabber_x", gx)
		get_hotspot("grabber")["rect"] = R(gx - 12, 62, 26, 50)
		queue_redraw()


func set_grabber(x: float) -> void:
	gx = x
	target = x
	GameState.set_flag("grabber_x", gx)
	get_hotspot("grabber")["rect"] = R(gx - 12, 62, 26, 50)
	queue_redraw()


func _draw() -> void:
	super._draw()
	if grabber_tex != null:
		draw_texture_rect(grabber_tex, Rect2(gx * 2 - 24, GRABBER_Y * 2, 48, 92), false)
		if riding:
			var rt := Art.tex("res://assets/sprites/roger.png")
			var outfit := 1 if GameState.flag("wearing_uniform") else 0
			if rt != null:
				draw_texture_rect_region(rt, Rect2(gx * 2 - 28, (GRABBER_Y + 4) * 2 - 104, 56, 104), Rect2(outfit * 5 * 28, 0, 28, 52))


func _on_rail(m) -> void:
	GameState.set_flag("on_rail")
	walk_poly = PP([[2, 74], [318, 74], [318, 77], [2, 77]])
	m.player.position = Vector2(clampf(m.player.position.x, 20, 620), 150)
	m.player.walk_target = m.player.position
	m.player.queue_redraw()


func walk_request(m, pos: Vector2) -> bool:
	if riding:
		target = clampf(pos.x / 2.0, LEFT, RIGHT)
		return true
	if GameState.flag("on_rail") and pos.y > 2 * 100:
		await m.die("Deceleration Trauma",
			"You step off the rail. The floor, far below, has been looking forward to this since the freighter was built.")
		return true
	return false


# ---------------------------------------------------------------- hotspot handlers
func _look_rail(m, _o) -> void:
	await m.say("A long cyan rail hung from the ceiling. Something that was clearly meant to carry loads, not people, is parked on it.")


func _jump(m, _o) -> void:
	if GameState.flag("on_rail"):
		await m.say("You're already up on the rail, which is as far as ambition goes in this place.")
		return
	_on_rail(m)
	m.award("jump_rail")
	await m.say("You jump, catch the rail, scramble up and stand on it. You immediately regret looking down.")


func _rail_walk(m, _o) -> void:
	if not GameState.flag("on_rail"):
		await _jump(m, _o)
		return
	var x := clampf(m.stage.get_local_mouse_position().x, 24.0, 616.0)
	await m.walk_to(Vector2(x, 150))


func _look_grabber(m, _o) -> void:
	await m.say("A rail grabber: a cab, a rod and a claw. Whoever it belonged to went home early, and left the keys in it.")


func _mount(m, _o) -> void:
	if riding:
		riding = false
		m.player.visible = true
		m.player.position = Vector2(gx * 2, 150)
		m.player.walk_target = m.player.position
		m.player.queue_redraw()
		queue_redraw()
		await m.say("You climb off the grabber onto the rail.")
		return
	if not GameState.flag("on_rail"):
		await m.say("The grabber is up on the rail and you are down here, in the part of the freighter where people are.")
		return
	riding = true
	m.player.visible = false
	queue_redraw()
	await m.say("You climb onto the grabber. Click along the rail to ride. Push the button, grabber, to work the claw.")


func _button(m, _o) -> void:
	if not riding:
		await m.say("The button is on the grabber. You'd have to be on the grabber.")
		return
	if absf(gx - SPOT_PEDESTAL) <= 16.0:
		if GameState.flag("motivator_held"):
			await m.say("The claw already has the motivator. It's holding it like a trophy.")
		elif GameState.flag("motivator_installed"):
			await m.say("The pedestal is empty. Success is always a little empty.")
		else:
			GameState.set_flag("motivator_held")
			queue_redraw()
			m.award("grab_motivator")
			await m.say("The claw drops, grips the warp motivator and lifts it free with a little mechanical sigh of satisfaction.")
	elif absf(gx - SPOT_PANEL) <= 18.0:
		if GameState.flag("motivator_held"):
			GameState.set_flag("motivator_held", false)
			GameState.set_flag("motivator_installed")
			queue_redraw()
			m.award("install_motivator")
			await m.say("The claw lowers the motivator into the open panel. It seats with a satisfying clunk. Somewhere, an engine thinks about it.")
		else:
			await m.say("The claw dangles over the open panel and holds nothing, which is the most tactful way to be useless.")
	else:
		await m.say("The claw clamps shut on thin air, then opens again, a little embarrassed.")


func _look_motivator(m, _o) -> void:
	await m.say("A warp motivator on a pedestal, glowing the green of money that isn't yours. It's far too heavy to lift by hand.")


func _heavy(m, _o) -> void:
	await m.say("You tug at it. It tugs back with the combined stubbornness of several tons. Clearly this is a job for something with a claw.")


func _look_panel(m, _o) -> void:
	if GameState.flag("motivator_installed"):
		await m.say("The panel on the Mallard's back, now with a warp motivator inside it. The ship looks a little more like it believes in itself.")
	else:
		await m.say("An open maintenance panel on the back of a small, tired ship. There's a motivator-sized gap inside, and nothing to fill it.")


func _look_chute(m, _o) -> void:
	await m.say("A blue garbage chute at the end of the rail, leading down and, you suspect, to a worse place than the one you're in.")


func _chute(m, _o) -> void:
	if not GameState.flag("on_rail"):
		await m.say("The chute is up on the rail. So, annoyingly, is everything useful.")
		return
	if riding:
		await m.say("Get off the grabber first. Falling down a chute in a vehicle is the kind of thing that has paperwork.")
		return
	m.award("fall_chute")
	await m.say("You step into the chute. It takes you the way a rumour takes a town.")
	m.change_room("rat_lair", "pipe")
