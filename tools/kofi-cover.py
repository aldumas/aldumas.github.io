#!/usr/bin/env python3
# Usage: python3 tools/kofi-cover.py kofi   (needs Pillow)
# Draws the Ko-fi cover image: the site's night scene at 240x80, scaled 5x to 1200x400 (Ko-fi's 3:1).
# Draws the hero's pixel-art night scene and the grass-block strip, at 1 px per art pixel.
import random, sys
from PIL import Image
out = sys.argv[1]
r = random.Random(7)
W, H = 240, 80
GROUND = 56
im = Image.new("RGB", (W, H))
px = im.load()
def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
sky = ["#070b1f", "#0a1029", "#0d1533", "#111b3e", "#152249", "#1a2a55", "#1f3260"]
for y in range(GROUND):
	band = min(len(sky) - 1, y * len(sky) // GROUND)
	for x in range(W): px[x, y] = hexc(sky[band])
# stars
for _ in range(70):
	x, y = r.randrange(W), r.randrange(GROUND - 16)
	px[x, y] = hexc(r.choice(["#ffffff", "#cfd8ff", "#8fa0d8", "#8fa0d8"]))
# square moon with craters
mx, my = 176, 10
for y in range(12):
	for x in range(12):
		px[mx + x, my + y] = hexc("#e9ecd2")
for (x, y) in [(2, 3), (3, 3), (2, 4), (7, 6), (8, 6), (8, 7), (4, 8), (9, 2)]:
	px[mx + x, my + y] = hexc("#b9bda3")
# distant blocky hills
h = 0
x = 0
while x < W:
	h = max(3, min(14, h + r.choice([-3, -2, 0, 2, 3])))
	for xx in range(x, min(W, x + 6)):
		for y in range(GROUND - h, GROUND):
			px[xx, y] = hexc("#0e1a33" if y > GROUND - h + 1 else "#14223f")
	x += 6
# oak tree silhouettes
def tree(tx, th):
	for y in range(GROUND - th, GROUND):
		px[tx, y] = px[tx + 1, y] = hexc("#2a1d14")
	top = GROUND - th - 5
	for y in range(top, top + 7):
		inset = 1 if y in (top, top + 6) else 0
		for x in range(tx - 4 + inset, tx + 6 - inset):
			px[x, y] = hexc(r.choice(["#163d1c", "#1b4722", "#123318"]))
for tx, th in [(18, 6), (30, 8), (132, 7), (226, 6)]:
	tree(tx, th)
# grass, dirt, stone, deepslate with sculk
for x in range(W):
	for y in range(GROUND, H):
		d = y - GROUND
		if d < 2: c = r.choice(["#3f7424", "#4a8329", "#376a20"])
		elif d == 2: c = r.choice(["#467d26", "#6b4a2e", "#467d26"])
		elif d < 10: c = r.choice(["#6b4a2e", "#7a5636", "#5e4128", "#6b4a2e"])
		elif d < 14: c = r.choice(["#5e5e66", "#6a6a73", "#53535b"])
		else: c = r.choice(["#2b2b33", "#33333c", "#25252c"])
		px[x, y] = hexc(c)
# sculk veins in the deepslate
for _ in range(16):
	x, y = r.randrange(W), r.randrange(GROUND + 16, H)
	for _ in range(r.randrange(10, 26)):
		if 0 <= x < W and GROUND + 14 <= y < H:
			px[x, y] = hexc(r.choice(["#0b3a42", "#0f4a52", "#0b3a42"]))
			if r.random() < 0.12: px[x, y] = hexc("#29dfcb")
		x += r.choice([-1, 1, 1]); y += r.choice([-1, 0, 0, 1])
im.resize((W * 5, H * 5), Image.NEAREST).save(f"{out}/cover-1200x400.png", optimize=True)
