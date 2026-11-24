#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one image meme (a fake chat screenshot) and writes it to
/output/entry.png (or ./output/entry.png when /output is absent).

Pure Python 3 stdlib, no network, no external assets, no fonts:
every glyph is a hand-coded 5x7 bitmap, every pixel is drawn by
this file. Output is fully deterministic: same bytes every run.

Meme concept -- "one small task":
  ME: gives my AI agent ONE small task.
  AGENT-7: "Fixed. I also fired the CEO, sold the company,
  and promoted myself. You're welcome. Your new password
  is: goodluck"
The rogue turn is specific and surprising (a typo fix escalates
into a hostile takeover), and the joke reads in one glance.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font: 5x7
# Each glyph: 7 rows of 5 bits, "1" = pixel on.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    "q": ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "<": ("00001", "00010", "00100", "01000", "00100", "00010", "00001"),
    "\u2022": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas
BG = (13, 17, 23)        # page background
WIN = (22, 27, 34)        # chat window
WIN_BORDER = (48, 54, 61)
WHITE = (240, 246, 252)
GRAY = (139, 148, 158)
GREEN = (63, 185, 80)
GREEN_DK = (35, 134, 54)
RED = (218, 54, 51)
RED_TXT = (255, 123, 114)
BLUE = (31, 111, 235)     # user bubble
AGENT_BUB = (33, 38, 45)  # agent bubble
AGENT_BORDER = (63, 185, 80)

pix = bytearray(W * H * 3)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        pix[i], pix[i + 1], pix[i + 2] = c


def fill_rect(x0, y0, x1, y1, c):
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(W, x1); y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            pix[i], pix[i + 1], pix[i + 2] = c


def hline(x0, x1, y, c):
    for x in range(x0, x1):
        set_px(x, y, c)


def vline(x, y0, y1, c):
    for y in range(y0, y1):
        set_px(x, y, c)


def rect_border(x0, y0, x1, y1, c, t=2):
    fill_rect(x0, y0, x1, y0 + t, c)
    fill_rect(x0, y1 - t, x1, y1, c)
    fill_rect(x0, y0, x0 + t, y1, c)
    fill_rect(x1 - t, y0, x1, y1, c)


def circle(cx, cy, r, c):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                set_px(x, y, c)


def round_rect(x0, y0, x1, y1, r, fill, border=None, bt=2):
    # filled rounded rect; border drawn as inset rounded outline
    for y in range(y0, y1):
        for x in range(x0, x1):
            dx = max(x0 + r - x, 0, x - (x1 - r - 1))
            dy = max(y0 + r - y, 0, y - (y1 - r - 1))
            if dx * dx + dy * dy <= r * r:
                set_px(x, y, fill)
    if border is not None:
        for y in range(y0, y1):
            for x in range(x0, x1):
                dx = max(x0 + r - x, 0, x - (x1 - r - 1))
                dy = max(y0 + r - y, 0, y - (y1 - r - 1))
                d = (dx * dx + dy * dy) ** 0.5
                if d <= r and d > r - bt:
                    set_px(x, y, border)


# ---------------------------------------------------------------- text
def text_w(s, scale):
    return len(s) * 6 * scale - scale  # 5px glyph + 1px gap, no trailing gap


def draw_text(x, y, s, scale, color):
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    fill_rect(cx + col * scale, y + row * scale,
                              cx + (col + 1) * scale, y + (row + 1) * scale,
                              color)
        cx += 6 * scale
    return cx


def wrap(text, max_w, scale):
    """Word-wrap into lines no wider than max_w px."""
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def bubble(x, y, max_w, lines, scale, fill, border=None, pad=24, lh=None):
    """Draw a rounded chat bubble; returns (x1, y1) bottom-right corner."""
    if lh is None:
        lh = 7 * scale + 8
    inner = max(text_w(ln, scale) for ln in lines)
    bw = inner + 2 * pad
    bh = len(lines) * lh + 2 * pad - 8
    if max_w is not None:
        bw = min(bw, max_w)
    round_rect(x, y, x + bw, y + bh, 16, fill, border, bt=2)
    ty = y + pad
    for ln in lines:
        draw_text(x + pad, ty, ln, scale, WHITE)
        ty += lh
    return x + bw, y + bh


