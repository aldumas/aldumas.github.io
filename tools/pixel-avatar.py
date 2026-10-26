#!/usr/bin/env python3
# Usage: python3 tools/pixel-avatar.py site/img   (needs Pillow)
# Draws Adam as a 42x32 pixel-art character giving a thumbs up, at 1 px per art pixel.
import sys
from PIL import Image
out = sys.argv[1]
N = 32
W = 42
C = {
	"K": "#2a1b1b", "s": "#f1b9a0", "S": "#dc9a80", "h": "#f9d3c0", "g": "#4a4a52", "G": "#8c8c94",
	"b": "#8a6450", "f": "#1f2433", "l": "#f4c4ae", "e": "#4a2c1c", "n": "#d98a74", "m": "#5a1a1a", "q": "#9a3d3d",
	"t": "#f4efe0", "r": "#c45a5a", "p": "#ea9c8a", "z": "#d6a08c", "R": "#8a2a35", "D": "#6a1e28",
	"C": "#561520", "y": "#b98f6c",
}
def draw(tilt):
	global g
	g = [["." for _ in range(W)] for _ in range(N)]
	body()
	thumbs_up()
	return g
def put(x, y, c):
	if 0 <= x < W and 0 <= y < N: g[y][x] = c
def body():
	# head mask: half-widths per row, centred between x 15 and 16
	half = {2: 5, 3: 6, 4: 7, 5: 7, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8,
		16: 8, 17: 8, 18: 7, 19: 7, 20: 6, 21: 5, 22: 4}
	head = {(x, y) for y, w in half.items() for x in range(16 - w, 16 + w)}
	# shirt, drawn first so the head sits on top
	for y in range(23, N):
		w = {23: 7, 24: 10, 25: 12}.get(y, 13)
		for x in range(16 - w, 16 + w):
			put(x, y, "D" if x in (16 - w + 1, 16 + w - 2) and y > 25 else "R")
		put(16 - w - 1, y, "K"); put(16 + w, y, "K")
	for x in range(9, 23): put(x, 22, "K")
	# neck and collar
	for y in (22, 23, 24):
		for x in range(13, 19): put(x, y, "S")
	for x in range(12, 20): put(x, 25, "C")
	put(11, 24, "C"); put(20, 24, "C"); put(12, 24, "C"); put(19, 24, "C")
	# faded shirt emblem: an arc with a peak
	for x, y in [(12, 30), (13, 29), (14, 28), (15, 28), (16, 28), (17, 28), (18, 29), (19, 30),
			(15, 30), (16, 30), (14, 31), (17, 31), (15, 29), (16, 29)]:
		if g[y][x] in "RD": put(x, y, "y")
	# head fill and outline
	for (x, y) in head:
		put(x, y, "s")
		if x >= 21: put(x, y, "S")
	for (x, y) in head:
		if any((x + dx, y + dy) not in head for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
			put(x, y, "K")
	for x in range(16 - 4, 16 + 4): put(x, 1, "K")
	for x, y in [(13, 4), (14, 4), (14, 3)]: put(x, y, "h")
	# ears
	for y in (12, 13, 14):
		put(7, y, "s"); put(24, y, "S"); put(6, y, "K"); put(25, y, "K")
	put(7, 11, "K"); put(7, 15, "K"); put(24, 11, "K"); put(24, 15, "K")
	# eyebrows
	for x, y in [(10, 10), (11, 9), (12, 9), (13, 10), (18, 10), (19, 9), (20, 9), (21, 10)]: put(x, y, "b")
	# glasses
	for x0 in (9, 17):
		for x in range(x0, x0 + 6):
			put(x, 11, "f"); put(x, 14, "f")
		for y in (12, 13):
			put(x0, y, "f"); put(x0 + 5, y, "f")
			for x in range(x0 + 1, x0 + 5): put(x, y, "l")
	put(15, 12, "f"); put(16, 12, "f"); put(8, 12, "f"); put(23, 12, "f")
	# smiling eyes
	for x in (11, 12, 19, 20): put(x, 12, "e")
	for x in (10, 13, 18, 21): put(x, 13, "e")
	# nose and cheeks
	put(15, 15, "n"); put(16, 15, "n"); put(14, 16, "n"); put(17, 16, "n"); put(16, 14, "S")
	for x, y in [(9, 15), (10, 15), (9, 16), (10, 16), (21, 15), (22, 15), (21, 16), (22, 16)]: put(x, y, "p")
	# warm smile, corners turned up
	put(11, 16, "n"); put(20, 16, "n")
	put(12, 17, "q"); put(19, 17, "q")
	for x in range(13, 19): put(x, 17, "t")
	put(13, 18, "q"); put(18, 18, "q")
	for x in range(14, 18): put(x, 18, "r")
	for x in range(14, 18): put(x, 19, "S")
	# stubble
	for (x, y) in head:
		if g[y][x] in "sS" and (y >= 19 or (y in (17, 18) and (x <= 10 or x >= 21))) and (x * 2 + y) % 3 == 0:
			put(x, y, "z")

def thumbs_up():
	"""A raised right arm giving a thumbs up: a fist with the thumb pointing up."""
	sleeve = {(x + (26 - y) // 3, y) for y in range(19, 27) for x in range(26, 31)}
	fore = {(x + (20 - y) // 4, y) for y in range(14, 21) for x in range(31, 34)}
	hx = 32
	fist = {(x, y) for y in range(8, 15) for x in range(hx - 2, hx + 4)}
	thumb = {(x, y) for y in range(3, 8) for x in (hx - 2, hx - 1)}
	skin = fore | fist | thumb
	shape = sleeve | skin
	for (x, y) in shape:
		if g[y][x] == ".":
			for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
				if (x + dx, y + dy) not in shape and 0 <= x + dx < W and 0 <= y + dy < N and g[y + dy][x + dx] == ".":
					put(x + dx, y + dy, "K")
	for (x, y) in sleeve: put(x, y, "R")
	for (x, y) in sleeve:
		if (x - 1, y) not in sleeve: put(x, y, "D")
	for (x, y) in skin: put(x, y, "s")
	for (x, y) in fore | thumb:
		if (x + 1, y) not in skin: put(x, y, "S")
	# the curled fingers, stacked down the front of the fist
	for y in (10, 12):
		for x in range(hx, hx + 4): put(x, y, "n")
	for y in range(8, 15): put(hx + 3, y, "S")
	put(hx - 1, 8, "S")

def render(grid):
	img = Image.new("RGBA", (W, N), (0, 0, 0, 0))
	px = img.load()
	for y in range(N):
		for x in range(W):
			c = grid[y][x]
			if c != ".":
				h = C[c]
				px[x, y] = tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
	return img

render(draw(0)).save(f"{out}/adam.png")
