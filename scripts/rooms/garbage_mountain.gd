extends "res://scripts/room_base.gd"
# Act 1, scene 2: the garbage mountain.


func _init() -> void:
	id = "garbage_mountain"
	title = "Garbage Mountain"
	walk_poly = PP([[10, 106], [310, 106], [318, 129], [2, 129]])
	entries = {"pod": P(62, 114), "start": P(62, 114), "east": P(290, 114), "south": P(160, 122)}
	add_hotspot({
		"id": "pod_hatch", "name": "escape pod", "rect": R(8, 56, 46, 44), "approach": P(62, 112),
		"verbs": {"Look at": _look_pod, "Open": _enter_pod},
	})
	add_hotspot({
		"id": "wire", "name": "wire", "rect": R(194, 92, 34, 12), "approach": P(206, 112), "default_verb": "Pick up",
		"visible": func(): return not GameState.has_item("wire") and not GameState.flag("wire_taken"),
		"verbs": {"Look at": _look_wire, "Pick up": _take_wire},
	})
	add_hotspot({
		"id": "heap", "name": "junk heap", "rect": R(150, 30, 140, 66),
		"verbs": {"Look at": _look_heap},
	})
	add_hotspot({
		"id": "starfighter", "name": "wrecked starfighter", "rect": R(104, 62, 56, 50), "approach": P(132, 114),
		"verbs": {"Look at": _look_fighter},
	})
	add_hotspot({
		"id": "east", "name": "path east", "rect": R(296, 50, 24, 56), "approach": P(300, 112), "default_verb": "Walk to",
		"verbs": {"Walk to": _go_east, "Open": _go_east, "Use": _go_east},
	})
	add_hotspot({
		"id": "south", "name": "way south", "rect": R(100, 118, 120, 11), "approach": P(160, 124), "default_verb": "Walk to",
		"verbs": {"Walk to": _go_south, "Open": _go_south, "Use": _go_south},
	})


func current_bg() -> String:
	return "garbage_mountain_nowire" if (GameState.has_item("wire") or GameState.flag("wire_taken")) else "garbage_mountain"


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
	await m.say("A hill of crushed metal. Somewhere in there, a thousand dreams sit folded in half.")

func _look_fighter(m, _o) -> void:
	await m.say("A crumpled starfighter, its cockpit dented like a bad review. Whoever flew it didn't land it; they merely stopped.")

func _go_east(m, _o) -> void:
	m.change_room("robot_head", "west")

func _go_south(m, _o) -> void:
	m.change_room("conveyor", "start")
