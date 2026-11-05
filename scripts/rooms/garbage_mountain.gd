extends "res://scripts/room_base.gd"
# Act 1, scene 2 (stub): the garbage mountain. Only enough content to test room changes and scoring.


func _init() -> void:
	id = "garbage_mountain"
	title = "Garbage Mountain"
	walk_poly = PackedVector2Array([Vector2(30, 190), Vector2(610, 190), Vector2(630, 258), Vector2(10, 258)])
	entries = {"pod": Vector2(120, 215)}
	add_hotspot({
		"id": "pod_hatch", "name": "escape pod", "rect": Rect2(40, 90, 80, 110), "approach": Vector2(120, 215),
		"verbs": {"Look at": _look_pod, "Open": _enter_pod},
	})
	add_hotspot({
		"id": "wire", "name": "wire", "rect": Rect2(380, 160, 60, 30), "approach": Vector2(410, 205), "default_verb": "Pick up",
		"visible": func(): return not GameState.has_item("wire") and not GameState.flag("wire_taken"),
		"verbs": {"Look at": _look_wire, "Pick up": _take_wire},
	})
	add_hotspot({
		"id": "heap", "name": "junk heap", "rect": Rect2(200, 110, 140, 90),
		"verbs": {"Look at": _look_heap},
	})


func _draw() -> void:
	draw_rect(Rect2(0, 0, 640, 264), Color("14101a"))
	draw_rect(Rect2(0, 190, 640, 74), Color("2e2520"))
	draw_colored_polygon(PackedVector2Array([Vector2(200, 200), Vector2(250, 110), Vector2(300, 130), Vector2(340, 200)]), Color("4a3a30"))
	draw_rect(Rect2(40, 90, 80, 110), Color("4a5a6a"))
	if not GameState.has_item("wire") and not GameState.flag("wire_taken"):
		draw_rect(Rect2(380, 172, 60, 4), Color("d0a020"))
	draw_circle(Vector2(560, 40), 6, Color("e0c040"))                   # distant hazard light


func _look_pod(m, _o) -> void:
	await m.say("Your escape pod. It brought you here, which in fairness is all anyone asked of it.")

func _enter_pod(m, _o) -> void:
	m.change_room("escape_pod", "hatch")

func _look_wire(m, _o) -> void:
	await m.say("A length of wire, lying around with the confidence of something that will be needed later.")

func _take_wire(m, _o) -> void:
	GameState.give_item("wire")
	GameState.set_flag("wire_taken", true)
	queue_redraw()
	m.award("wire")
	await m.say("You pick up the wire. Not yet a plan, but certainly a start.")

func _look_heap(m, _o) -> void:
	await m.say("A hill of crushed metal. Somewhere in there, a thousand dreams sit folded in half. (End of test content: more to come.)")
