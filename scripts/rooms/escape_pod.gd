extends "res://scripts/room_base.gd"
# Act 1, scene 1: the escape pod. Placeholder art drawn in code.


func _init() -> void:
	id = "escape_pod"
	title = "Escape Pod"
	walk_poly = PackedVector2Array([Vector2(60, 200), Vector2(580, 200), Vector2(615, 255), Vector2(25, 255)])
	entries = {"start": Vector2(300, 228), "hatch": Vector2(500, 215)}
	add_hotspot({
		"id": "cryo", "name": "cryo-chamber", "rect": Rect2(70, 50, 90, 150), "approach": Vector2(150, 215),
		"verbs": {
			"Look at": _look_cryo, "Open": _open_cryo, "Close": _close_cryo, "Climb": _climb_cryo,
		},
	})
	add_hotspot({
		"id": "locker", "name": "wall locker", "rect": Rect2(260, 70, 70, 120), "approach": Vector2(295, 210),
		"verbs": {"Look at": _look_locker, "Open": _open_locker, "Close": _close_locker, "Pull": _open_locker},
	})
	add_hotspot({
		"id": "uniform", "name": "uniform", "rect": Rect2(275, 95, 40, 70), "approach": Vector2(295, 210),
		"default_verb": "Pick up",
		"visible": func(): return GameState.flag("locker_open") and not GameState.has_item("uniform") and not GameState.flag("wearing_uniform"),
		"verbs": {"Look at": _look_uniform, "Pick up": _take_uniform},
	})
	add_hotspot({
		"id": "hatch", "name": "airlock hatch", "rect": Rect2(470, 60, 80, 140), "approach": Vector2(500, 215),
		"verbs": {"Look at": _look_hatch, "Open": _open_hatch, "Push": _open_hatch, "Use": _open_hatch},
	})


func _draw() -> void:
	draw_rect(Rect2(0, 0, 640, 264), Color("0b0b1a"))                  # wall
	draw_rect(Rect2(0, 200, 640, 64), Color("2a2a3a"))                  # floor grating
	for x in range(0, 640, 24):
		draw_line(Vector2(x, 200), Vector2(x, 264), Color("3a3a4c"))
	draw_rect(Rect2(70, 50, 90, 150), Color("34506b"))                  # cryo chamber
	draw_rect(Rect2(80, 62, 70, 126), Color("1c2b3a"))
	draw_rect(Rect2(260, 70, 70, 120), Color("5a5a6a"))                 # locker
	if GameState.flag("locker_open"):
		draw_rect(Rect2(266, 76, 58, 108), Color("14141c"))
		if not GameState.has_item("uniform") and not GameState.flag("wearing_uniform"):
			draw_rect(Rect2(278, 98, 34, 66), Color("ff8c1a"))
	draw_rect(Rect2(470, 60, 80, 140), Color("7a6a3a"))                 # hatch
	draw_circle(Vector2(510, 130), 28, Color("1a1a24"))
	draw_circle(Vector2(510, 130), 20, Color("02020a"))


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
