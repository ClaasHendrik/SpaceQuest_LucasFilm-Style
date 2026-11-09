extends Node
# Sound effects. Registered as the autoload "Sfx". The wav files are read directly, so they work without an editor import.

const NAMES := ["points", "pickup", "click", "lift", "takeoff", "blast", "jingle_death", "no", "squeak", "steal"]
var _streams: Dictionary = {}
var _players: Array = []
var muted := false


func _ready() -> void:
	for n in NAMES:
		var path := "res://assets/sfx/%s.wav" % n
		var bytes := FileAccess.get_file_as_bytes(path)
		if bytes.size() > 44:
			var s := AudioStreamWAV.new()
			s.format = AudioStreamWAV.FORMAT_16_BITS
			s.mix_rate = 22050
			s.stereo = false
			s.data = bytes.slice(44)
			_streams[n] = s
	for i in 4:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_players.append(p)


func play(name: String) -> void:
	if muted or not _streams.has(name):
		return
	for p in _players:
		if not p.playing:
			p.stream = _streams[name]
			p.play()
			return
	_players[0].stream = _streams[name]
	_players[0].play()
