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
		"id": "uniform", "name": "uniform", "rect": R(150, 50, 28, 44), "approach": P(163, 120), "default_verb": "Pick up",
		"visible": func(): return GameState.flag("locker_open") and not GameState.has_item("uniform") and not GameState.flag("wearing_uniform"),
		"verbs": {"Look at": _look_uniform, "Pick up": _take_uniform},
	})
	add_hotspot({
		"id": "hatch", "name": "airlock hatch", "rect": R(226, 24, 80, 84), "approach": P(266, 120),
		"verbs": {"Look at": _look_hatch, "Open": _open_hatch, "Push": _open_hatch, "Use": _open_hatch},
	})


func current_bg() -> String:
	if not GameState.flag("locker_open"):
		return "escape_pod"
	if GameState.has_item("uniform") or GameState.flag("wearing_uniform"):
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
		if GameState.has_item("uniform") or GameState.flag("wearing_uniform"):
			await m.say("An empty locker. It has the quiet dignity of something that has finished its job.")
		else:
			await m.say("Inside hangs a single orange-and-white uniform, pressed by the loving hands of nobody.")
	else:
		await m.say("A battered wall locker with a hand-lettered sign: 'PROPERTY OF SOMEONE WHO ISN'T YOU'.")

func _open_locker(m, _o) -> void:
	if GameState.flag("locker_open"):
		await m.say("It's open. Wider, and it would simply be a hole.")
		return
	GameState.set_flag("locker_open", true)
	queue_redraw()
	await m.say("The locker opens with the groan of a door that has opinions. Inside hangs a single orange-and-white uniform.")

func _close_locker(m, _o) -> void:
	if not GameState.flag("locker_open"):
		await m.say("It's closed. Your faith in it is touching.")
		return
	GameState.set_flag("locker_open", false)
	queue_redraw()
	await m.say("You close the locker. It sighs, which you choose to take as thanks.")

func _look_uniform(m, _o) -> void:
	await m.say("A sanitation uniform in regulation orange. The only colour in a universe otherwise committed to grey.")

func _take_uniform(m, _o) -> void:
	GameState.give_item("uniform")
	queue_redraw()
	await m.say("You take the uniform. It's the first thing in your life that has been issued to you on purpose.")

func _look_hatch(m, _o) -> void:
	await m.say("The airlock hatch. Beyond it: space, scrap, and a temperature best described as 'professional disappointment'.")

func _open_hatch(m, _o) -> void:
	if not GameState.flag("wearing_uniform"):
		await m.die("Cold Reception",
			"You step into the freighter in your underwear.\nThe air there is -80 degrees. Your last thought is that nobody ever tells you how loud your own teeth are.")
		return
	m.change_room("garbage_mountain", "pod")
