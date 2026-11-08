extends "res://scripts/room_base.gd"
# A room built entirely from data/rooms.json (see tools/make_rooms.py). Used for every room without custom puzzle logic.

const EXIT_VERBS := ["Walk to", "Open", "Climb", "Use", "Push", "Pull"]
static var _db = null


func on_verbs(hid: String, verbs: Array, handler: Callable) -> void:
	var h := get_hotspot(hid)
	for v in verbs:
		h["verbs"][v] = handler


func remove_hotspots(ids: Array) -> void:
	hotspots = hotspots.filter(func(h): return not ids.has(h["id"]))


func setup(room_id: String) -> void:
	if _db == null:
		_db = {}
		for path in ["res://data/rooms.json", "res://data/act1_rooms.json"]:
			var f := FileAccess.open(path, FileAccess.READ)
			for r in JSON.parse_string(f.get_as_text()):
				_db[r["id"]] = r
	var d: Dictionary = _db[room_id]
	id = room_id
	title = d["title"]
	bg = d["bg"]
	no_player = d["no_player"]
	walk_poly = PP(d["walk"])
	for k in d["entries"]:
		entries[k] = P(d["entries"][k][0], d["entries"][k][1])
	for h in d["hotspots"]:
		var r: Array = h["rect"]
		var look: String = h["look"]
		var verbs := {"Look at": func(m, _o): await m.say(look)}
		var hs := {"id": h["id"], "name": h["name"], "rect": R(r[0], r[1], r[2], r[3]), "verbs": verbs}
		if h.has("approach"):
			hs["approach"] = P(h["approach"][0], h["approach"][1])
		if h.has("default_verb"):
			hs["default_verb"] = h["default_verb"]
		if h.has("exit"):
			var target: String = h["exit"]["room"]
			var entry: String = h["exit"]["entry"]
			for v in EXIT_VERBS:
				verbs[v] = func(m, _o): m.change_room(target, entry)
			if not hs.has("default_verb"):
				hs["default_verb"] = "Walk to"
		add_hotspot(hs)
