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


# ---------------------------------------------------------------- the ship's computer, in the original's screen layout
const GREEN := Color("00aa00")
const GREEN_HI := Color("55ff55")
const GREY := Color("535552")
const FLAT_Y := 40.0            # the 320x200 original is drawn at 2x, centred in the 640x480 window


func _on(f: String) -> String:
	return "ON" if GameState.flag(f) else "off"


func _frame(parent: Control, r: Rect2, col: Color, fill: Color = Color(0, 0, 0, 0), w := 2) -> Panel:
	var p := Panel.new()
	p.position = r.position
	p.size = r.size
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sb := StyleBoxFlat.new()
	sb.bg_color = fill
	sb.border_color = col
	sb.set_border_width_all(w)
	p.add_theme_stylebox_override("panel", sb)
	parent.add_child(p)
	return p


func _label(parent: Control, text: String, pos: Vector2, col: Color, size_ := 18, w := 0.0, center := false) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	if w > 0.0:
		l.size = Vector2(w, 24)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER if center else HORIZONTAL_ALIGNMENT_LEFT
	l.add_theme_color_override("font_color", col)
	l.add_theme_font_size_override("font_size", size_)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(l)
	return l


func _key(parent: Control, r: Rect2, key: String, text: String, active: bool, cb: Callable) -> void:
	_frame(parent, r, GREEN, GREEN if active else Color(0, 0, 0, 0))
	_label(parent, key + ".", r.position + Vector2(4, 0), Color.BLACK if active else GREEN, 18)
	_label(parent, text, r.position + Vector2(24, 0), Color.BLACK if active else GREEN, 16, r.size.x - 24)
	var b := Button.new()
	b.flat = true
	b.position = r.position
	b.size = r.size
	b.focus_mode = Control.FOCUS_NONE
	var empty := StyleBoxEmpty.new()
	for st in ["normal", "hover", "pressed", "disabled", "focus"]:
		b.add_theme_stylebox_override(st, empty)
	b.pressed.connect(cb)
	parent.add_child(b)


func _screen(m) -> Control:
	m._close_overlay()
	var ov := Control.new()
	ov.set_anchors_preset(Control.PRESET_FULL_RECT)
	ov.mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := ColorRect.new()
	bg.color = Color.BLACK
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_STOP
	ov.add_child(bg)
	m.overlay = ov
	m.add_child(ov)
	return ov


func _menu(m, note := "") -> void:
	# the flight screen: Engines and Navigation, Flight Mode (Takeoff, Cruise, Light Speed, Attack Speed), Defense (Radar, Weapons)
	var ov := _screen(m)
	var y := FLAT_Y + 12
	_key(ov, Rect2(12, y, 262, 36), "1", "ENGINES", GameState.flag("sys_engines"), func(): _toggle(m, "sys_engines"))
	_key(ov, Rect2(12, y + 40, 262, 36), "2", "NAVIGATION", false, func(): _menu(m, "Navigation is offline until the ship has left the freighter."))
	_frame(ov, Rect2(290, y - 4, 214, 84), GREEN, Color(0, 0, 0, 0), 1)
	_label(ov, "FLIGHT MODE", Vector2(290, y - 24), GREEN, 16, 214.0, true)
	_key(ov, Rect2(296, y, 100, 36), "3", "TAKEOFF", false, func(): _takeoff(m))
	_key(ov, Rect2(400, y, 100, 36), "5", "LIGHT SPD", false, func(): _menu(m, "The engines are not that sure of themselves yet."))
	_key(ov, Rect2(296, y + 40, 100, 36), "4", "CRUISE", false, func(): _menu(m, "There is nothing to cruise to."))
	_key(ov, Rect2(400, y + 40, 100, 36), "6", "ATTACK SPD", false, func(): _menu(m, "Attack speed is for attacking, and nobody has asked."))
	_frame(ov, Rect2(520, y - 4, 110, 84), GREEN, Color(0, 0, 0, 0), 1)
	_label(ov, "DEFENSE", Vector2(520, y - 24), GREEN, 16, 110.0, true)
	_key(ov, Rect2(526, y, 98, 36), "7", "RADAR", GameState.flag("sys_radar"), func(): _toggle(m, "sys_radar"))
	_key(ov, Rect2(526, y + 40, 98, 36), "8", "WEAPONS", GameState.flag("sys_weapons"), func(): _toggle(m, "sys_weapons"))
	_label(ov, "PRESS F6 FOR COCKPIT VIEW", Vector2(0, y + 112), GREEN_HI, 18, 640.0, true)
	_frame(ov, Rect2(14, y + 148, 612, 150), Color("aa0000"), Color(0, 0, 0, 0), 2)
	var lines := PackedStringArray()
	lines.append("ENGINES: %s     RADAR: %s     WEAPONS: %s" % [_on("sys_engines"), _on("sys_radar"), _on("sys_weapons")])
	lines.append("")
	lines.append("CURRENT SECTOR: 75")
	lines.append("NO COURSE SELECTED")
	if note != "":
		lines.append("")
		lines.append(note)
	_label(ov, "\n".join(lines), Vector2(30, y + 156), GREEN, 17, 584.0)
	_key(ov, Rect2(500, y + 258, 120, 32), "X", "EXIT", false, func(): m._close_overlay())


