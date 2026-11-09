"""Builds docs/act1_walkthrough.pdf: the Act 1 route with points, plus sample screens.
Usage: python3 tools/make_act1_pdf.py <shots_dir>   (shots from tests/shot_act1.gd)"""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit

SH = sys.argv[1]
PW, PH = A4
M = 15 * mm
IW = PW - 2 * M
pts = {e["id"]: e for e in json.load(open("data/points.json"))}
c = canvas.Canvas("docs/act1_walkthrough.pdf", pagesize=A4)
c.setTitle("Space Quest III (LucasFilm-style) - Act 1")


def footer(n):
    c.setFont("Helvetica", 8)
    c.setFillGray(0.45)
    c.drawString(M, 8 * mm, "Space Quest III, LucasFilm-style remake - Act 1: The Garbage Freighter")
    c.drawRightString(PW - M, 8 * mm, str(n))
    c.setFillGray(0)


def para(text, y, size=9.5, font="Helvetica", width=IW, lead=4.6, x=M):
    for ln in simpleSplit(text, font, size, width):
        c.setFont(font, size)
        c.drawString(x, y, ln)
        y -= lead * mm
    return y


STEPS = [
    ("Escape pod (the script's opening)", "Open the locker, take the pod manual (it says: engines first, radar before takeoff, front shields before firing). Open the hatch.", []),
    ("Crash site and the tube", "East to the tube entrance, through the middle arch into the tube. Pick up the hanging wires.", ["wire"]),
    ("Robot head", "East to the robot head. Use the broken eye to climb up to the shuttle. Look at it, note the open panel, climb down the ladder. Do not step into the chasm.", ["robot_eye"]),
    ("Junk field and lift tower", "Back to the crash site, south, east. Use the lift tower: the bucket carries you up to the conveyor.", ["trash_bucket"]),
    ("Conveyor (timed)", "The belt carries you to the shredder. Use the rail overhead to jump before it arrives.", ["jump_rail"]),
    ("Rail and the grabber", "Walk west along the rail to the tower; Use the grabber. In the claw view click along the yard: Push the warp motivator (white drum) to lift it, move over the shuttle's open panel and Push again. Walk off at the platform, then Use the blue chute.", ["grab_motivator", "install_motivator", "fall_chute"]),
    ("Dark room (rats on a timer)", "Pick up the reactor from the hole. Climb the ladder to the tube entrance. In the tube the rat steals the reactor and the wire: go back down for both, then pick up the ladder at the tube entrance.", ["get_reactor", "get_ladder"]),
    ("Shuttle yard", "Climb the robot's eye again. Use the ladder with the shuttle, open the top hatch, use the reactor and the wire on the power panel, then go through the hatch.", ["ladder_ship_top", "open_hatch", "install_reactor", "install_wire"]),
    ("Cockpit", "Use the seat for the buckazoids. Use the computer: Engines, Radar, Takeoff; then Weapons and Front shields, Fire.", ["search_cushion", "escape_freighter"]),
]

y = PH - 25 * mm
c.setFont("Helvetica-Bold", 20)
c.drawString(M, y, "Act 1: The Garbage Freighter")
y -= 8 * mm
c.setFont("Helvetica", 11)
c.drawString(M, y, "Route, points and screens on the original layout. Playable from the first screen to the escape.")
y -= 10 * mm
total = 0
for room, text, ev in STEPS:
    c.setFont("Helvetica-Bold", 10)
    p_ = sum(pts[e]["points"] for e in ev)
    total += p_
    c.drawString(M, y, room + ("   (%d points)" % p_ if p_ else ""))
    y -= 4.6 * mm
    y = para(text, y, x=M + 4 * mm, width=IW - 4 * mm)
    for e in ev:
        c.setFont("Helvetica-Oblique", 8.5)
        c.setFillGray(0.35)
        c.drawString(M + 8 * mm, y, "+%d  %s" % (pts[e]["points"], pts[e]["description"]))
        c.setFillGray(0)
        y -= 4.0 * mm
    y -= 2.5 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y - 2 * mm, "Act 1 total: %d points (of 738)" % total)
y -= 9 * mm
y = para("Deaths in this act, each with its own painted picture: the chasm, the metal plate, the shredder (too slow), stepping off the rail, "
         "the rat (too slow), taking off without radar, switching the engines off in flight, and firing without front shields. "
         "The game checks the whole route from the first screen to the escape: all 15 events, exactly 145 points.", y, 9)
footer(1)
c.showPage()

ROOMS14 = ["crash_site", "tube_entrance", "wire_tube", "robot_head", "yard", "yard_ladder", "junk_field", "junk_tower", "conveyor", "rail_west", "rail_window", "rail_tower", "dark_room", "cockpit"]
TITLES = {"crash_site": "Crash site", "tube_entrance": "Tube entrance", "wire_tube": "Inside the tube", "robot_head": "The robot head", "yard": "On top of the head",
          "yard_ladder": "With the ladder", "junk_field": "Junk field", "junk_tower": "The lift tower", "conveyor": "The conveyor", "rail_west": "On the rail",
          "rail_window": "The rail by the window", "rail_tower": "The rail tower", "dark_room": "The dark room (rats)", "cockpit": "The cockpit"}
SHOTS = [(r + ".png", TITLES[r]) for r in ROOMS14]
hw = (IW - 6 * mm) / 2
hh = hw * 960 / 1280
n = 2
for page in range((len(SHOTS) + 3) // 4):
    y = PH - 20 * mm
    for row in range(2):
        for col in range(2):
            k = page * 4 + row * 2 + col
            if k >= len(SHOTS):
                continue
            name, cap = SHOTS[k]
            x = M + col * (hw + 6 * mm)
            c.drawImage(ImageReader(os.path.join(SH, name)), x, y - hh, hw, hh)
            c.setStrokeGray(0.5)
            c.rect(x, y - hh, hw, hh)
            c.setFont("Helvetica-Oblique", 8)
            for i, ln in enumerate(simpleSplit(cap, "Helvetica-Oblique", 8, hw)):
                c.drawString(x, y - hh - (4 + 3.6 * i) * mm, ln)
        y -= hh + 16 * mm
    footer(n)
    c.showPage()
    n += 1
c.save()
print("ok")
