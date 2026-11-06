"""Builds docs/room_gallery.pdf from in-game screenshots.
Usage: python3 tools/make_gallery.py <shots_dir>   (shots made by tests/shot.gd)"""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit
from PIL import Image

SHOTS = sys.argv[1]
ART = "assets/backgrounds/"
PAGE_W, PAGE_H = A4
M = 15 * mm
rooms = json.load(open("data/rooms.json"))
byid = {r["id"]: r for r in rooms}
# scripted rooms live in GDScript; describe them here
byid["escape_pod"] = {"id": "escape_pod", "title": "Escape Pod", "act": 1, "hotspots": [
    {"name": "cryo-chamber"}, {"name": "wall locker"}, {"name": "uniform (after opening locker)"},
    {"name": "airlock hatch", "exit": {"room": "garbage_mountain"}}]}
byid["garbage_mountain"] = {"id": "garbage_mountain", "title": "Garbage Mountain", "act": 1, "hotspots": [
    {"name": "escape pod", "exit": {"room": "escape_pod"}}, {"name": "wire"}, {"name": "junk heap"},
    {"name": "wrecked starfighter"}, {"name": "path east", "exit": {"room": "robot_head"}},
    {"name": "way south", "exit": {"room": "conveyor"}}]}
order = ["escape_pod", "garbage_mountain"] + [r["id"] for r in rooms]
ACTS = {1: "Act 1: The Garbage Freighter", 2: "Act 2: Phleebhut", 3: "Act 3: Monolith Burger",
        4: "Act 4: Ortega", 5: "Act 5: Pestulon (ScumSoft)"}
NOTES = {
    "nav_screen": "Navigation computer. 'Set course' cycles Phleebhut, Monolith Burger, Ortega, Pestulon; the launch lever in the cockpit flies there.",
    "cockpit": "Launch lever flies to the course chosen on the navigation computer.",
    "astro_chicken": "Arcade screen. The minigame itself is not built yet.",
    "space_battle": "Space battle screen. The shield-management minigame is not built yet.",
    "deep_space": "Ending screen.",
}

c = canvas.Canvas("docs/room_gallery.pdf", pagesize=A4)
c.setTitle("Space Quest III (LucasFilm-style) - Room Gallery")


def footer(n):
    c.setFont("Helvetica", 8)
    c.setFillGray(0.45)
    c.drawString(M, 8 * mm, "Space Quest III, LucasFilm-style remake - room gallery (painted placeholder art, work in progress)")
    c.drawRightString(PAGE_W - M, 8 * mm, str(n))
    c.setFillGray(0)


def wrap(text, font, size, width):
    return simpleSplit(text, font, size, width)


# ---- cover / overview
page = 1
c.setFont("Helvetica-Bold", 22)
c.drawString(M, PAGE_H - 30 * mm, "Space Quest III - LucasFilm-style remake")
c.setFont("Helvetica", 13)
c.drawString(M, PAGE_H - 38 * mm, "Room gallery: every area in the game as it appears on screen")
y = PAGE_H - 52 * mm
intro = ("Each screenshot is taken from the running game: the 640x480 view with the speech strip on top and the verb grid and "
         "inventory underneath, in the style of the Lucasfilm Games interface. The scenes are painted at 320x144 pixels with "
         "gradients, lighting and texture, reduced to a 190-colour palette and shown at 2x. Each planet has its own palette. "
         "It is a draft to work from, not final art: some rooms (the escape pod, the garbage mountain) are more finished than others "
         "(the hangar, the cell block). Roger is a placeholder sprite. Objects listed under each screen can be examined in the game; "
         "exits lead to the rooms named.")
for ln in wrap(intro, "Helvetica", 10, PAGE_W - 2 * M):
    c.setFont("Helvetica", 10)
    c.drawString(M, y, ln)
    y -= 5 * mm