func _takeoff(m) -> void:
	if not GameState.flag("sys_engines"):
		_menu(m, "ADEQUATE THRUST NOT ACHIEVED. The ship rises about as well as an opinion.")
		return
	if not GameState.flag("sys_radar"):
		m._close_overlay()
		await m.die("Learn to Drive That Thing!",
			"You take off without radar, which is the sort of thing the manual warns about, in the part nobody reads.\nThe freighter's roof is the first thing you meet, and the last.")
		return
	m._close_overlay()
	GameState.set_flag("launched")
	Sfx.play("takeoff")
	await m.play_cutscene([["cut_takeoff", 2.2, "The Mallard shudders, thinks it over, and lifts off the deck. Dead ahead: the freighter's wall."]])
	_wall_menu(m)


func _wall_menu(m, note := "") -> void:
	# the weapons screen: controls, shields (front and back), a radar and a FIRE key
	var ov := _screen(m)
	var cy := FLAT_Y + 6
	_frame(ov, Rect2(6, cy, 628, 380), Color("5555ff"), Color("0a0a40"), 4)
	_frame(ov, Rect2(14, cy + 8, 612, 364), Color("aa00aa"), Color(0, 0, 0, 0), 2)
	_label(ov, "CONTROLS", Vector2(22, cy + 18), GREEN_HI, 16)
	_label(ov, "SHIELDS", Vector2(520, cy + 18), GREEN_HI, 16)
	_key(ov, Rect2(22, cy + 44, 130, 40), "H", "HELP", false, func(): _wall_menu(m, "Front shields before you fire. Back shields are for when you are being followed."))
	_key(ov, Rect2(22, cy + 92, 130, 40), "O", "OFF", false, func(): _wall_toggle_weapons(m))
	_frame(ov, Rect2(22, cy + 160, 130, 70), GREEN, Color(0, 0, 0, 0), 1)
	_label(ov, "RADAR", Vector2(22, cy + 140), GREEN_HI, 14, 130.0, true)
	_label(ov, "TARGET:\n%s" % ("WALL" if GameState.flag("sys_weapons") else "-"), Vector2(30, cy + 166), GREEN, 15)
	_key(ov, Rect2(510, cy + 44, 108, 40), "F", "FRONT", GameState.flag("sys_front"), func(): _wall_toggle(m, "sys_front"))
	_key(ov, Rect2(510, cy + 92, 108, 40), "B", "BACK", GameState.flag("sys_back"), func(): _wall_toggle(m, "sys_back"))
	# the view: a red crosshair frame with two white stars
	_frame(ov, Rect2(170, cy + 40, 320, 230), Color("ff5555"), Color(0, 0, 0, 0), 2)
	var ln := ColorRect.new()
	ln.color = Color("ff5555")
	ln.position = Vector2(329, cy + 40)
	ln.size = Vector2(2, 230)
	ov.add_child(ln)
	var ln2 := ColorRect.new()
	ln2.color = Color("ff5555")
	ln2.position = Vector2(170, cy + 154)
	ln2.size = Vector2(320, 2)
	ov.add_child(ln2)
	for sx in [230, 430]:
		_label(ov, "*", Vector2(sx, cy + 140), Color("ffffff"), 28)
	_label(ov, "WEAPONS: %s    ENGINES: %s" % [_on("sys_weapons"), _on("sys_engines")], Vector2(170, cy + 276), GREEN, 15, 320.0, true)
	if note != "":
		_label(ov, note, Vector2(22, cy + 304), Color("ffff55"), 16, 596.0)
	var fire := Button.new()
	fire.text = "FIRE"
	fire.position = Vector2(270, cy + 326)
	fire.size = Vector2(120, 34)
	fire.add_theme_color_override("font_color", Color.BLACK)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color("ffff55")
	sb.border_color = Color("aa5500")
	sb.set_border_width_all(2)
	fire.add_theme_stylebox_override("normal", sb)
	fire.add_theme_stylebox_override("hover", sb)
	fire.add_theme_stylebox_override("pressed", sb)
	fire.focus_mode = Control.FOCUS_NONE
	fire.pressed.connect(func(): _fire(m))
	ov.add_child(fire)
	_label(ov, "SPACE BAR", Vector2(270, cy + 360), Color("ffff55"), 13, 120.0, true)


func _wall_toggle_weapons(m) -> void:
	GameState.set_flag("sys_weapons", not GameState.flag("sys_weapons"))
	_wall_menu(m)


func _toggle(m, f: String) -> void:
	Sfx.play("click")
	GameState.set_flag(f, not GameState.flag(f))
	_menu(m)


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
	Sfx.play("blast")
	await m.play_cutscene([
		["cut_blast", 2.4, "The lasers punch a doorway through the freighter, and the Mallard follows them out."],
		["cut_free", 2.4, "Behind you, the garbage freighter goes on eating the universe at its own pace."],
		["cut_away", 1.8, "Plot a course on the navigation computer."],
	])
	GameState.set_flag("escaped_freighter")
	m.award("escape_freighter")
