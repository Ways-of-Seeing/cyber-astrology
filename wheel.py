"""
ASCII natal chart wheel renderer.
Draws an elliptical wheel (corrected for terminal char aspect ratio)
with zodiac ring, house divisions, and planetary positions.
"""

import math

# Character aspect ratio correction: terminal chars are ~2.2× taller than wide.
# Using ry = rx * ASPECT makes the ellipse appear circular on screen.
ASPECT = 0.46

ZODIAC_SYMBOLS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
ZODIAC_NAMES_PT = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes",
]

# Outer ring rx in chars. ry = rx * ASPECT.
R_OUTER = 35


def _to_xy(longitude: float, r_factor: float, cx: int, cy: int,
           asc_lon: float) -> tuple[int, int]:
    """
    Convert astrological longitude to grid (x, y).
    r_factor: fraction of R_OUTER (1.0 = outer edge).
    AC is placed on the LEFT (screen angle = 180°).
    """
    screen_angle = math.radians(180.0 - longitude + asc_lon)
    rx = R_OUTER * r_factor
    ry = rx * ASPECT
    x = int(round(cx + rx * math.cos(screen_angle)))
    y = int(round(cy - ry * math.sin(screen_angle)))
    return x, y


def _ellipse_points(cx: int, cy: int, r_factor: float) -> list[tuple[int, int]]:
    """Return a set of (x, y) points forming an ellipse."""
    rx = R_OUTER * r_factor
    ry = rx * ASPECT
    steps = max(4, int(math.pi * (rx + ry)) * 2)
    pts = set()
    for i in range(steps):
        a = 2 * math.pi * i / steps
        x = int(round(cx + rx * math.cos(a)))
        y = int(round(cy - ry * math.sin(a)))
        pts.add((x, y))
    return list(pts)


def _line_points(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    """Return points along a line using parametric stepping."""
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy), 1) * 2
    pts = set()
    for i in range(steps + 1):
        t = i / steps
        pts.add((int(round(x1 + t * dx)), int(round(y1 + t * dy))))
    return list(pts)


def render(chart_data: dict, width: int = 79, height: int = 41) -> str:
    grid = [[" "] * width for _ in range(height)]
    cx = width // 2
    cy = height // 2

    asc_lon = chart_data["ascendant"]["longitude"]

    def put(x, y, ch):
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = ch

    # ── Outer boundary ──────────────────────────────────────────────────────
    for x, y in _ellipse_points(cx, cy, 1.0):
        put(x, y, "·")

    # ── Zodiac sign ring (inner boundary) ───────────────────────────────────
    for x, y in _ellipse_points(cx, cy, 0.8):
        put(x, y, "·")

    # ── Sign boundary tick-lines (every 30°) ────────────────────────────────
    for i in range(12):
        boundary_lon = i * 30.0  # 0° = Aries
        bx, by = _to_xy(boundary_lon, 0.8, cx, cy, asc_lon)
        ox, oy = _to_xy(boundary_lon, 1.0, cx, cy, asc_lon)
        for x, y in _line_points(bx, by, ox, oy):
            put(x, y, "·")

    # ── Zodiac symbols (midpoint of each sign, between outer & inner rings) ─
    for i, sym in enumerate(ZODIAC_SYMBOLS):
        mid_lon = i * 30.0 + 15.0
        x, y = _to_xy(mid_lon, 0.9, cx, cy, asc_lon)
        put(x, y, sym)

    # ── House boundary (inner circle) ───────────────────────────────────────
    for x, y in _ellipse_points(cx, cy, 0.6):
        put(x, y, "·")

    # ── House cusp lines & numbers ──────────────────────────────────────────
    house_cusps = chart_data["house_cusps"]
    for i, cusp_lon in enumerate(house_cusps):
        # Line from inner circle to zodiac ring
        ix, iy = _to_xy(cusp_lon, 0.6, cx, cy, asc_lon)
        zx, zy = _to_xy(cusp_lon, 0.8, cx, cy, asc_lon)
        for x, y in _line_points(ix, iy, zx, zy):
            put(x, y, "·")

        # House number: midpoint between this cusp and next, inside inner ring
        next_lon = house_cusps[(i + 1) % 12]
        if next_lon < cusp_lon:
            next_lon += 360.0
        mid_lon = (cusp_lon + next_lon) / 2.0
        nx, ny = _to_xy(mid_lon, 0.7, cx, cy, asc_lon)
        num = str(i + 1)
        if 0 <= nx < width - 1 and 0 <= ny < height:
            for j, ch in enumerate(num):
                put(nx + j - len(num) // 2, ny, ch)

    # ── Planet symbols ───────────────────────────────────────────────────────
    placed: list[tuple[int, int]] = []

    def find_free(base_x: int, base_y: int) -> tuple[int, int]:
        """Nudge a symbol if its cell is already occupied."""
        offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
                   (2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in offsets:
            nx2, ny2 = base_x + dx, base_y + dy
            if (nx2, ny2) not in placed:
                return nx2, ny2
        return base_x, base_y

    for attr, pdata in sorted(chart_data["planets"].items(),
                               key=lambda kv: kv[1]["longitude"]):
        lon = pdata["longitude"]
        px, py = _to_xy(lon, 0.42, cx, cy, asc_lon)
        px, py = find_free(px, py)
        placed.append((px, py))
        put(px, py, pdata["symbol"])

    # ── AC / DC / MC / IC markers ────────────────────────────────────────────
    for label, lon, r in [
        ("AC", asc_lon, 0.52),
        ("DC", (asc_lon + 180) % 360, 0.52),
        ("MC", chart_data["mc"]["longitude"], 0.52),
        ("IC", (chart_data["mc"]["longitude"] + 180) % 360, 0.52),
    ]:
        lx, ly = _to_xy(lon, r, cx, cy, asc_lon)
        for j, ch in enumerate(label):
            put(lx + j - 1, ly, ch)

    return "\n".join("".join(row) for row in grid)
