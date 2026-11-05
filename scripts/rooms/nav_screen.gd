extends "res://scripts/rooms/data_room.gd"
# Navigation computer: "2. Set course" cycles the destination; the cockpit's launch lever flies there.

const DESTS := [
	["landing_strip", "Phleebhut"],
	["monolith_exterior", "Monolith Burger"],
	["ortega_crater", "Ortega"],
	["pestulon_exterior", "Pestulon"],
]


func setup(room_id: String) -> void:
	super.setup(room_id)
	get_hotspot("course")["verbs"]["Look at"] = _cycle
	get_hotspot("course")["verbs"]["Use"] = _cycle
	get_hotspot("course")["verbs"]["Push"] = _cycle
	get_hotspot("course")["verbs"]["Walk to"] = _cycle
	get_hotspot("planet")["verbs"]["Look at"] = _read_planet


func _cycle(m, _o) -> void:
	var i := (int(GameState.flag("course_index", 0)) + 1) % DESTS.size()
	GameState.set_flag("course_index", i)
	await m.say("Course set for %s." % DESTS[i][1])


func _read_planet(m, _o) -> void:
	var i := int(GameState.flag("course_index", 0))
	await m.say("Destination: %s. The computer is confident. That's not the same as being right." % DESTS[i][1])
