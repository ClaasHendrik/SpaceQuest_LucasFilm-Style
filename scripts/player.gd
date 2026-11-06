extends Node2D
# Roger. 28x52 sprite frames (stand + 4 walk frames per outfit), drawn at 2x; origin at his feet.

const Art := preload("res://scripts/art.gd")
const FW := 28
const FH := 52
const FEET := 50          # feet baseline inside the frame

var walk_target := Vector2.ZERO
var walking := false
var speed := 130.0
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
		frame = 1 + int(_t * 7.0) % 4
	var src := Rect2((outfit * 5 + frame) * FW, 0, FW, FH)
	draw_texture_rect_region(_tex, Rect2(-FW, -FEET * 2, FW * 2, FH * 2), src)
