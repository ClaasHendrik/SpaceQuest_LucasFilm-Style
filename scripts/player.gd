extends Node2D
# Roger. 16x30 sprite frames drawn at 2x; origin at his feet.
# Sheet: 0-4 side (stand + 4 walk), 5-9 front, 10-14 back, 15-17 pick-up gesture (side). Left is the side view flipped.

const Art := preload("res://scripts/art.gd")
const FW := 16
const FH := 30
const FEET := 29          # feet baseline inside the frame

var walk_target := Vector2.ZERO
var walking := false
var speed := 130.0
var facing := "side"      # side, front or back
var flip := 1.0
var action := -1          # frame of the pick-up gesture, or -1
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
		if absf(to.y) > absf(to.x) * 1.3:
			facing = "front" if to.y > 0.0 else "back"
		else:
			facing = "side"
			if absf(to.x) > 1.0:
				flip = 1.0 if to.x > 0.0 else -1.0
	scale.x = flip if facing == "side" else 1.0
	queue_redraw()


# The reach-and-crouch gesture for picking something up (skipped in the fast test mode).
func reach() -> void:
	facing = "side"
	scale.x = flip
	for i in [0, 1, 2, 1]:
		action = i
		queue_redraw()
		await get_tree().create_timer(0.16).timeout
	action = -1
	queue_redraw()


func face(dir: String) -> void:
	facing = dir
	scale.x = flip if dir == "side" else 1.0
	queue_redraw()


func _draw() -> void:
	if _tex == null:
		return
	var base := 0
	if facing == "front":
		base = 5
	elif facing == "back":
		base = 10
	var frame := 0
	if walking:
		frame = 1 + int(_t * 7.0) % 4
	var idx := base + frame
	if action >= 0:
		idx = 15 + action
	draw_texture_rect_region(_tex, Rect2(-FW, -FEET * 2, FW * 2, FH * 2), Rect2(idx * FW, 0, FW, FH))
