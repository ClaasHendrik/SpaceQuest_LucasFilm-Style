extends Node2D
# Base class for rooms. Art is 320x132 native, shown 2x (640x264). Coordinates in code are stage pixels;
# use R() and P() to write them in art pixels.
# Hotspot dictionary: id, name, rect (Rect2), approach (Vector2, optional), default_verb (optional),
# visible (Callable -> bool, optional), verbs {verb_name: Callable(main, other_dict)}.

const Art := preload("res://scripts/art.gd")

var id := ""
var title := ""
var bg := ""
var no_player := false
var walk_poly := PackedVector2Array()
var hotspots: Array = []
var entries: Dictionary = {}


static func R(x: float, y: float, w: float, h: float) -> Rect2:
	return Rect2(x * 2, y * 2, w * 2, h * 2)


static func P(x: float, y: float) -> Vector2:
	return Vector2(x * 2, y * 2)


static func PP(pts: Array) -> PackedVector2Array:
	var out := PackedVector2Array()
	for p in pts:
		out.append(Vector2(p[0] * 2, p[1] * 2))
	return out


func current_bg() -> String:
	return bg


func _draw() -> void:
	var t := Art.tex("res://assets/backgrounds/%s.png" % current_bg())
	if t != null:
		var off := 0.0                                         # older 144-row rooms sit at the top of the 160-row picture area
		draw_rect(Rect2(0, 0, 640, 320), Color.BLACK)
		draw_texture_rect(t, Rect2(0, off, 640, t.get_height() * 2), false)
	else:
		draw_rect(Rect2(0, 0, 640, 320), Color.DARK_SLATE_GRAY)
	if OS.has_environment("HOTSPOTS"):   # debug overlay: hotspot rectangles and the walkable area
		for h in hotspots:
			draw_rect(h["rect"], Color(1, 1, 0, 0.9), false, 1.0)
			if h.has("approach"):
				draw_circle(h["approach"], 3, Color(1, 0, 0))
		draw_polyline(walk_poly + PackedVector2Array([walk_poly[0]]) if walk_poly.size() > 0 else walk_poly, Color(0, 1, 1, 0.8), 1.0)


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
