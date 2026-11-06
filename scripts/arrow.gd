extends Button
# Small blue scroll triangle for the inventory (like the original interface).

var up := true


func _ready() -> void:
	flat = true
	focus_mode = Control.FOCUS_NONE


func _draw() -> void:
	var w := size.x
	var h := size.y
	var pts := PackedVector2Array([Vector2(w / 2, 1), Vector2(w - 1, h - 1), Vector2(1, h - 1), Vector2(w / 2, 1)])
	if not up:
		pts = PackedVector2Array([Vector2(w / 2, h - 1), Vector2(w - 1, 1), Vector2(1, 1), Vector2(w / 2, h - 1)])
	draw_polyline(pts, Color("5555ff") if not is_hovered() else Color("aaaaff"), 2.0)
