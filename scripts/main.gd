extends Control
# Main controller: LucasFilm-style verb grid, sentence line, inventory, stage, death screen and menu.
# Layout (640x400): stage 0-264, sentence line 266, verb grid left and inventory right below.

# Verb grid as in the Lucasfilm interface: five columns, three rows. Label differs from the handler key for "Look".
const VERB_COLUMNS := [
	[["Push", "Push"], ["Pull", "Pull"], ["Give", "Give"]],
	[["Open", "Open"], ["Close", "Close"], ["Look", "Look at"]],
	[["Walk to", "Walk to"], ["Pick up", "Pick up"], ["What is", "What is"]],
	[["Use", "Use"], ["Turn on", "Turn on"], ["Turn off", "Turn off"]],
	[["Talk to", "Talk to"], ["Travel", "Travel"]],
]
const VERB_X := [6, 100, 209, 352, 515]
const CONTEXT_VERBS := ["Talk to", "Travel"]          # greyed out unless something in the room responds to them
const TWO_STEP := {"Use": "with", "Give": "to"}
const ROOMS := {
	"escape_pod": "res://scripts/rooms/escape_pod.gd",
	"garbage_mountain": "res://scripts/rooms/garbage_mountain.gd",
	"cockpit": "res://scripts/rooms/cockpit.gd",
	"nav_screen": "res://scripts/rooms/nav_screen.gd",
}
const DATA_ROOM := "res://scripts/rooms/data_room.gd"
const SAVE_SLOT := "slot1"
# Layout, 640x480: dialogue strip 0-40, scene 40-328, sentence line, verbs and inventory below.
const STRIP_H := 40
const STAGE_POS := Vector2(0, 40)
const STAGE_SIZE := Vector2(640, 288)
const COL_VERB := Color("00aa00")
const COL_VERB_HOVER := Color("55ff55")
const COL_GREY := Color("535552")
const COL_INV := Color("aa00aa")
const COL_INV_HOVER := Color("ff55ff")
const COL_SENTENCE := Color("00aaaa")
const COL_ROGER := Color("ffff55")
const FONT_SIZE := 22
const DEFAULTS := {
	"Open": ["It doesn't open. You check twice, because hope is cheap.", "You try. It declines."],
	"Close": ["It's not the closing kind.", "Closing it would improve nothing."],
	"Pick up": ["You can't take that. Believe me, you looked into it.", "It stays. Some things are above your pay grade."],
	"Talk to": ["It doesn't respond. Honestly, it's the best conversation you've had this week."],
	"Use": ["You can't think of a use for that. Neither can the universe."],
	"Push": ["You push. Nothing moves, least of all your confidence."],
	"Pull": ["You pull. It pulls back, in spirit."],
	"Give": ["It has no use for that. Rude."],
	"Turn on": ["There's nothing to turn on. You'll have to supply the enthusiasm yourself."],
	"Turn off": ["It isn't on. You're not sure it was ever really on."],
	"Travel": ["You can't travel from here. A pity; you've never been anywhere good."],
}

signal _never

var verb := "Walk to"
var pending := {}
var busy := false
var dead := false
var fast := false
var room
var player
var stage: Control
var sentence: Label
var message: Label
var score_flash: Label
var arrow_up: Button
var arrow_down: Button
var inv_box: Control
var overlay: Control
var verb_buttons: Dictionary = {}
var inv_offset := 0
var font: FontFile
var _say_skip := false
var _walk_token := 0
var _selftest
var room_ids: Array = []


