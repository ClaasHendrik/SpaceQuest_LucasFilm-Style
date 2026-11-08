extends "res://scripts/rooms/data_room.gd"
# The cockpit. Act 1: search the seat for buckazoids, power the ship up on the computer, and blast out of the freighter.
# After the escape, the computer plots courses (see nav_screen.gd) and the launch lever flies there.

const Nav := preload("res://scripts/rooms/nav_screen.gd")


func setup(room_id: String) -> void:
	super.setup(room_id)
	on_verbs("seat", ["Use", "Open", "Pick up", "Pull"], _search)
	get_hotspot("seat")["verbs"]["Look at"] = _look_seat
	on_verbs("computer", ["Use", "Push"], _computer)
	get_hotspot("computer")["verbs"]["Travel"] = _computer
	on_verbs("launch", ["Walk to", "Use", "Pull", "Push", "Travel"], _launch)
	get_hotspot("launch")["verbs"]["Look at"] = _look_lever


func _look_seat(m, _o) -> void:
	await m.say("The pilot's seat. It has the shape of a person who has long since given up. The cushion is lumpy in a way that suggests savings.")


func _search(m, _o) -> void:
	if GameState.flag("seat_searched"):
		await m.say("You search the cushion again. Lint, a button, and a deep sense of having been here before.")
		return
	GameState.set_flag("seat_searched")
	GameState.give_item("buckazoids")
	m.award("search_cushion")
	await m.say("You dig into the cushion and come out with a fistful of buckazoids: 350 of them. The previous pilot must have been saving for an escape.")


func _look_lever(m, _o) -> void:
	await m.say("The launch lever. It does nothing until the computer is ready, and the computer is never ready on the first try.")


func _launch(m, _o) -> void:
	if not GameState.flag("escaped_freighter"):
		await m.say("You pull the lever. Nothing happens, with great conviction. The computer has to agree first.")
		return
	var d: Array = Nav.DESTS[int(GameState.flag("course_index", 0)) % Nav.DESTS.size()]
	await m.say("The Aluminum Mallard shudders, thinks it over, and heads for %s." % d[1])
	m.change_room(d[0], "start")


func _computer(m, _o) -> void:
	if GameState.flag("escaped_freighter"):
		m.change_room("nav_screen", "start")
		return
	if not (GameState.flag("motivator_installed") and GameState.flag("reactor_installed") and GameState.flag("wire_installed")):
		await m.say("The computer is dark. It is waiting for a warp motivator, a reactor and a wire, and it is not shy about the order.")
		return
	_menu(m)


# ---------------------------------------------------------------- the ship's computer (menu overlay)
func _on(f: String) -> String:
	return "ON" if GameState.flag(f) else "off"


func _menu(m, note := "") -> void:
	var text := "Engines: %s     Radar: %s     Weapons: %s" % [_on("sys_engines"), _on("sys_radar"), _on("sys_weapons")]
	if note != "":
		text += "\n\n" + note
	m._show_overlay("Ship's Computer", text, [
		["1   Engines", func(): _toggle(m, "sys_engines")],
		["7   Radar", func(): _toggle(m, "sys_radar")],
		["8   Weapons", func(): _toggle(m, "sys_weapons")],
		["3   Takeoff", func(): _takeoff(m)],
		["Close", func(): m._close_overlay()],
	])


func _toggle(m, f: String) -> void:
	GameState.set_flag(f, not GameState.flag(f))
	_menu(m)


func _takeoff(m) -> void:
	if not GameState.flag("sys_engines"):
		_menu(m, "The engines are off. The ship rises about as well as an opinion.")
		return
	if not GameState.flag("sys_radar"):
		m._close_overlay()
		await m.die("Learn to Drive That Thing!",
			"You take off without radar, which is the sort of thing the manual warns about, in the part nobody reads.\nThe freighter's roof is the first thing you meet, and the last.")
		return
	m._close_overlay()
	GameState.set_flag("launched")
	_wall_menu(m)


func _wall_menu(m, note := "") -> void:
	var text := "The Mallard rises. Dead ahead, the freighter's wall.\nEngines: %s    Weapons: %s    Front shields: %s" % [_on("sys_engines"), _on("sys_weapons"), _on("sys_front")]
	if note != "":
		text += "\n\n" + note
	m._show_overlay("Takeoff", text, [
		["1   Engines", func(): _wall_toggle(m, "sys_engines")],
		["8   Weapons", func(): _wall_toggle(m, "sys_weapons")],
		["F   Front shields", func(): _wall_toggle(m, "sys_front")],
		["Fire", func(): _fire(m)],
	])


func _wall_toggle(m, f: String) -> void:
	GameState.set_flag(f, not GameState.flag(f))
	if f == "sys_engines" and not GameState.flag("sys_engines"):
		m._close_overlay()
		m.die("Learn to Drive That Thing!",
			"You switch off the engines mid-flight. The ship, with admirable honesty, stops being a ship and starts being a falling object.")
		return
	_wall_menu(m)


func _fire(m) -> void:
	if not GameState.flag("sys_weapons"):
		_wall_menu(m, "The weapons are off. You pull the trigger anyway, in spirit.")
		return
	if not GameState.flag("sys_front"):
		m._close_overlay()
		m.die("Decompression Blues",
			"The blast tears a hole in the wall. Unfortunately, your own front plating goes first.\nThe vacuum, to its credit, is very fast about it.")
		return
	m._close_overlay()
	GameState.set_flag("escaped_freighter")
	m.award("escape_freighter")
	m.say("The lasers carve a doorway through the freighter and the Aluminum Mallard bursts out into open space. Behind you, the garbage freighter goes on, eating the universe at its own pace. Plot a course on the navigation computer.")
