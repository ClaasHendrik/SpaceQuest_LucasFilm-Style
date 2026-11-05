extends Node2D
# Roger. Placeholder figure drawn in code until real sprites exist.

var walk_target := Vector2.ZERO
var walking := false
var speed := 90.0


func _process(delta: float) -> void:
	if not walking:
		return
	var to := walk_target - position
	var step := speed * delta
	if to.length() <= step:
		position = walk_target
		walking = false
	else:
		position += to.normalized() * step
		if absf(to.x) > 1.0:
			scale.x = 1.0 if to.x > 0.0 else -1.0
	queue_redraw()


func _draw() -> void:
	# origin is at the feet
	var body := Color("f0f0f0")
	if GameState.flag("wearing_uniform"):
		body = Color("ff8c1a")
	draw_rect(Rect2(-5, -36, 10, 8), Color("e8b890"))   # head
	draw_rect(Rect2(-6, -28, 12, 16), body)              # torso
	draw_rect(Rect2(-6, -12, 5, 12), Color("e8b890"))    # legs
	draw_rect(Rect2(1, -12, 5, 12), Color("e8b890"))