y -= 4 * mm
c.setFont("Helvetica-Bold", 12)
c.drawString(M, y, "Contents (%d screens)" % len(order))
y -= 7 * mm
for act in range(1, 6):
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, ACTS[act])
    y -= 5 * mm
    names = [byid[i]["title"] for i in order if byid[i]["act"] == act]
    for ln in wrap(", ".join(names) + ".", "Helvetica", 9, PAGE_W - 2 * M - 8 * mm):
        c.setFont("Helvetica", 9)
        c.drawString(M + 5 * mm, y, ln)
        y -= 4.4 * mm
    y -= 3 * mm
y -= 2 * mm
c.setFont("Helvetica-Bold", 10)
c.drawString(M, y, "Not shown / not yet built")
y -= 5 * mm
todo = ("Puzzles beyond the first two rooms, dialogue, sound, the Astro Chicken and space-battle minigames, "
        "and the death scenes. Walking and examining work everywhere. In the game, F2 / F3 jump to the previous / next room.")
for ln in wrap(todo, "Helvetica", 9, PAGE_W - 2 * M):
    c.setFont("Helvetica", 9)
    c.drawString(M, y, ln)
    y -= 4.4 * mm
footer(page)
c.showPage()
page += 1

# ---- rooms, two per page
IMG_W = (PAGE_W - 2 * M) * 0.74
IMG_H = IMG_W * 960 / 1280
slot_h = (PAGE_H - 2 * M - 8 * mm) / 2


def draw_room(rid, top):
    r = byid[rid]
    y = top
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y - 4 * mm, "%s  -  %s" % (ACTS[r["act"]].split(":")[0], r["title"]))
    y -= 7 * mm
    path = os.path.join(SHOTS, rid + ".png")
    c.drawImage(ImageReader(path), M, y - IMG_H, IMG_W, IMG_H)
    c.setStrokeGray(0.6)
    c.rect(M, y - IMG_H, IMG_W, IMG_H)
    y -= IMG_H + 4.5 * mm
    names = [h["name"] for h in r["hotspots"] if not h.get("exit")]
    exits = ["%s (to %s)" % (h["name"], byid[h["exit"]["room"]]["title"]) for h in r["hotspots"] if h.get("exit")]
    lines = []
    if names:
        lines.append(("Objects: ", ", ".join(names)))
    if exits:
        lines.append(("Exits: ", "; ".join(exits)))
    if rid in NOTES:
        lines.append(("Note: ", NOTES[rid]))
    for label, text in lines:
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(M, y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 8.5)
        wrapped = wrap(text, "Helvetica", 8.5, (PAGE_W - 2 * M) - lw)
        for i, ln in enumerate(wrapped):
            c.setFont("Helvetica", 8.5)
            c.drawString(M + lw, y, ln)
            y -= 3.8 * mm
        if not wrapped:
            y -= 3.8 * mm


i = 0
while i < len(order):
    for slot in range(2):
        if i >= len(order):
            break
        draw_room(order[i], PAGE_H - M - slot * slot_h)
        i += 1
    footer(page)
    c.showPage()
    page += 1

# ---- variants page: art states that change during play
c.setFont("Helvetica-Bold", 14)
c.drawString(M, PAGE_H - 25 * mm, "Room variants (the art changes as you play)")
variants = [("escape_pod_open", "Escape pod: locker opened, uniform inside"),
            ("escape_pod_open_empty", "Escape pod: locker opened, uniform taken"),
            ("garbage_mountain_nowire", "Garbage mountain: wire taken")]
y = PAGE_H - 35 * mm
vw = (PAGE_W - 2 * M) * 0.85
vh = vw * 144 / 320
for name, cap in variants:
    c.drawImage(ImageReader(Image.open(ART + name + ".png").resize((960, 432), Image.NEAREST)), M, y - vh, vw, vh)
    c.rect(M, y - vh, vw, vh)
    c.setFont("Helvetica", 9)
    c.drawString(M, y - vh - 4.5 * mm, cap)
    y -= vh + 14 * mm
footer(page)
c.showPage()
c.save()
print("pages:", page)