func _ready() -> void:
	RenderingServer.set_default_clear_color(Color.BLACK)
	_build_ui()
	GameState.inventory_changed.connect(_refresh_inventory)
	_load_room_ids()
	var start_room: String = GameState.current_room
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--room="):
			start_room = a.substr(7)
	change_room(start_room, "start")
	_refresh_inventory()
	if OS.get_cmdline_user_args().has("--shot-pilot"):
		_selftest = load("res://tests/shot_pilot.gd").new()
		_selftest.run(self)
	elif OS.get_cmdline_user_args().has("--shot"):
		_selftest = load("res://tests/shot.gd").new()
		_selftest.run(self)
	elif OS.get_cmdline_user_args().has("--selftest"):
		_selftest = load("res://tests/selftest.gd").new()  # keep a reference or the coroutine is freed
		_selftest.run(self)


func _load_room_ids() -> void:
	room_ids = ["escape_pod", "garbage_mountain"]
	var f := FileAccess.open("res://data/rooms.json", FileAccess.READ)
	for r in JSON.parse_string(f.get_as_text()):
		room_ids.append(r["id"])


# --- UI construction -------------------------------------------------------
func _load_font() -> void:
	font = FontFile.new()
	font.data = FileAccess.get_file_as_bytes("res://assets/fonts/VT323-Regular.ttf")
	font.antialiasing = TextServer.FONT_ANTIALIASING_NONE
	font.hinting = TextServer.HINTING_NONE
	font.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED
	var th := Theme.new()
	th.default_font = font
	th.default_font_size = FONT_SIZE
	theme = th


func _build_ui() -> void:
	_load_font()
	var bg := ColorRect.new()
	bg.color = Color.BLACK
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	stage = Control.new()
	stage.position = STAGE_POS
	stage.size = STAGE_SIZE
	stage.clip_contents = true
	stage.mouse_filter = Control.MOUSE_FILTER_STOP
	stage.gui_input.connect(_on_stage_input)
	add_child(stage)

	player = load("res://scripts/player.gd").new()
	stage.add_child(player)

	# speech appears in the black strip above the scene, like the original
	message = _make_label(Vector2(8, 4), Vector2(624, 34), COL_ROGER)
	message.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	message.add_theme_font_size_override("font_size", 20)
	message.add_theme_constant_override("line_spacing", -5)
	message.visible = false
	add_child(message)

	sentence = _make_label(Vector2(6, 328), Vector2(320, 24), COL_SENTENCE)
	add_child(sentence)
	score_flash = _make_label(Vector2(330, 328), Vector2(304, 24), Color("55ff55"))
	score_flash.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	score_flash.visible = false
	add_child(score_flash)

	for c in VERB_COLUMNS.size():
		for r in VERB_COLUMNS[c].size():
			var label: String = VERB_COLUMNS[c][r][0]
			var key: String = VERB_COLUMNS[c][r][1]
			var b := _make_button(label, COL_VERB, COL_VERB_HOVER)
			b.add_theme_color_override("font_disabled_color", COL_GREY)
			b.position = Vector2(VERB_X[c], 354 + r * 18)
			b.size = Vector2(120, 18)
			b.pressed.connect(_on_verb_pressed.bind(key))
			b.mouse_entered.connect(_update_sentence)
			add_child(b)
			verb_buttons[key] = b

	inv_box = Control.new()
	inv_box.position = Vector2(0, 414)
	inv_box.size = Vector2(640, 60)
	add_child(inv_box)
	arrow_up = load("res://scripts/arrow.gd").new()
	arrow_up.position = Vector2(318, 416)
	arrow_up.size = Vector2(14, 14)
	arrow_up.pressed.connect(_scroll_inventory.bind(-1))
	add_child(arrow_up)
	arrow_down = load("res://scripts/arrow.gd").new()
	arrow_down.up = false
	arrow_down.position = Vector2(318, 456)
	arrow_down.size = Vector2(14, 14)
	arrow_down.pressed.connect(_scroll_inventory.bind(1))
	add_child(arrow_down)
	_update_sentence()


func _make_label(pos: Vector2, sz: Vector2, col: Color) -> Label:
	var l := Label.new()
	l.position = pos
	l.size = sz
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	l.add_theme_color_override("font_color", col)
	return l


