#!/usr/bin/env python3
"""Render the post-x video frames: prompt -> agent coding -> gameplay -> hold.
Mirrors game.html (Neon Breakout): same layout, colours and physics constants,
rescaled from the 960x540 canvas to the 1920x1080 video frame."""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

random.seed(20261123)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 30
BG = (7, 7, 15)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def F(size, bold=False):
    return ImageFont.truetype(MONOB if bold else MONO, size)

idx = 0
def save(img):
    global idx
    img.save(os.path.join(OUT, f"f{idx:04d}.png"))
    idx += 1

# ---------- Segment A: title + the one prompt (5.5s) ----------
PROMPT = "build me a tiny browser game: neon breakout,\none file, mouse paddle, bricks that burst. go."
for i in range(int(5.5 * FPS)):
    t = i / FPS
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((W // 2, 300), "ONE PROMPT.", font=F(92, True), fill=(125, 249, 255), anchor="mm")
    d.text((W // 2, 408), "ONE GAME.", font=F(92, True), fill=(232, 232, 255), anchor="mm")
    x0, y0, x1, y1 = 360, 540, 1560, 880
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(13, 13, 26), outline=(42, 42, 85), width=3)
    d.ellipse([x0 + 28, y0 + 24, x0 + 52, y0 + 48], fill=(255, 93, 143))
    d.ellipse([x0 + 68, y0 + 24, x0 + 92, y0 + 48], fill=(255, 179, 93))
    d.ellipse([x0 + 108, y0 + 24, x0 + 132, y0 + 48], fill=(93, 255, 143))
    typed = PROMPT[:max(0, int((t - 0.9) * 26))]
    for j, ln in enumerate(("you  >  " + typed).split("\n")):
        d.text((x0 + 40, y0 + 86 + j * 52), ln, font=F(36), fill=(232, 232, 255))
    if t > 0.9 + len(PROMPT) / 26 + 0.35:
        d.text((x0 + 40, y0 + 86 + 2 * 52 + 26), "agent >  on it. writing game.html ...",
               font=F(36), fill=(93, 255, 143))
    save(img)

# ---------- Segment B: the agent writing the real code (11s) ----------
code_lines = [ln.rstrip() for ln in open(os.path.join(HERE, "game.html"))]
code_lines = [ln for ln in code_lines if ln.strip()]
for i in range(int(11 * FPS)):
    t = i / FPS
    img = Image.new("RGB", (W, H), (10, 10, 20))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 64], fill=(16, 16, 32))
    d.text((28, 18), "game.html - agent is writing", font=F(28), fill=(160, 160, 200))
    d.text((W - 28, 18), f"{min(100, int(t / 11 * 100))}%", font=F(28),
           fill=(93, 255, 143), anchor="ra")
    shown = 6 + int(t / 11 * (len(code_lines) - 6))
    window = code_lines[max(0, shown - 21):shown]
    for j, ln in enumerate(window):
        col = (200, 200, 225) if j < len(window) - 1 else (125, 249, 255)
        d.text((40, 96 + j * 44), ln[:88], font=F(30), fill=col)
    save(img)

# ---------- Segment C: gameplay with the game's own physics (21s) ----------
COLORS = [(255, 93, 143), (255, 179, 93), (249, 248, 113),
          (93, 255, 143), (93, 200, 255), (200, 93, 255)]
ROWS, COLS, BW, BH, GAP, OX, OY = 6, 10, 86, 24, 8, 35, 64
K = 1.28                      # layout scale inside the video frame
GX, GY = 330, 150             # game area origin in the video frame
bricks = [[True] * COLS for _ in range(ROWS)]
paddle_w, paddle_x = 120.0, 420.0
ball = {"x": 480.0, "y": 496.0, "vx": 3.4, "vy": -5.2, "r": 9}
score, particles, trail = 0, [], []

def draw_game():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([300, 110, W - 300, H - 50], 16, fill=(11, 11, 24),
                        outline=(42, 42, 85), width=3)
    for r in range(ROWS):
        for c in range(COLS):
            if not bricks[r][c]:
                continue
            x = GX + (OX + c * (BW + GAP)) * K
            y = GY + (OY + r * (BH + GAP)) * K
            d.rounded_rectangle([x, y, x + BW * K, y + BH * K], 8, fill=COLORS[r])
    for k, tp in enumerate(trail):
        rr = ball["r"] * K * (k + 1) / max(1, len(trail))
        d.ellipse([GX + tp[0] * K - rr, GY + tp[1] * K - rr,
                   GX + tp[0] * K + rr, GY + tp[1] * K + rr], fill=(40, 90, 100))
    for p in particles:
        d.rectangle([GX + p["x"] * K - 4, GY + p["y"] * K - 4,
                     GX + p["x"] * K + 4, GY + p["y"] * K + 4], fill=p["color"])
    py = GY + (540 - 34) * K
    d.rounded_rectangle([GX + paddle_x * K, py, GX + (paddle_x + paddle_w) * K, py + 14 * K],
                        9, fill=(232, 232, 255))
    d.ellipse([GX + ball["x"] * K - 11, GY + ball["y"] * K - 11,
               GX + ball["x"] * K + 11, GY + ball["y"] * K + 11], fill=(255, 255, 255))
    d.text((GX + 16, GY + 8), f"SCORE {score}", font=F(30), fill=(232, 232, 255))
    d.text((GX + 944 * K, GY + 8), "LIVES 3", font=F(30), fill=(232, 232, 255), anchor="ra")
    return img

for i in range(int(21 * FPS)):
    target = ball["x"] - paddle_w / 2
    paddle_x += max(-11.0, min(11.0, (target - paddle_x) * 0.35))
    paddle_x = max(0.0, min(960 - paddle_w, paddle_x))
    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]
    if ball["x"] < ball["r"]:
        ball["x"] = ball["r"]; ball["vx"] *= -1
    if ball["x"] > 960 - ball["r"]:
        ball["x"] = 960 - ball["r"]; ball["vx"] *= -1
    if ball["y"] < ball["r"]:
        ball["y"] = ball["r"]; ball["vy"] *= -1
    if ball["y"] > 560:
        ball["y"] = 300; ball["vy"] = -abs(ball["vy"])
    if (ball["vy"] > 0 and ball["y"] + ball["r"] >= 506 and ball["y"] - ball["r"] <= 520
            and paddle_x <= ball["x"] <= paddle_x + paddle_w):
        tt = (ball["x"] - (paddle_x + paddle_w / 2)) / (paddle_w / 2)
        sp = math.hypot(ball["vx"], ball["vy"])
        a = -math.pi / 2 + tt * 1.05
        ball["vx"], ball["vy"] = sp * math.cos(a), sp * math.sin(a)
        ball["y"] = 506 - ball["r"] - 1
    hit = False
    for r in range(ROWS):
        for c in range(COLS):
            if not bricks[r][c]:
                continue
            bx, by = OX + c * (BW + GAP), OY + r * (BH + GAP)
            if (ball["x"] + ball["r"] > bx and ball["x"] - ball["r"] < bx + BW
                    and ball["y"] + ball["r"] > by and ball["y"] - ball["r"] < by + BH):
                bricks[r][c] = False
                score += 10
                ball["vy"] *= -1
                hit = True
                for _ in range(14):
                    a = random.random() * math.pi * 2
                    s = 1 + random.random() * 3.4
                    particles.append({"x": bx + BW / 2, "y": by + BH / 2,
                                      "vx": math.cos(a) * s, "vy": math.sin(a) * s - 0.6,
                                      "life": 30, "color": COLORS[r]})
                break
        if hit:
            break
    for p in particles:
        p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.12; p["life"] -= 1
    particles = [p for p in particles if p["life"] > 0]
    trail.append((ball["x"], ball["y"]))
    if len(trail) > 12:
        trail.pop(0)
    img = draw_game()
    if i < 60:
        d = ImageDraw.Draw(img)
        d.text((W // 2, 64), "...and it plays.", font=F(36, True),
               fill=(125, 249, 255), anchor="mm")
    save(img)

# ---------- Segment D: hold the last frame for the end card (2.5s) ----------
hold = draw_game()
for _ in range(int(2.5 * FPS)):
    save(hold.copy())

print("frames:", idx, "seconds:", idx / FPS)
