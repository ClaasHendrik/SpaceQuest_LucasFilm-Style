extends Node
# Global game state: flags, inventory, score (events from data/points.json), save/restore.
# Registered as the autoload "GameState". Deliberately has no class_name.

signal inventory_changed
signal score_changed(score)

const POINTS_PATH := "res://data/points.json"
const ITEMS_PATH := "res://data/items.json"
const SAVE_DIR := "user://saves"

var flags: Dictionary = {}
var inventory: Array = []
var awarded: Dictionary = {}
var score: int = 0
var max_score: int = 0
var current_room: String = "escape_pod"
var player_pos: Vector2 = Vector2(300, 225)
var points: Dictionary = {}
var items: Dictionary = {}


func _init() -> void:
	for e in _read_json(POINTS_PATH, []):
		points[e["id"]] = e
		max_score += int(e["points"])
	items = _read_json(ITEMS_PATH, {})


func _read_json(path: String, fallback):
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		push_error("Cannot open " + path)
		return fallback
	var data = JSON.parse_string(f.get_as_text())
	return fallback if data == null else data


func reset() -> void:
	flags = {}
	inventory = []
	awarded = {}
	score = 0
	current_room = "escape_pod"
	player_pos = Vector2(300, 225)
	inventory_changed.emit()
	score_changed.emit(score)


# --- flags -------------------------------------------------------------
func set_flag(name: String, value = true) -> void:
	flags[name] = value


func flag(name: String, default = false):
	return flags.get(name, default)


# --- inventory ---------------------------------------------------------
func has_item(id: String) -> bool:
	return inventory.has(id)


func give_item(id: String) -> void:
	if not inventory.has(id):
		inventory.append(id)
		inventory_changed.emit()


func take_item(id: String) -> void:
	if inventory.has(id):
		inventory.erase(id)
		inventory_changed.emit()


# --- score -------------------------------------------------------------
# Returns the points actually added. 0 for unknown ids or events already awarded.
func add_score(id: String) -> int:
	if not points.has(id):
		push_warning("Unknown score event: " + id)
		return 0
	if awarded.has(id):
		return 0
	awarded[id] = true
	var p := int(points[id]["points"])
	score += p
	score_changed.emit(score)
	return p


# --- save / restore ------------------------------------------------------
func serialize() -> Dictionary:
	return {
		"flags": flags, "inventory": inventory, "awarded": awarded, "score": score,
		"room": current_room, "player_pos": [player_pos.x, player_pos.y],
	}


func deserialize(d: Dictionary) -> void:
	flags = d.get("flags", {})
	inventory = d.get("inventory", [])
	awarded = d.get("awarded", {})
	score = int(d.get("score", 0))
	current_room = d.get("room", "escape_pod")
	var pp = d.get("player_pos", [300, 225])
	player_pos = Vector2(pp[0], pp[1])
	inventory_changed.emit()
	score_changed.emit(score)


func save_slot(slot: String) -> bool:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR)
	var f := FileAccess.open("%s/%s.json" % [SAVE_DIR, slot], FileAccess.WRITE)
	if f == null:
		return false
	f.store_string(JSON.stringify(serialize()))
	return true


func has_slot(slot: String) -> bool:
	return FileAccess.file_exists("%s/%s.json" % [SAVE_DIR, slot])


func load_slot(slot: String) -> bool:
	if not has_slot(slot):
		return false
	var f := FileAccess.open("%s/%s.json" % [SAVE_DIR, slot], FileAccess.READ)
	var d = JSON.parse_string(f.get_as_text())
	if typeof(d) != TYPE_DICTIONARY:
		return false
	deserialize(d)
	return true