func _make_button(text: String, col: Color, hover: Color) -> Button:
	var b := Button.new()
	b.text = text
	b.flat = true
	b.focus_mode = Control.FOCUS_NONE
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.add_theme_color_override("font_color", col)
	b.add_theme_color_override("font_hover_color", hover)
	b.add_theme_color_override("font_pressed_color", Color.WHITE)
	# the original has no button chrome: keep only the coloured text
	var empty := StyleBoxEmpty.new()
	for st in ["normal", "hover", "pressed", "disabled", "focus"]:
		b.add_theme_stylebox_override(st, empty)
	return b


func verb_enabled(key: String) -> bool:
	if not CONTEXT_VERBS.has(key):
		return true
	if room == null:
		return false
	for h in room.hotspots:
		if room._is_visible(h) and (h["verbs"] as Dictionary).has(key):
			return true
	return false


func _update_verb_states() -> void:
	for key in verb_buttons:
		var on := verb_enabled(key)
		verb_buttons[key].disabled = not on
		if not on and verb == key:
			verb = "Walk to"
	_update_sentence()


func _scroll_inventory(dir: int) -> void:
	inv_offset = clampi(inv_offset + dir, 0, maxi(0, GameState.inventory.size() - 6))
	_refresh_inventory()


func _refresh_inventory() -> void:
	for c in inv_box.get_children():
		c.queue_free()
	inv_offset = clampi(inv_offset, 0, maxi(0, GameState.inventory.size() - 6))
	for i in 6:
		var idx := inv_offset + i
		if idx >= GameState.inventory.size():
			break
		var id: String = GameState.inventory[idx]
		var nm: String = GameState.items.get(id, {}).get("name", id)
		var b := _make_button(nm, COL_INV, COL_INV_HOVER)
		b.position = Vector2(6 if i < 3 else 352, (i % 3) * 18)
		b.size = Vector2(300, 18)
		b.pressed.connect(_on_target.bind("item", id))
		b.mouse_entered.connect(_update_sentence.bind(nm))
		b.mouse_exited.connect(_update_sentence)
		inv_box.add_child(b)
	arrow_up.visible = inv_offset > 0
	arrow_down.visible = GameState.inventory.size() > inv_offset + 6


func _update_sentence(hover_name := "") -> void:
	var s := _verb_label(verb)
	if pending.size() > 0:
		s = "%s %s %s" % [s, _target_name(pending), TWO_STEP.get(verb, "")]
	if hover_name != "":
		s += " " + hover_name
	sentence.text = s.strip_edges()


func _verb_label(key: String) -> String:
	return "Look at" if key == "Look at" else key


func _target_name(t: Dictionary) -> String:
	if t["kind"] == "item":
		return GameState.items.get(t["id"], {}).get("name", t["id"])
	var h: Dictionary = room.get_hotspot(t["id"])
	return h.get("name", t["id"])


# --- rooms ------------------------------------------------------------------
func change_room(room_id: String, entry = "start") -> void:
	if room != null:
		stage.remove_child(room)
		room.queue_free()
	if ROOMS.has(room_id):
		room = load(ROOMS[room_id]).new()
	else:
		room = load(DATA_ROOM).new()
	if room.has_method("setup"):
		room.setup(room_id)
	stage.add_child(room)
	stage.move_child(room, 0)
	GameState.current_room = room_id
	var p: Vector2
	if typeof(entry) == TYPE_VECTOR2:
		p = entry
	else:
		p = room.entries.get(entry, room.entries.values()[0])
	player.visible = not room.no_player
	player.position = p
	player.walk_target = p
	player.walking = false
	_walk_token += 1
	pending = {}
	verb = "Walk to"
	_update_sentence()
	player.queue_redraw()
	room.on_enter(self)
	_update_verb_states()


func walk_to(pos: Vector2) -> void:
	_walk_token += 1
	var tok := _walk_token
	player.speed = 130.0 * (30.0 if fast else 1.0)
	player.walk_target = room.clamp_to_walk(pos)
	player.walking = true
	while player.walking and tok == _walk_token:
		await get_tree().process_frame