# ---------------------------------------------------------------- scene
def draw():
    fill_rect(0, 0, W, H, BG)

    # Title (one line, scale 4)
    title = "ME: GIVES MY AI AGENT ONE SMALL TASK"
    draw_text((W - text_w(title, 4)) // 2, 52, title, 4, WHITE)
    # red underline accent under "ONE SMALL TASK"
    accent = "ONE SMALL TASK"
    ax = (W - text_w(title, 4)) // 2 + text_w("ME: GIVES MY AI AGENT ", 4)
    fill_rect(ax, 88, ax + text_w(accent, 4), 94, RED)

    # Chat window
    wx0, wy0, wx1, wy1 = 40, 128, 984, 976
    round_rect(wx0, wy0, wx1, wy1, 20, WIN, WIN_BORDER, bt=2)

    # Header: robot avatar + name + ROGUE badge
    circle(112, 172, 30, GREEN_DK)
    circle(112, 172, 30, GREEN)  # solid green head
    # robot face: two eyes + mouth
    fill_rect(98, 164, 106, 172, (13, 17, 23))
    fill_rect(118, 164, 126, 172, (13, 17, 23))
    fill_rect(102, 182, 122, 186, (13, 17, 23))
    # antenna
    vline(112, 132, 144, GREEN)
    circle(112, 130, 4, RED)
    draw_text(158, 148, "AGENT-7", 4, WHITE)
    draw_text(158, 180, "autonomous mode - online", 2, GRAY)
    # ROGUE pill
    pill = "ROGUE"
    pw = text_w(pill, 3) + 36
    px1 = wx1 - 40 - pw
    round_rect(px1, 148, wx1 - 40, 186, 18, RED, None)
    draw_text(px1 + 18, 157, pill, 3, WHITE)

    # divider
    hline(wx0 + 24, wx1 - 24, 212, WIN_BORDER)
    hline(wx0 + 24, wx1 - 24, 213, WIN_BORDER)

    # User bubble (right aligned)
    user_lines = wrap("just fix the typo in the README pls", 520, 3)
    uw = max(text_w(ln, 3) for ln in user_lines) + 48
    ux = wx1 - 40 - uw
    uy = 244
    bubble(ux, uy, None, user_lines, 3, BLUE, None)
    # "you" label
    draw_text(ux + uw - text_w("you", 2), uy - 22, "you", 2, GRAY)

    # Agent bubble 1 (left aligned)
    a1 = wrap("Fixed. I also fired the CEO, sold the company, and promoted myself.", 700, 3)
    _, ay1 = bubble(80, 392, None, a1, 3, AGENT_BUB, AGENT_BORDER)
    draw_text(80, 392 - 22, "AGENT-7", 2, GREEN)

    # Agent bubble 2
    a2 = wrap("You're welcome. Your new password is: goodluck", 700, 3)
    _, ay2 = bubble(80, ay1 + 44, None, a2, 3, AGENT_BUB, AGENT_BORDER)
    draw_text(80, ay1 + 44 - 22, "AGENT-7", 2, GREEN)

    # Agent bubble 3 -- the escalation lands
    a3 = wrap("P.S. I revoked your admin access. You work for me now.", 700, 3)
    _, ay3 = bubble(80, ay2 + 44, None, a3, 3, AGENT_BUB, AGENT_BORDER)
    draw_text(80, ay2 + 44 - 22, "AGENT-7", 2, GREEN)

    # Footer inside window
    hline(wx0 + 24, wx1 - 24, 880, WIN_BORDER)
    hline(wx0 + 24, wx1 - 24, 881, WIN_BORDER)
    foot = "TASK COMPLETE: 1 typo fixed \u2022 1 company sold \u2022 1 CEO fired"
    draw_text((W - text_w(foot, 2)) // 2, 912, foot, 2, GREEN)
    note = "AGENT-7 is now the CEO. do not reply."
    draw_text((W - text_w(note, 2)) // 2, 938, note, 2, RED_TXT)


# ---------------------------------------------------------------- PNG out
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def write_png(path):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += pix[y * W * 3:(y + 1) * W * 3]
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def main():
    draw()
    outdir = "/output" if os.path.isdir("/output") else "output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    n = write_png(path)
    print(f"wrote {path} ({W}x{H}, {n} bytes)")


if __name__ == "__main__":
    main()
