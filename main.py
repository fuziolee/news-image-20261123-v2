#!/usr/bin/env python3
"""The World in One Day -- Monday, 23 November 2026. (v2 rescue prebuild)
make.fun bounty news-image-20261123 entry renderer.
STDLIB ONLY (zlib + struct). Deterministic: no timestamps, no randomness.
Writes entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR (default /output).
37 stories: 4 heroes + 12 smalls + 21 best one-liners across 7 regions.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font (5x7)
# Each glyph: 7 rows, 5 bits each (bit 4 = leftmost column).
F = {}

def _g(ch, rows):
    F[ch] = tuple(rows)

# Uppercase
_g("A", (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11))
_g("B", (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E))
_g("C", (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E))
_g("D", (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E))
_g("E", (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F))
_g("F", (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10))
_g("G", (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F))
_g("H", (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11))
_g("I", (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E))
_g("J", (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C))
_g("K", (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11))
_g("L", (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F))
_g("M", (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11))
_g("N", (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11))
_g("O", (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E))
_g("P", (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10))
_g("Q", (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D))
_g("R", (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11))
_g("S", (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E))
_g("T", (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04))
_g("U", (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E))
_g("V", (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04))
_g("W", (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11))
_g("X", (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11))
_g("Y", (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04))
_g("Z", (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F))
# Digits
_g("0", (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E))
_g("1", (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E))
_g("2", (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F))
_g("3", (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E))
_g("4", (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02))
_g("5", (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E))
_g("6", (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E))
_g("7", (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08))
_g("8", (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E))
_g("9", (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C))
# Lowercase
_g("a", (0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F))
_g("b", (0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x1E))
_g("c", (0x00, 0x00, 0x0E, 0x10, 0x10, 0x11, 0x0E))
_g("d", (0x01, 0x01, 0x0D, 0x13, 0x11, 0x11, 0x0F))
_g("e", (0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E))
_g("f", (0x06, 0x08, 0x1E, 0x08, 0x08, 0x08, 0x08))
_g("g", (0x00, 0x0F, 0x11, 0x11, 0x0F, 0x10, 0x0E))  # tail hooks LEFT, distinct from digit 9
_g("h", (0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x11))
_g("i", (0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E))
_g("j", (0x02, 0x00, 0x06, 0x02, 0x02, 0x12, 0x0C))
_g("k", (0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12))
_g("l", (0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E))
_g("m", (0x00, 0x00, 0x1A, 0x15, 0x15, 0x15, 0x15))
_g("n", (0x00, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11))
_g("\u00f1", (0x0A, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11))  # ñ
_g("o", (0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E))
_g("p", (0x00, 0x00, 0x1E, 0x11, 0x1E, 0x10, 0x10))
_g("q", (0x00, 0x00, 0x0D, 0x13, 0x0F, 0x01, 0x01))
_g("r", (0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10))
_g("s", (0x00, 0x00, 0x0F, 0x10, 0x0E, 0x01, 0x1E))
_g("t", (0x04, 0x04, 0x1F, 0x04, 0x04, 0x05, 0x06))
_g("u", (0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D))
_g("v", (0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04))
_g("w", (0x00, 0x00, 0x11, 0x15, 0x15, 0x15, 0x0A))
_g("x", (0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11))
_g("y", (0x00, 0x00, 0x11, 0x11, 0x0F, 0x01, 0x0E))
_g("z", (0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F))
# Punctuation / symbols
_g(" ", (0, 0, 0, 0, 0, 0, 0))
_g(".", (0, 0, 0, 0, 0, 0x0C, 0x0C))
_g(",", (0, 0, 0, 0, 0x0C, 0x04, 0x08))
_g("!", (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04))
_g("?", (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04))
_g("'", (0x04, 0x04, 0x08, 0, 0, 0, 0))
_g('"', (0x0A, 0x0A, 0x0A, 0, 0, 0, 0))
_g("-", (0, 0, 0, 0x0E, 0, 0, 0))
_g("\u2013", (0, 0, 0, 0x0E, 0, 0, 0))          # en dash
_g("\u2014", (0, 0, 0, 0x1F, 0, 0, 0))          # em dash
_g("\u00b7", (0, 0, 0, 0x0C, 0x0C, 0, 0))       # middle dot
_g("\u2022", (0x04, 0x0E, 0x0E, 0x0E, 0x04, 0, 0))  # bullet
_g("(", (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02))
_g(")", (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08))
_g("/", (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10))
_g("\\", (0x10, 0x10, 0x08, 0x04, 0x02, 0x01, 0x01))
_g("%", (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13))
_g("&", (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D))
_g("$", (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04))
_g("\u00a3", (0x07, 0x08, 0x08, 0x1E, 0x08, 0x08, 0x1F))  # pound
_g("\u20ac", (0x06, 0x09, 0x1E, 0x08, 0x1E, 0x09, 0x06))  # euro
_g(";", (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08))
_g(":", (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0))
_g("+", (0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0))
_g("=", (0, 0, 0x1F, 0, 0x1F, 0, 0))
_g("*", (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0))
_g("~", (0, 0, 0, 0x0A, 0x15, 0, 0))
_g("\u00b0", (0x0E, 0x11, 0x0E, 0, 0, 0, 0))   # degree
_g("\u00d7", (0, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0))  # multiply
_g("[", (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E))
_g("]", (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E))
_g("_", (0, 0, 0, 0, 0, 0, 0x1F))
_g("<", (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02))
_g(">", (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08))
_g("#", (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A))
_g("@", (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E))
# Curly quotes / apostrophes map to straight ones
F["\u2018"] = F["'"]
F["\u2019"] = F["'"]
F["\u201c"] = F['"']
F["\u201d"] = F['"']
F["\u2026"] = F["."]

QUESTION = F["?"]


def glyph(ch):
    return F.get(ch, QUESTION)


# ---------------------------------------------------------------- canvas
CREAM = (0xF7, 0xF1, 0xDE)
INK = (0x14, 0x14, 0x14)
WHITE = (0xFF, 0xFF, 0xFF)
RED = (0xC0, 0x39, 0x2B)
LAND = (0xD8, 0xCC, 0x9E)
LAND_EDGE = (0xB8, 0xA8, 0x72)
PANEL = (0xEF, 0xE3, 0xC4)

REGION_COLORS = {
    "Europe": (0x1F, 0x4E, 0x9C),
    "Middle East": (0xD9, 0x6C, 0x1E),
    "Asia": (0x7B, 0x3F, 0xA0),
    "Americas": (0xC0, 0x39, 0x2B),
    "Africa": (0x1E, 0x7D, 0x46),
    "Oceania": (0x0E, 0x7C, 0x7B),
    "Global": (0x6B, 0x72, 0x80),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def _off(self, x, y):
        return (y * self.w + x) * 3

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = self._off(x, y)
            self.buf[o] = c[0]
            self.buf[o + 1] = c[1]
            self.buf[o + 2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        if w <= 0 or h <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x0 >= x1 or y0 >= y1:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            o = self._off(x0, yy)
            self.buf[o:o + len(row)] = row

    def hline(self, x, y, w, c, t=1):
        self.fill_rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill_rect(x, y, t, h, c)

    def rect_outline(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)

    def ring(self, cx, cy, r, c, t=2):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            dx2 = int(max(0, (r - t) * (r - t) - dy * dy) ** 0.5) if abs(dy) < r - t else 0
            self.fill_rect(cx - dx, cy + dy, dx - dx2, 1, c)
            self.fill_rect(cx + dx2 + 1, cy + dy, dx - dx2, 1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        """Bresenham line, thickness t (square brush)."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.fill_rect(x - t // 2, y - t // 2, t, t, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy


