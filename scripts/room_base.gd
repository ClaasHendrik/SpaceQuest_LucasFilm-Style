extends Node2D
# Base class for rooms. Rooms are scripts that fill in hotspots, a walk polygon and entry points.
# Hotspot dictionary: id, name, rect (Rect2), approach (Vector2, optional), default_verb (optional),
# visible (Callable -> bool, optional), verbs {verb_name: Callable(main, other_dict)}.

var id := ""
var title := ""
var walk_poly := PackedVector2Array()
var hotspots: Array = []
var entries: Dictionary = {}


func on_enter(_main) -> void:
	pass


func add_hotspot(h: Dictionary) -> void:
	hotspots.append(h)


func get_hotspot(hid: String) -> Dictionary:
	for h in hotspots:
		if h["id"] == hid:
			return h
	return {}


func _is_visible(h: Dictionary) -> bool:
	var v = h.get("visible")
	return not (v is Callable) or v.call()


func hotspot_at(p: Vector2) -> Dictionary:
	for i in range(hotspots.size() - 1, -1, -1):
		var h: Dictionary = hotspots[i]
		if _is_visible(h) and (h["rect"] as Rect2).has_point(p):
			return h
	return {}


func clamp_to_walk(p: Vector2) -> Vector2:
	if walk_poly.size() < 3 or Geometry2D.is_point_in_polygon(p, walk_poly):
		return p
	var best := p
	var best_d := INF
	for i in walk_poly.size():
		var q := Geometry2D.get_closest_point_to_segment(p, walk_poly[i], walk_poly[(i + 1) % walk_poly.size()])
		var d := p.distance_squared_to(q)
		if d < best_d:
			best_d = d
			best = q
	return best