# --- speech, score, death -----------------------------------------------------
func say(text: String, col := Color("ffff55")) -> void:
	message.text = text
	message.add_theme_color_override("font_color", col)
	message.visible = true
	_say_skip = false
	var dur := 0.03 if fast else maxf(1.5, text.length() * 0.05)
	var t := 0.0
	while t < dur and not _say_skip:
		await get_tree().process_frame
		t += get_process_delta_time()
	message.visible = false


func award(id: String) -> void:
	var p := GameState.add_score(id)
	if p > 0:
		_flash("+%d points   Score: %d of %d" % [p, GameState.score, GameState.max_score])


func _flash(text: String) -> void:
	score_flash.text = text
	score_flash.visible = true
	await get_tree().create_timer(0.1 if fast else 2.5).timeout
	if score_flash.text == text:
		score_flash.visible = false


func die(title: String, text: String) -> void:
	dead = true
	_show_overlay(title, text, [["Restore", _on_restore], ["Restart", _on_restart], ["Quit", _on_quit]])
	await _never


# --- overlay (death screen and menu) -------------------------------------------
func _show_overlay(title: String, text: String, buttons: Array) -> void:
	_close_overlay()
	overlay = Control.new()
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.86)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	overlay.add_child(dim)
	var t := _make_label(Vector2(60, 80), Vector2(520, 30), Color("ff5555"))
	t.text = title
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 30)
	overlay.add_child(t)
	var body := _make_label(Vector2(80, 130), Vector2(480, 150), Color("ffffff"))
	body.text = text
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	overlay.add_child(body)
	var y := 300
	for bd in buttons:
		var b := _make_button(bd[0], COL_VERB, COL_VERB_HOVER)
		b.alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.position = Vector2(240, y)
		b.size = Vector2(160, 22)
		b.pressed.connect(bd[1])
		overlay.add_child(b)
		y += 26
	add_child(overlay)


func _close_overlay() -> void:
	if overlay != null:
		overlay.queue_free()
		overlay = null


func _on_restore() -> void:
	if not GameState.load_slot(SAVE_SLOT):
		_show_overlay("No saved game", "You never saved. A bold strategy, and one the universe has noted.",
			[["Restart", _on_restart], ["Quit", _on_quit]])
		return
	dead = false
	busy = false
	_close_overlay()
	change_room(GameState.current_room, GameState.player_pos)
	_refresh_inventory()


func _on_restart() -> void:
	GameState.reset()
	dead = false
	busy = false
	_close_overlay()
	change_room("escape_pod", "start")
	_refresh_inventory()


func _on_quit() -> void:
	get_tree().quit()


func _open_menu() -> void:
	_show_overlay("Space Quest III", "Score: %d of %d" % [GameState.score, GameState.max_score], [
		["Resume", _close_overlay],
		["Save", func(): GameState.player_pos = player.position; GameState.save_slot(SAVE_SLOT); _close_overlay()],
		["Restore", _on_restore],
		["Restart", _on_restart],
		["Quit", _on_quit],
	])


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and not dead:
		if event.keycode == KEY_ESCAPE:
			if overlay != null:
				_close_overlay()
			else:
				_open_menu()
		elif (event.keycode == KEY_F2 or event.keycode == KEY_F3) and overlay == null and not busy:
			# developer shortcut: F2 / F3 = previous / next room
			var idx := room_ids.find(room.id)
			idx = (idx + (1 if event.keycode == KEY_F3 else -1) + room_ids.size()) % room_ids.size()
			change_room(room_ids[idx], "start")
		elif event.keycode == KEY_TAB and overlay == null:
			_flash("Score: %d of %d" % [GameState.score, GameState.max_score])


# --- input / interaction ------------------------------------------------------
func _on_verb_pressed(v: String) -> void:
	if overlay != null or dead:
		return
	if busy:
		_say_skip = true
		return
	verb = v
	pending = {}
	_update_sentence()


