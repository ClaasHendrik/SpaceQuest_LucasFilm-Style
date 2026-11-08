extends "res://scripts/room_base.gd"
# Act 1, scene 1: the escape pod.


func _init() -> void:
	id = "escape_pod"
	title = "Escape Pod"
	walk_poly = PP([[14, 112], [306, 112], [318, 141], [2, 141]])
	entries = {"start": P(160, 126), "hatch": P(266, 122)}
	add_hotspot({
		"id": "cryo", "name": "cryo-chamber", "rect": R(10, 20, 72, 90), "approach": P(60, 120),
		"verbs": {"Look at": _look_cryo, "Open": _open_cryo, "Close": _close_cryo, "Use": _climb_cryo},
	})
	add_hotspot({
		"id": "locker", "name": "wall locker", "rect": R(140, 38, 46, 70), "approach": P(163, 120),
		"verbs": {"Look at": _look_locker, "Open": _open_locker, "Close": _close_locker, "Pull": _open_locker},
	})
	add_hotspot({
		"id": "manual", "name": "pod manual", "rect": R(150, 62, 28, 30), "approach": P(163, 120), "default_verb": "Pick up",
		"visible": func(): return GameState.flag("locker_open") and not GameState.has_item("manual") and not GameState.flag("manual_taken"),
		"verbs": {"Look at": _look_manual, "Pick up": _take_manual},
	})
	add_hotspot({
		"id": "hatch", "name": "airlock hatch", "rect": R(226, 24, 80, 84), "approach": P(266, 120),
		"verbs": {"Look at": _look_hatch, "Open": _open_hatch, "Push": _open_hatch, "Use": _open_hatch},
	})


func current_bg() -> String:
	if not GameState.flag("locker_open"):
		return "escape_pod"
	if GameState.has_item("manual") or GameState.flag("manual_taken"):
		return "escape_pod_open_empty"
	return "escape_pod_open"


func _look_cryo(m, _o) -> void:
	await m.say("Your cryo-chamber. Empty, open, and faintly warm, like a seat someone just gave up on you.")

func _open_cryo(m, _o) -> void:
	await m.say("It's already open. You are the one who isn't. Ready, that is.")

func _close_cryo(m, _o) -> void:
	await m.say("You are not getting back in there. You've only just got out.")

func _climb_cryo(m, _o) -> void:
	await m.say("Going back to sleep is not a plan. It's a lifestyle, and you can't afford it.")

func _look_locker(m, _o) -> void:
	if GameState.flag("locker_open"):
		if GameState.has_item("manual") or GameState.flag("manual_taken"):
			await m.say("An empty locker, apart from a flare and a folded blanket that nobody has ever needed. It has the quiet dignity of something that has finished its job.")
		else:
			await m.say("On the shelf: a flare, a folded emergency blanket, and a thin booklet that looks as though it has never once been opened.")
	else:
		await m.say("A battered wall locker with a hand-lettered sign: 'PROPERTY OF SOMEONE WHO ISN'T YOU'.")

func _open_locker(m, _o) -> void:
	if GameState.flag("locker_open"):
		await m.say("It's open. Wider, and it would simply be a hole.")
		return
	GameState.set_flag("locker_open", true)
	queue_redraw()
	await m.say("The locker opens with the groan of a door that has opinions. On the shelf lies a thin manual, bored and unread.")

func _close_locker(m, _o) -> void:
	if not GameState.flag("locker_open"):
		await m.say("It's closed. Your faith in it is touching.")
		return
	GameState.set_flag("locker_open", false)
	queue_redraw()
	await m.say("You close the locker. It sighs, which you choose to take as thanks.")

func _look_manual(m, _o) -> void:
	await m.say("The Escape Pod Owner's Manual. The cover promises 'Everything You Need to Know'. The back cover is less committal.")

func _take_manual(m, _o) -> void:
	GameState.give_item("manual")
	GameState.set_flag("manual_taken")
	queue_redraw()
	await m.say("You take the manual. It is light, unthumbed and, you suspect, the only thing on this ship that was ever meant to help.")

func _look_hatch(m, _o) -> void:
	await m.say("The airlock hatch. Beyond it: space, scrap, and a temperature best described as 'professional disappointment'.")

func _open_hatch(m, _o) -> void:
	m.change_room("crash_site", "pod")
