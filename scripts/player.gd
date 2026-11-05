extends Node2D
# Roger. 14x28 sprite frames drawn at 2x; origin at his feet.

const Art := preload("res://scripts/art.gd")
const FW := 14
const FH := 28

var walk_target := Vector2.ZERO
var walking := false
var speed := 110.0
var _t := 0.0
var _tex: Texture2D


func _ready() -> void:
	_tex = Art.tex("res://assets/sprites/roger.png")


func _process(delta: float) -> void:
	if not walking:
		return
	_t += delta
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
	if _tex == null:
		return
	var outfit := 1 if GameState.flag("wearing_uniform") else 0
	var frame := 0
	if walking:
		frame = 1 + int(_t * 8.0) % 2
	draw_texture_rect_region(_tex, Rect2(-FW, -FH * 2, FW * 2, FH * 2), Rect2((outfit * 3 + frame) * FW, 0, FW, FH))