func _on_stage_input(event: InputEvent) -> void:
	if overlay != null or dead:
		return
	if event is InputEventMouseMotion:
		_update_sentence(room.hotspot_at(event.position).get("name", ""))
	elif event is InputEventMouseButton and event.pressed:
		if busy:
			_say_skip = true
			return
		var hs: Dictionary = room.hotspot_at(event.position)
		if event.button_index == MOUSE_BUTTON_LEFT:
			if hs.is_empty():
				pending = {}
				verb = "Walk to"
				_update_sentence()
				walk_to(event.position)
			else:
				_on_target("hotspot", hs["id"])
		elif event.button_index == MOUSE_BUTTON_RIGHT and not hs.is_empty():
			pending = {}
			verb = hs.get("default_verb", "Look at")
			_on_target("hotspot", hs["id"])


func _on_target(kind: String, id: String) -> void:
	if dead or overlay != null:
		return
	if busy:
		_say_skip = true
		return
	var a := {"kind": kind, "id": id}
	if pending.size() > 0:
		var first: Dictionary = pending
		pending = {}
		await _execute(verb, first, a)
		return
	if kind == "item" and TWO_STEP.has(verb) and not (verb == "Use" and GameState.items.get(id, {}).get("wearable", false)):
		pending = a
		_update_sentence()
		return
	var v1 := verb
	if kind == "item" and v1 == "Walk to":
		v1 = "Look at"
	await _execute(v1, a, {})


# Public so tests can drive it: perform verb on a (and b for two-step verbs).
func act(v: String, kind: String, id: String, other_kind := "", other_id := "") -> void:
	verb = v
	pending = {}
	if other_kind == "":
		await _on_target(kind, id)
	else:
		pending = {"kind": kind, "id": id}
		await _on_target(other_kind, other_id)


func _execute(v: String, a: Dictionary, b: Dictionary) -> void:
	busy = true
	if a["kind"] == "hotspot":
		await _run_hotspot(v, a["id"], b)
	else:
		await _run_item(v, a, b)
	busy = false
	verb = "Walk to"
	pending = {}
	_update_verb_states()


func _run_hotspot(v: String, hid: String, other: Dictionary) -> void:
	var hs: Dictionary = room.get_hotspot(hid)
	if hs.is_empty():
		return
	var verbs: Dictionary = hs["verbs"]
	if not room.no_player:
		await walk_to(hs.get("approach", (hs["rect"] as Rect2).get_center()))
	if v == "Walk to" and not verbs.has("Walk to"):
		return
	var h = verbs.get(v)
	if h is Callable:
		await h.call(self, other)
	else:
		await say(_default_text(v, hs["name"]))


func _run_item(v: String, a: Dictionary, b: Dictionary) -> void:
	var item: Dictionary = GameState.items.get(a["id"], {})
	var nm: String = item.get("name", "that")
	match v:
		"Look at":
			await say(item.get("look", "It's an item. Obviously."))
		"What is":
			await say(_default_text(v, nm))
		"Use", "Give":
			if b.is_empty():
				if v == "Use" and item.get("wearable", false):
					GameState.take_item(a["id"])
					GameState.set_flag(item["wear_flag"], true)
					player.queue_redraw()
					await say(item["wear_text"])
				else:
					await say("Use it on what?")
			elif b["kind"] == "hotspot":
				await _run_hotspot(v, b["id"], a)
			else:
				await say("That would accomplish nothing. Heroically.")
		_:
			await say(_default_text(v, nm))


func _default_text(v: String, name: String) -> String:
	if v == "Look at":
		return "You see nothing special about the %s." % name
	if v == "What is":
		return "That's the %s. Nothing more, nothing less." % name
	var opts: Array = DEFAULTS.get(v, ["Nothing happens."])
	return opts[randi() % opts.size()]