# ---------------------------------------------------------------- text
def text_width(s, scale, bold=False, adv=None):
    """Width of the drawn glyphs: (n-1) advances + one glyph cell (5*scale)
    + bold offset. Advance per char = 6*scale (or adv override)."""
    if not s:
        return 0
    a = adv if adv is not None else 6 * scale
    boff = max(1, scale // 3) if bold else 0
    return (len(s) - 1) * (a + boff) + 5 * scale + boff


def draw_text(cv, x, y, s, scale, color, bold=False, adv=None):
    """Draw string; (x, y) is the top-left of the glyph cells."""
    a = adv if adv is not None else 6 * scale
    boff = max(1, scale // 3) if bold else 0
    cx = x
    for ch in s:
        g = glyph(ch)
        for row in range(7):
            bits = g[row]
            if not bits:
                continue
            for col in range(5):
                if bits & (0x10 >> col):
                    cv.fill_rect(cx + col * scale, y + row * scale, scale, scale, color)
                    if boff:
                        cv.fill_rect(cx + col * scale + boff, y + row * scale, scale, scale, color)
        cx += a + boff
    return cx


def wrap_text(s, max_w, scale, bold=False, adv=None):
    """Greedy word wrap; returns list of lines, each <= max_w. Never clips:
    a single over-long word is hard-split by characters."""
    lines = []
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if text_width(trial, scale, bold, adv) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # hard-split over-long single word
                while text_width(wd, scale, bold, adv) > max_w:
                    cut = 0
                    for i in range(1, len(wd) + 1):
                        if text_width(wd[:i], scale, bold, adv) <= max_w:
                            cut = i
                        else:
                            break
                    if cut == 0:
                        cut = 1
                    lines.append(wd[:cut])
                    wd = wd[cut:]
                cur = wd
        if cur or not lines:
            lines.append(cur)
    return lines


def draw_lines(cv, x, y, lines, scale, color, bold=False, adv=None, pitch=None):
    if pitch is None:
        pitch = 7 * scale + 2
    for i, ln in enumerate(lines):
        draw_text(cv, x, y + i * pitch, ln, scale, color, bold, adv)
    return y + len(lines) * pitch


# ---------------------------------------------------------------- PNG
def _chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


# ---------------------------------------------------------------- data
# Story facts reused verbatim from the verified v1 pool (23 Nov 2026).
TIMELINE = [
    ("02:40", "M6.5 quake strikes Vanuatu region"),
    ("05:12", "UN mission in Libya demands probe into Benghazi ship attacks"),
    ("09:00", "Nigeria's central bank opens final 2026 rate meeting"),
    ("09:21", "S&P 500 futures up 2.9% as Wall Street rebounds"),
    ("10:32", "Reuters: Trump official urged Guyana to cede land"),
    ("11:00", "Johannesburg council convenes to elect mayor"),
]

# (num, region, topic, headline, summary, claim?)
HEROES = [
    (1, "Africa", "WAR AT SEA",
     "Ukraine claims its drones sank Russian corvette off Libya",
     "President Zelenskyy says seven sea drones sank the corvette Merkury at Benghazi and hit the cargo ship MV Angara; the UN mission in Libya demands an independent probe. \u2014 AP",
     True),
    (2, "Americas", "DIPLOMACY",
     "Trump official urged Guyana to cede land to Venezuela",
     "A US official suggested Guyana consider ceding part of the oil-rich Essequibo region; Washington then reassured Georgetown its border policy had not changed. \u2014 Reuters",
     False),
    (3, "Middle East", "OIL WAR",
     "US strikes Iranian oil tanker as 31 ships mass beyond Hormuz",
     "Maritime analysts say the US hit a tanker exporting Iranian oil near its blockade line as laden sanctioned tankers wait beyond the strait. \u2014 WarBrief",
     True),
    (4, "Asia", "AID",
     "India gives Nepal $1.63bn flood-rebuild package",
     "PM Modi and Nepal PM Shah announce the package, sign eight deals and launch the Ayodhya\u2013Janakpur train. \u2014 The Hindu BusinessLine",
     False),
]

# (num, region, topic, headline, summary)
SMALLS = [
    (5, "Europe", "WAR",
     "Russian strike kills 11 in Dymer, near Kyiv",
     "A strike on a five-storey block in Dymer kills at least 11, rescuers pulling survivors from the rubble. \u2014 Just Security"),
    (6, "Europe", "POLITICS",
     "Burnham sells \u2018landmark\u2019 EU deal to MPs",
     "PM Burnham tells Parliament the Brussels deal is \u2018the single biggest growth measure\u2019 of this parliament, claiming a \u00a317bn boost the Tories dispute. \u2014 Brussels Reporter"),
    (7, "Europe", "STRIKE",
     "Belgium strike grounds all flights",
     "A national strike over \u20ac10bn austerity plans halts air traffic 07:00\u201321:00 and brings thousands onto Brussels streets. \u2014 Al Jazeera"),
    (8, "Middle East", "YEMEN",
     "Saudi strikes on Hodeida kill 10",
     "Warplanes hit a telecom building under construction in the early hours; nearly three dozen wounded, Houthi media say. \u2014 Press TV"),
    (9, "Americas", "MARKETS",
     "Wall Street rebounds; CrowdStrike buys Zscaler for $43.9bn",
     "Futures surge after last week\u2019s AI sell-off pushed the S&P 500 into correction; Nvidia rises ~8.7% premarket. \u2014 Reuters"),
    (10, "Africa", "EDUCATION",
     "101 pupils, one classroom: South Africa schools crisis",
     "The Human Rights Commission finds 101 learners crammed into one room across 173 monitored public schools. \u2014 Sowetan"),
    (11, "Africa", "POLITICS",
     "Johannesburg council sits to elect a mayor",
     "Councillors are sworn in and a mayor elected as the ANC weighs a pact handing ActionSA the city. \u2014 The Profiler"),
    (12, "Asia", "DISASTER",
     "Indonesia factory fire toll confirmed at 24",
     "More remains are recovered from the Cikande candy factory; about 30 workers are still missing. \u2014 AP"),
    (13, "Oceania", "QUAKE",
     "Deep M6.5 quake strikes Vanuatu region",
     "The 600 km-deep tremor hits at 02:40 UTC; no tsunami threat and no damage reported. \u2014 Fana News"),
    (14, "Oceania", "CRICKET",
     "New Zealand salvage draw after India\u2019s record 720",
     "The hosts bat out 120 overs on day five at Wellington; India\u2019s 720/9 is the highest Test total ever on NZ soil. \u2014 ICC"),
    (15, "Global", "CLIMATE",
     "Guterres \u2018deeply disappointed\u2019 as COP31 ends with no deal",
     "The UN chief warns 1.5\u00b0C overshoot is now inevitable after the longest summit ever collapses in Antalya. \u2014 The Business Standard"),
    (16, "Global", "SCIENCE",
     "Deepest volcanic eruption ever found in Mariana Trench",
     "A robot submersible finds pyroclastic rock from blasts ~6,150 m down near Challenger Deep. \u2014 Phys.org"),
]

# Best 21 of v1's 34 one-liners (13 weakest dropped), kept in v1 order.
# Region split: Europe 4, Middle East 4, Asia 2, Americas 4, Africa 4,
# Oceania 2, Global 1.
ALSO21 = [
    ("Europe", "Russia fires 153 drones at Ukraine overnight; two killed in Slovyansk"),
    ("Europe", "Ukrainian drones strike Russian oil sites in Tatarstan, Rostov, Perm"),
    ("Europe", "EU Council adopts \u20ac199.7bn budget for 2027"),
    ("Europe", "Ukraine says Kerch Bridge crippled; Crimea road link halted"),
    ("Middle East", "Houthis claim strike on Saudi Rabigh oil refinery"),
    ("Middle East", "Gaza death toll reaches 74,742, Health Ministry says"),
    ("Middle East", "Two killed in dawn strike on al-Mawasi, west of Khan Younis"),
    ("Middle East", "Egypt ready to defend Saudi Arabia against Houthis, Sisi says"),
    ("Asia", "South Korea education chief quits over AI exam-cheating chaos"),
    ("Asia", "Taiwan warns Canada against deeper China trade ties"),
    ("Americas", "Democrats plan 12 presidential debates for 2028, first in June 2027"),
    ("Americas", "US Army to detonate five tons of unstable explosives in Iowa"),
    ("Americas", "New thumb implant treats severe arthritis like a hip replacement"),
    ("Americas", "US oil and gas exports hit records amid Iran war trade shifts"),
    ("Africa", "Overberg wildfire destroys 24 homes across 25,000 hectares"),
    ("Africa", "Nigeria\u2019s central bank opens final rate meeting of 2026"),
    ("Africa", "US-Iran war hands African fuel exporters $21.6bn windfall"),
    ("Africa", "Kenya court fast-tracks challenge to Sh17.6bn election tech tender"),
    ("Oceania", "Pacific braces for fierce El Ni\u00f1o cyclone season"),
    ("Oceania", "Giddey posts 23 pts, 14 reb, 22 ast in NBA OT thriller"),
    ("Global", "AI screens ocean compounds, flags two prostate-cancer candidates"),
]

# (num, region, lat, lon) for the map dots
MAP_DOTS = [
    (1, "Africa", 32.1, 20.1),
    (2, "Americas", 6.8, -58.2),
    (3, "Middle East", 25.0, 59.0),
    (4, "Asia", 28.6, 77.2),
    (5, "Europe", 50.8, 30.3),
    (6, "Europe", 51.5, -0.1),
    (7, "Europe", 50.8, 4.4),
    (8, "Middle East", 14.8, 42.9),
    (9, "Americas", 40.7, -74.0),
    (10, "Africa", -25.7, 28.2),
    (11, "Africa", -26.2, 28.0),
    (12, "Asia", -6.1, 106.3),
    (13, "Oceania", -16.0, 167.0),
    (14, "Oceania", -41.3, 174.8),
    (15, "Global", 36.9, 30.7),
    (16, "Global", 11.3, 142.2),
]
# pixel nudges (dx, dy) so near-identical locations stay readable
MAP_NUDGE = {
    1: (-7, 7), 3: (10, -8), 4: (14, 4), 5: (2, -14), 6: (-8, -7), 7: (9, 5),
    10: (-12, 6), 11: (12, -6), 15: (12, 6),
}

# Coarse land bitmap: 36 rows (lat 90..-90, 5 deg each) x 72 cols (lon -180..180).
# Defined as (row, col_start, col_end) inclusive ranges.
LAND_CELLS = [
    (1, 5, 13), (1, 24, 26), (1, 50, 68),
    (2, 3, 15), (2, 23, 27), (2, 40, 70),
    (3, 2, 16), (3, 24, 27), (3, 38, 71),
    (4, 2, 17), (4, 36, 71),
    (5, 2, 18), (5, 34, 40), (5, 42, 71),
    (6, 3, 17), (6, 34, 42), (6, 43, 70),
    (7, 4, 16), (7, 34, 41), (7, 43, 69),
    (8, 5, 15), (8, 34, 40), (8, 44, 68),
    (9, 6, 14), (9, 35, 39), (9, 45, 66),
    (10, 7, 13), (10, 35, 38), (10, 46, 64),
    (11, 8, 12), (11, 33, 45), (11, 47, 62),
    (12, 9, 12), (12, 32, 46), (12, 48, 60),
    (13, 10, 12), (13, 32, 46), (13, 49, 58),
    (14, 11, 13), (14, 20, 26), (14, 33, 45), (14, 50, 56),
    (15, 20, 27), (15, 34, 44), (15, 52, 57),
    (16, 20, 28), (16, 34, 43), (16, 53, 58),
    (17, 21, 28), (17, 35, 42),
    (18, 21, 27), (18, 35, 41),
    (19, 22, 27), (19, 36, 40),
    (20, 22, 26), (20, 36, 39),
    (21, 23, 26), (21, 36, 39),
    (22, 23, 26), (22, 37, 39),
    (23, 24, 26), (23, 37, 38), (23, 58, 64),
    (24, 24, 25), (24, 58, 66),
    (25, 24, 25), (25, 59, 65),
    (26, 24, 25), (26, 67, 68),
    (27, 24, 25),
    (28, 24, 25),
]

FOOTER = ("Every story here happened or was first reported on Monday, 23 November 2026. "
          "CLAIM = one side\u2019s account, not independently confirmed. Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 "
          "UN News \u00b7 The Hindu BusinessLine \u00b7 ICC \u00b7 AAP \u00b7 PINA \u00b7 The Business Standard \u00b7 "
          "Sowetan \u00b7 Bloomberg Government \u00b7 Korea JoongAng Daily \u00b7 Phys.org \u00b7 Scientific Reports \u00b7 "
          "Just Security \u00b7 Press TV \u00b7 Al Jazeera")


# ---------------------------------------------------------------- layout
X0, X1 = 14, 1010          # content margins
CW = X1 - X0               # 996
COL2 = 520                 # second column x
COLW = 490                 # column width


def center_x(s, scale, bold=False, adv=None):
    return (W - text_width(s, scale, bold, adv)) // 2


def _waves(cv, px, py, rc):
    """Three zig-zag wave lines near the bottom of an illustration panel."""
    for wy in (66, 73, 80):
        x = 6
        up = True
        while x < 102:
            nx = min(x + 12, 104)
            ny = wy - 3 if up else wy + 3
            cv.line(px + x, py + wy, px + nx, py + ny, rc, 2)
            x, up = nx, not up


def _motif_sea(cv, px, py, rc):
    """Hero 1: sea, ship, sea drones above."""
    for (dx, dy) in ((20, 14), (48, 9), (78, 16)):
        cv.disc(px + dx, py + dy, 2, INK)
        cv.hline(px + dx - 4, py + dy, 9, INK, 1)
        cv.vline(px + dx, py + dy - 4, 9, INK, 1)
    # ship
    cv.fill_rect(px + 28, py + 52, 56, 12, rc)
    cv.fill_rect(px + 84, py + 54, 8, 10, rc)
    cv.fill_rect(px + 92, py + 56, 5, 8, rc)
    cv.vline(px + 52, py + 34, 18, INK, 2)
    cv.fill_rect(px + 62, py + 40, 10, 12, INK)
    cv.fill_rect(px + 54, py + 34, 10, 5, RED)
    _waves(cv, px, py, rc)


def _motif_map(cv, px, py, rc):
    """Hero 2: rough landmass with a long arrow across it."""
    cv.fill_rect(px + 20, py + 28, 44, 30, LAND)
    cv.rect_outline(px + 20, py + 28, 44, 30, LAND_EDGE, 1)
    cv.fill_rect(px + 72, py + 52, 14, 10, LAND)
    cv.rect_outline(px + 72, py + 52, 14, 10, LAND_EDGE, 1)
    cv.disc(px + 30, py + 44, 3, rc)
    cv.disc(px + 58, py + 36, 3, rc)
    cv.line(px + 14, py + 68, px + 92, py + 22, RED, 3)
    cv.line(px + 92, py + 22, px + 80, py + 24, RED, 2)
    cv.line(px + 92, py + 22, px + 88, py + 34, RED, 2)


def _motif_tanker(cv, px, py, rc):
    """Hero 3: oil tanker on waves."""
    cv.fill_rect(px + 8, py + 58, 94, 12, rc)
    cv.fill_rect(px + 102, py + 60, 6, 10, rc)
    cv.fill_rect(px + 70, py + 44, 20, 14, INK)
    cv.fill_rect(px + 76, py + 36, 8, 8, RED)
    cv.fill_rect(px + 14, py + 50, 40, 8, INK)
    cv.disc(px + 30, py + 30, 2, INK)
    cv.disc(px + 44, py + 24, 2, INK)
    _waves(cv, px, py, rc)


def _motif_train(cv, px, py, rc):
    """Hero 4: aid train with boxes."""
    cv.hline(px + 6, py + 76, 98, INK, 2)
    for sx in range(10, 102, 12):
        cv.vline(px + sx, py + 76, 5, INK, 2)
    cv.fill_rect(px + 8, py + 52, 30, 20, rc)
    cv.fill_rect(px + 42, py + 52, 30, 20, rc)
    cv.fill_rect(px + 76, py + 52, 28, 20, rc)
    cv.rect_outline(px + 8, py + 52, 30, 20, INK, 1)
    cv.rect_outline(px + 42, py + 52, 30, 20, INK, 1)
    cv.rect_outline(px + 76, py + 52, 28, 20, INK, 1)
    for wx in (16, 30, 50, 64, 84, 98):
        cv.disc(px + wx, py + 74, 3, INK)
    cv.fill_rect(px + 46, py + 42, 14, 10, WHITE)
    cv.rect_outline(px + 46, py + 42, 14, 10, INK, 1)
    cv.fill_rect(px + 80, py + 42, 14, 10, WHITE)
    cv.rect_outline(px + 80, py + 42, 14, 10, INK, 1)
    cv.hline(px + 49, py + 46, 8, RED, 1)
    cv.vline(px + 52, py + 44, 6, RED, 1)
    cv.hline(px + 83, py + 46, 8, RED, 1)
    cv.vline(px + 86, py + 44, 6, RED, 1)
    draw_text(cv, px + 13, py + 59, "AID", 1, WHITE, True)


MOTIFS = {1: _motif_sea, 2: _motif_map, 3: _motif_tanker, 4: _motif_train}


def draw_hero(cv, x, y, num, region, topic, headline, summary, claim):
    rc = REGION_COLORS[region]
    # numbered circle
    cx, cy = x + 13, y + 13
    cv.disc(cx, cy, 12, rc)
    n = str(num)
    draw_text(cv, cx - text_width(n, 2, True) // 2, cy - 7, n, 2, WHITE, True)
    tx = x + 30
    # region line
    tag = region.upper() + " \u00b7 " + topic
    draw_text(cv, tx, y + 2, tag, 1, rc, True)
    if claim:
        bx = tx + text_width(tag, 1, True) + 8
        bw = text_width("CLAIM", 1, True) + 8
        cv.rect_outline(bx, y + 1, bw, 9, RED, 1)
        draw_text(cv, bx + 4, y + 2, "CLAIM", 1, RED, True)
    # illustration panel, right side (110 x 88)
    px, py = x + 380, y + 2
    cv.fill_rect(px, py, 110, 88, PANEL)
    cv.rect_outline(px, py, 110, 88, rc, 1)
    MOTIFS[num](cv, px, py, rc)
    # headline, bold scale 3, up to 4 lines (text width 350)
    hl = wrap_text(headline, 350, 3, True)
    assert len(hl) <= 4, "hero headline overflow: %r" % headline
    draw_lines(cv, tx, y + 14, hl, 3, INK, True, pitch=23)
    # summary, full card width, up to 2 lines
    sy = y + 14 + len(hl) * 23 + 4
    sm = wrap_text(summary, COLW - 30, 1, False, adv=5)
    assert len(sm) <= 2, "hero summary overflow: %r" % summary
    assert sy + len(sm) * 9 <= y + 128, "hero card overflow: %r" % headline
    draw_lines(cv, tx, sy, sm, 1, INK, False, adv=5, pitch=9)


def draw_small(cv, x, y, num, region, topic, headline, summary):
    rc = REGION_COLORS[region]
    draw_text(cv, x, y, str(num), 1, rc, True)
    tx = x + 16
    tag = region.upper() + " \u00b7 " + topic
    draw_text(cv, tx, y, tag, 1, rc, True)
    hl = wrap_text(headline, COLW - 16, 2, True)
    assert len(hl) <= 2, "small headline overflow: %r" % headline
    draw_lines(cv, tx, y + 9, hl, 2, INK, True, pitch=16)
    sy = y + 9 + len(hl) * 16 + 3
    sm = wrap_text(summary, COLW - 16, 1, False, adv=5)
    assert len(sm) <= 2, "small summary overflow: %r" % summary
    assert sy + len(sm) * 9 <= y + 62, "small row overflow: %r" % headline
    draw_lines(cv, tx, sy, sm, 1, INK, False, adv=5, pitch=9)


def draw_map(cv, x, y, w, h):
    cw, ch = w / 72.0, h / 36.0
    for (r, c0, c1) in LAND_CELLS:
        cv.fill_rect(x + int(c0 * cw), y + int(r * ch),
                     int((c1 + 1) * cw) - int(c0 * cw),
                     max(1, int((r + 1) * ch) - int(r * ch)), LAND)
    cv.rect_outline(x, y, w, h, LAND_EDGE, 1)
    for (num, region, lat, lon) in MAP_DOTS:
        dx, dy = MAP_NUDGE.get(num, (0, 0))
        px = x + int((lon + 180.0) / 360.0 * w) + dx
        py = y + int((90.0 - lat) / 180.0 * h) + dy
        px = max(x + 8, min(x + w - 8, px))
        py = max(y + 8, min(y + h - 8, py))
        cv.disc(px, py, 6, REGION_COLORS[region])
        cv.ring(px, py, 6, WHITE, 1)
        s = str(num)
        draw_text(cv, px - text_width(s, 1, False) // 2, py - 3, s, 1, WHITE, False)


def build():
    assert len(HEROES) == 4 and len(SMALLS) == 12 and len(ALSO21) == 21
    cv = Canvas(W, H, CREAM)
    # frame
    cv.rect_outline(3, 3, W - 6, H - 6, INK, 2)

    # 1. kicker
    draw_text(cv, X0, 12, "ONE DAY OF WORLD NEWS, ONE PICTURE", 2, INK, True)
    r = "37 STORIES \u00b7 7 REGIONS"
    draw_text(cv, X1 - text_width(r, 2, True), 12, r, 2, INK, True)
    cv.hline(X0, 31, CW, INK, 1)

    # 2. masthead
    mast = "THE WORLD IN ONE DAY"
    draw_text(cv, center_x(mast, 5, True), 37, mast, 5, INK, True)
    date = "MONDAY, 23 NOVEMBER 2026"
    draw_text(cv, center_x(date, 2, True), 76, date, 2, INK, True)
    cv.hline(X0, 94, CW, INK, 1)

    # 3. timeline strip
    draw_text(cv, X0, 100, "THE DAY IN UTC", 1, INK, True)
    for i, (t, txt) in enumerate(TIMELINE):
        ex = X0 if i % 2 == 0 else COL2
        ey = 113 + (i // 2) * 13
        draw_text(cv, ex, ey, t, 1, RED, True)
        draw_text(cv, ex + text_width(t, 1, True) + 6, ey, txt, 1, INK, False)
    cv.hline(X0, 153, CW, INK, 1)

    # 4. heroes: 2x2, card height 128
    for i, (num, region, topic, hl, sm, claim) in enumerate(HEROES):
        hx = X0 if i % 2 == 0 else COL2
        hy = 159 + (i // 2) * 128
        draw_hero(cv, hx, hy, num, region, topic, hl, sm, claim)
    cv.hline(X0, 419, CW, INK, 1)

    # 5. small stories: 2 cols x 6 rows, row height 62
    for i, (num, region, topic, hl, sm) in enumerate(SMALLS):
        sx = X0 if i % 2 == 0 else COL2
        sy = 425 + (i // 2) * 62
        draw_small(cv, sx, sy, num, region, topic, hl, sm)
    cv.hline(X0, 801, CW, INK, 1)

    # 6. bottom band
    draw_text(cv, X0, 807, "WHERE IT HAPPENED", 1, INK, True)
    draw_text(cv, 346, 807, "ALSO ON MONDAY, 23 NOVEMBER 2026", 1, INK, True)
    draw_map(cv, X0, 821, 320, 104)
    # legend under the map: 4 cols x 2 rows
    legend = ["Europe", "Middle East", "Asia", "Africa",
              "Americas", "Oceania", "Global"]
    for li, name in enumerate(legend):
        lx = X0 + (li % 4) * 78
        ly = 929 + (li // 4) * 14
        cv.fill_rect(lx, ly, 8, 8, REGION_COLORS[name])
        draw_text(cv, lx + 12, ly, name, 1, INK, False, adv=5)
    # also-on: 3 columns x 7 rows
    for ci in range(3):
        items = ALSO21[ci * 7:(ci + 1) * 7]
        ax = 346 + ci * 220
        for j, (region, txt) in enumerate(items):
            iy = 821 + j * 19
            cv.disc(ax + 3, iy + 4, 3, REGION_COLORS[region])
            lines = wrap_text(txt, 209, 1, False, adv=5)
            assert len(lines) <= 2, "also-on overflow: %r" % txt
            draw_lines(cv, ax + 11, iy, lines, 1, INK, False, adv=5, pitch=9)
    cv.vline(338, 807, 150, INK, 1)

    # 7. date-check banner
    cv.fill_rect(X0, 961, CW, 26, RED)
    banner = ("DATE CHECK \u2014 Every story on this page happened or was first "
              "reported on Monday, 23 November 2026.")
    draw_text(cv, center_x(banner, 1, True), 970, banner, 1, WHITE, True)

    # 8. footer
    fl = wrap_text(FOOTER, CW, 1, False, adv=5)
    assert len(fl) <= 3, "footer overflow: %d lines" % len(fl)
    draw_lines(cv, X0, 991, fl, 1, INK, False, adv=5, pitch=8)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    cv = build()
    path = os.path.join(outdir, "entry.png")
    n = write_png(cv, path)
    print("wrote %s (%d bytes)" % (path, n))


if __name__ == "__main__":
    main()
