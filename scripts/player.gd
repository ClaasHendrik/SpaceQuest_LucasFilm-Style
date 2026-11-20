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
var mode := ""            # "", "climb" or "fall"
var talking := false      # mouth flaps while Roger speaks
var fast := false
var _t := 0.0
var _tex: Texture2D


func _ready() -> void:
	_tex = Art.tex("res://assets/sprites/roger.png")


func _process(delta: float) -> void:
	if talking or mode != "":
		_t += delta
		queue_redraw()
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


# Climb straight up or down by dy pixels (negative = up) over secs seconds, hands and feet alternating.
func climb(dy: float, secs: float) -> void:
	mode = "climb"
	var y0 := position.y
	var t := 0.0
	var dur := 0.02 if fast else secs
	while t < dur:
		await get_tree().process_frame
		t += get_process_delta_time()
		position.y = y0 + dy * minf(t / dur, 1.0)
	mode = ""
	queue_redraw()


# Fall by dy pixels, accelerating, arms up and screaming; stays in the pose afterwards.
func fall(dy: float) -> void:
	mode = "fall"
	var y0 := position.y
	var t := 0.0
	var dur := 0.02 if fast else 0.9
	while t < dur:
		await get_tree().process_frame
		t += get_process_delta_time()
		var k := minf(t / dur, 1.0)
		position.y = y0 + dy * k * k
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
	elif mode == "climb":
		idx = 18 + int(_t * 6.0) % 4
	elif mode == "fall":
		idx = 22 + int(_t * 8.0) % 2
	elif talking and not walking and int(_t * 7.0) % 2 == 0:
		idx = 25 if facing == "front" else (24 if facing == "side" else idx)
	draw_texture_rect_region(_tex, Rect2(-FW, -FEET * 2, FW * 2, FH * 2), Rect2(idx * FW, 0, FW, FH))
