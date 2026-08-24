"""Minimal SVG path 'd' attribute parser -> a sequence of Cairo drawing ops.

Only what the two bundled artworks (hello.html's hand-drawn stroke, and plain
Bezier text outlines) actually use: M/L/H/V/C/S/Q/T/Z, absolute and relative.
Arcs ('A') are not needed by any asset in this app and are not implemented.

Not a general-purpose SVG library on purpose: no external dependency, no
runtime cost beyond parsing two small path strings once at startup.
"""
import math
import re

_TOKEN_RE = re.compile(r"[MLHVCSQTAZmlhvcsqtaz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _arc_to_cubics(x0, y0, rx, ry, phi_deg, large_arc, sweep, x, y):
    """Standard SVG elliptical-arc-to-cubic-Bezier conversion (endpoint-to-
    center parameterization, subdivided into <=90-degree cubic segments)."""
    if rx == 0 or ry == 0 or (x0 == x and y0 == y):
        return [(x, y, x, y, x, y)]

    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg % 360)
    cos_phi, sin_phi = math.cos(phi), math.sin(phi)

    dx2, dy2 = (x0 - x) / 2.0, (y0 - y) / 2.0
    x1p = cos_phi * dx2 + sin_phi * dy2
    y1p = -sin_phi * dx2 + cos_phi * dy2

    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s

    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large_arc == sweep:
        co = -co

    cxp = co * (rx * y1p) / ry
    cyp = -co * (ry * x1p) / rx
    cx = cos_phi * cxp - sin_phi * cyp + (x0 + x) / 2.0
    cy = sin_phi * cxp + cos_phi * cyp + (y0 + y) / 2.0

    def angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        length = math.sqrt((ux ** 2 + uy ** 2) * (vx ** 2 + vy ** 2))
        a = math.acos(max(-1.0, min(1.0, dot / length))) if length else 0.0
        return a if (ux * vy - uy * vx) >= 0 else -a

    theta1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = angle(
        (x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry
    )
    if not sweep and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2 * math.pi

    segments = max(1, int(math.ceil(abs(dtheta) / (math.pi / 2))))
    delta = dtheta / segments
    t = 4.0 / 3.0 * math.tan(delta / 4.0)

    cubics = []
    theta = theta1
    for _ in range(segments):
        cos_t1, sin_t1 = math.cos(theta), math.sin(theta)
        theta2 = theta + delta
        cos_t2, sin_t2 = math.cos(theta2), math.sin(theta2)

        p1x = cos_phi * rx * cos_t1 - sin_phi * ry * sin_t1 + cx
        p1y = sin_phi * rx * cos_t1 + cos_phi * ry * sin_t1 + cy
        p2x = cos_phi * rx * cos_t2 - sin_phi * ry * sin_t2 + cx
        p2y = sin_phi * rx * cos_t2 + cos_phi * ry * sin_t2 + cy

        q1x = p1x - t * (cos_phi * rx * sin_t1 + sin_phi * ry * cos_t1)
        q1y = p1y - t * (sin_phi * rx * sin_t1 - cos_phi * ry * cos_t1)
        q2x = p2x + t * (cos_phi * rx * sin_t2 + sin_phi * ry * cos_t2)
        q2y = p2y + t * (sin_phi * rx * sin_t2 - cos_phi * ry * cos_t2)

        cubics.append((q1x, q1y, q2x, q2y, p2x, p2y))
        theta = theta2

    return cubics


def _tokenize(d):
    return _TOKEN_RE.findall(d)


def parse_path(d):
    """Parse an SVG path 'd' string into a list of absolute-coordinate ops:
    [('M', x, y), ('L', x, y), ('C', x1,y1,x2,y2,x,y), ('Z',)]
    Quadratic curves are converted to cubic so callers only handle 'C'.
    """
    tokens = _tokenize(d)
    i = 0
    ops = []
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    last_cmd = None
    last_ctrl = None  # reflection control point for S/T

    def nextf():
        nonlocal i
        v = float(tokens[i])
        i += 1
        return v

    while i < len(tokens):
        tok = tokens[i]
        if tok.isalpha():
            cmd = tok
            i += 1
        else:
            # repeated implicit command
            cmd = last_cmd
        is_rel = cmd.islower()
        C = cmd.upper()

        if C == "M":
            x, y = nextf(), nextf()
            if is_rel:
                x, y = cur[0] + x, cur[1] + y
            ops.append(("M", x, y))
            cur = (x, y)
            start = cur
            last_ctrl = None
            last_cmd = "l" if is_rel else "L"  # subsequent bare coords are lineto
        elif C == "L":
            x, y = nextf(), nextf()
            if is_rel:
                x, y = cur[0] + x, cur[1] + y
            ops.append(("L", x, y))
            cur = (x, y)
            last_ctrl = None
            last_cmd = cmd
        elif C == "H":
            x = nextf()
            if is_rel:
                x = cur[0] + x
            ops.append(("L", x, cur[1]))
            cur = (x, cur[1])
            last_ctrl = None
            last_cmd = cmd
        elif C == "V":
            y = nextf()
            if is_rel:
                y = cur[1] + y
            ops.append(("L", cur[0], y))
            cur = (cur[0], y)
            last_ctrl = None
            last_cmd = cmd
        elif C == "C":
            x1, y1, x2, y2, x, y = (nextf() for _ in range(6))
            if is_rel:
                x1, y1 = cur[0] + x1, cur[1] + y1
                x2, y2 = cur[0] + x2, cur[1] + y2
                x, y = cur[0] + x, cur[1] + y
            ops.append(("C", x1, y1, x2, y2, x, y))
            cur = (x, y)
            last_ctrl = (x2, y2)
            last_cmd = cmd
        elif C == "S":
            x2, y2, x, y = (nextf() for _ in range(4))
            if is_rel:
                x2, y2 = cur[0] + x2, cur[1] + y2
                x, y = cur[0] + x, cur[1] + y
            if last_ctrl is not None:
                x1, y1 = 2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]
            else:
                x1, y1 = cur
            ops.append(("C", x1, y1, x2, y2, x, y))
            cur = (x, y)
            last_ctrl = (x2, y2)
            last_cmd = cmd
        elif C == "Q":
            x1, y1, x, y = (nextf() for _ in range(4))
            if is_rel:
                x1, y1 = cur[0] + x1, cur[1] + y1
                x, y = cur[0] + x, cur[1] + y
            cx1 = cur[0] + 2.0 / 3.0 * (x1 - cur[0])
            cy1 = cur[1] + 2.0 / 3.0 * (y1 - cur[1])
            cx2 = x + 2.0 / 3.0 * (x1 - x)
            cy2 = y + 2.0 / 3.0 * (y1 - y)
            ops.append(("C", cx1, cy1, cx2, cy2, x, y))
            cur = (x, y)
            last_ctrl = (x1, y1)
            last_cmd = cmd
        elif C == "T":
            x, y = nextf(), nextf()
            if is_rel:
                x, y = cur[0] + x, cur[1] + y
            if last_ctrl is not None:
                x1, y1 = 2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]
            else:
                x1, y1 = cur
            cx1 = cur[0] + 2.0 / 3.0 * (x1 - cur[0])
            cy1 = cur[1] + 2.0 / 3.0 * (y1 - cur[1])
            cx2 = x + 2.0 / 3.0 * (x1 - x)
            cy2 = y + 2.0 / 3.0 * (y1 - y)
            ops.append(("C", cx1, cy1, cx2, cy2, x, y))
            cur = (x, y)
            last_ctrl = (x1, y1)
            last_cmd = cmd
        elif C == "A":
            rx, ry, rot = nextf(), nextf(), nextf()
            large_arc, sweep = int(nextf()), int(nextf())
            x, y = nextf(), nextf()
            if is_rel:
                x, y = cur[0] + x, cur[1] + y
            for cubic in _arc_to_cubics(cur[0], cur[1], rx, ry, rot, large_arc, sweep, x, y):
                ops.append(("C",) + cubic)
            cur = (x, y)
            last_ctrl = None
            last_cmd = cmd
        elif C == "Z":
            ops.append(("Z",))
            cur = start
            last_ctrl = None
            last_cmd = cmd
        else:
            raise ValueError("Unsupported SVG path command: %s" % cmd)

    return ops


def path_to_cairo(cr, ops):
    """Append parsed ops to a cairo.Context's current path."""
    for op in ops:
        if op[0] == "M":
            cr.move_to(op[1], op[2])
        elif op[0] == "L":
            cr.line_to(op[1], op[2])
        elif op[0] == "C":
            cr.curve_to(*op[1:])
        elif op[0] == "Z":
            cr.close_path()
