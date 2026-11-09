"""Synthesises the sound effects into assets/sfx/*.wav (22050 Hz, mono, 16 bit). Period flavour: square and triangle waves,
short envelopes, arpeggios. Usage: python3 tools/make_sfx.py"""
import wave
import numpy as np

SR = 22050


def tone(freq, dur, kind="square", vol=0.5, glide=None, decay=3.0):
    t = np.arange(int(SR * dur)) / SR
    f = freq if glide is None else np.linspace(freq, glide, len(t))
    ph = np.cumsum(2 * np.pi * f / SR) if glide is not None else 2 * np.pi * freq * t
    if kind == "square":
        w = np.sign(np.sin(ph))
    elif kind == "tri":
        w = 2 / np.pi * np.arcsin(np.sin(ph))
    elif kind == "noise":
        w = np.random.default_rng(3).uniform(-1, 1, len(t))
    else:
        w = np.sin(ph)
    env = np.minimum(1.0, t * 400) * np.exp(-decay * t / dur)
    return w * env * vol


def seq(*parts):
    return np.concatenate(parts)


def save(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(f"assets/sfx/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32000).astype(np.int16).tobytes())


# the Sierra-style score blip: three rising notes
save("points", seq(tone(660, 0.07), tone(880, 0.07), tone(1320, 0.14, decay=2.0)))
save("pickup", seq(tone(520, 0.06, "tri"), tone(780, 0.10, "tri", decay=2.5)))
save("click", tone(300, 0.05, "square", 0.4, decay=6.0))
save("lift", seq(tone(70, 0.5, "tri", 0.6, glide=140, decay=1.0), tone(140, 0.5, "tri", 0.5, glide=220, decay=1.0)))
save("takeoff", tone(90, 1.8, "square", 0.45, glide=900, decay=0.8) * 0.8 + tone(60, 1.8, "noise", 0.12, decay=0.6))
save("blast", seq(tone(200, 0.25, "noise", 0.6, decay=4.0), tone(900, 0.5, "square", 0.4, glide=90, decay=3.0)))
save("jingle_death", seq(tone(392, 0.18, "tri"), tone(370, 0.18, "tri"), tone(349, 0.18, "tri"), tone(330, 0.5, "tri", decay=1.5), tone(220, 0.7, "tri", 0.5, decay=1.2)))
save("no", seq(tone(180, 0.08, "square", 0.4), tone(140, 0.14, "square", 0.4)))
save("squeak", seq(tone(1700, 0.05, "tri", 0.4, glide=2400), tone(2000, 0.04, "tri", 0.3, glide=1500)))
save("steal", seq(tone(900, 0.06, "square", 0.3, glide=300), tone(1200, 0.05, "tri", 0.3, glide=2000)))
print("sfx written")
