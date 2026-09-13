"""
CPA Math 6 — Day 9: Area of a Parallelogram — Refine, Practice & Quiz
Built to match the visual/interactive structure of the Day 5 ("Area Is
Multiplication"), Day 6 ("Area Unlocks the Missing Side"), Day 7 ("Area of
Compound Rectangles"), and Day 8 ("Area of a Parallelogram — Explore &
Model It") apps by Xavier Honablue, M.Ed — Chandler Park Academy.

Day 8 covered i-Ready Classroom Mathematics Lesson 1, Session 2's Explore ->
Model It -> Try It portion (the cut-and-slide proof that a parallelogram is
a rectangle in disguise). Day 9 finishes Lesson 1 exactly where the i-Ready
Teacher Edition picks back up, problem-for-problem and number-for-number:

  * Session 2 Apply It, problems 6-8 (spinach pie, select-all dimensions,
    grid parallelogram)
  * Session 3 Refine, the worked Example plus guided problems 2-3 (a
    mixed-number base, and Juanita's base-times-slant mistake on the barn
    window)
  * Additional Practice, problems 3-5 (the tiled-wall mirror, explaining
    which sides are base/height, the Eagle Express logo)
  * The Lesson 1 Quiz, problems 1-5 (grid-entry area, the kitchen tile,
    a mixed-number area, Sayali's four-parallelogram chalk design, and the
    two-bases-same-area question)
  * The Math Journal + Error Alert + End of Lesson Checklist that close the
    session

Every number, distractor, and correct answer below is taken directly from
the i-Ready Grade 6 Teacher Edition pages for this lesson so this app can be
projected as a 1:1 stand-in for (or companion to) the worktext.

Run locally with: streamlit run app.py
Deploy the same way Day 5/6/7/8 were deployed: push this folder to a new
GitHub repo (cpamath6day9) and connect it on Streamlit Community Cloud as
cpamath6day9.streamlit.app, then add the card to the launcher app.
"""

import math
import random

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import streamlit as st

# ----------------------------------------------------------------------
# Page config & theme (matches Day 7/8 exactly)
# ----------------------------------------------------------------------
st.set_page_config(page_title="Day 9 — Area of a Parallelogram: Refine & Quiz", page_icon="📐", layout="wide")

NAVY = "#1b3a5c"
NAVY_LIGHT = "#eef4fa"
NAVY_BORDER = "#2c4a6e"
GREEN = "#3f7d55"
GREEN_LIGHT = "#eef7f0"
GOLD = "#8a5a20"
GOLD_LIGHT = "#f6ecd9"
RED = "#b03a2e"
RED_LIGHT = "#fdf1ef"
PURPLE = "#5b3a7d"
PURPLE_LIGHT = "#f2eef7"
GRAY = "#7a8290"

FILL_A = "#dbe8f6"   # kept / stationary region
FILL_B = "#f6e3c6"   # moved piece / second parallelogram
FILL_CUT = "#f6d0c9" # subtracted / unshaded region

CUSTOM_CSS = f"""
<style>
.box {{
    border: 2px solid {NAVY};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    background: white;
}}
.pill {{
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}}
.box-readaloud {{ border-color: {NAVY}; }}
.box-readaloud .pill {{ background: {NAVY}; }}
.box-readaloud p {{ font-style: italic; margin: 4px 0 0 0; }}

.box-literacy {{ border-color: {NAVY_BORDER}; background: {NAVY_LIGHT}; }}
.box-literacy .pill {{ background: {NAVY_BORDER}; }}

.box-existing {{ border-color: {GREEN}; background: {GREEN_LIGHT}; }}
.box-existing .pill {{ background: {GREEN}; }}

.box-tools {{ border-color: {GOLD}; background: {GOLD_LIGHT}; }}
.box-tools .pill {{ background: {GOLD}; }}

.box-observer {{ border: 2px dashed {RED}; background: {RED_LIGHT}; }}
.box-observer .pill {{ background: {RED}; }}

.box-method {{ border-color: {PURPLE}; background: {PURPLE_LIGHT}; }}
.box-method .pill {{ background: {PURPLE}; }}

.ask {{ color: {RED}; font-weight: 700; margin-top: 8px; }}

.roadmap-title {{ color: {NAVY}; font-weight: 700; font-size: 15px; margin-bottom: 0; }}
.roadmap-sub {{ color: #5a6672; font-size: 11.5px; margin-top: -4px; }}

.credit {{ text-align: center; color: #8a939c; font-size: 11px; margin-top: 18px; }}

.itext {{ background: {NAVY_LIGHT}; border-left: 4px solid {NAVY}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 14px; }}
.consider {{ background: {PURPLE_LIGHT}; border-left: 4px solid {PURPLE}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 13.5px; }}
.pairshare {{ background: {GOLD_LIGHT}; border-left: 4px solid {GOLD}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 13.5px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def box(kind, pill, body_html):
    st.markdown(
        f'<div class="box box-{kind}"><span class="pill">{pill}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def read_aloud(text):
    box("readaloud", "🔊 READ ALOUD", f"<p>&ldquo;{text}&rdquo;</p>")


def ask_the_class(text):
    st.markdown(f'<p class="ask">❓ Ask the class: {text}</p>', unsafe_allow_html=True)


def consider_this(text):
    st.markdown(f'<div class="consider"><b>CONSIDER THIS...</b><br>{text}</div>', unsafe_allow_html=True)


def pair_share(text):
    st.markdown(f'<div class="pairshare"><b>PAIR/SHARE</b><br>{text}</div>', unsafe_allow_html=True)


def itext_source(label, text):
    """Verbatim-style callout showing exactly what the worktext page says,
    so the teacher can confirm this app matches the book in hand."""
    st.markdown(f'<div class="itext"><b>📘 {label}</b><br>{text}</div>', unsafe_allow_html=True)


def attempt(key):
    k = f"attempts_{key}"
    st.session_state[k] = st.session_state.get(k, 0) + 1
    return st.session_state[k]


def explain(title, lines):
    body = "<br>".join(lines)
    st.markdown(
        f'<div class="box box-tools"><span class="pill">💡 {title}</span>{body}</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------
def _parallelogram_points(base, height, lean):
    """A=(0,0) bottom-left, B=(base,0) bottom-right, C=(base+lean,height)
    top-right, D=(lean,height) top-left. P=(lean,0) is the foot of the
    perpendicular dropped from D."""
    A = (0, 0)
    B = (base, 0)
    C = (base + lean, height)
    D = (lean, height)
    P = (lean, 0)
    return A, B, C, D, P


def draw_labeled_parallelogram(base, height, lean, base_label=None, height_label=None,
                                side_label=None, side_is="left", extra_note=None,
                                inside_height=True, figsize=(4.6, 4.0)):
    """General-purpose parallelogram drawer used across Day 9's problems.
    side_label marks the slanted (non-perpendicular) side length — the
    distractor every one of these problems is built around. inside_height
    draws the height segment *inside* the shape (as the book's diagrams do)
    instead of as an outside dashed extension."""
    A, B, C, D, P = _parallelogram_points(base, height, lean)
    base_label = base_label if base_label is not None else f"{base}"
    height_label = height_label if height_label is not None else f"{height}"
    fig, ax = plt.subplots(figsize=figsize)
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))

    # base label (bottom)
    ax.text((A[0] + B[0]) / 2, -0.55, f"base = {base_label}", ha="center", va="top",
             fontsize=10.5, fontweight="bold", color=NAVY)

    # height segment + right-angle mark, drawn inside the shape like the book
    if inside_height:
        ax.plot([D[0], P[0]], [D[1], P[1]], linestyle="--", color=RED, linewidth=1.8)
        ax.plot([P[0], P[0] + 0.3], [0, 0], color=RED, linewidth=1.4)
        ax.plot([P[0], P[0]], [0, 0.3], color=RED, linewidth=1.4)
        ax.text(P[0] + 0.15, height / 2, f"height = {height_label}", ha="left", va="center",
                 fontsize=10, fontweight="bold", color=RED, rotation=90)

    # slanted side label (the distractor)
    if side_label is not None:
        if side_is == "left":
            mx, my = (A[0] + D[0]) / 2, (A[1] + D[1]) / 2
            ax.text(mx - 0.5, my, side_label, ha="right", va="center", fontsize=10, color=GRAY, style="italic")
        else:
            mx, my = (B[0] + C[0]) / 2, (B[1] + C[1]) / 2
            ax.text(mx + 0.5, my, side_label, ha="left", va="center", fontsize=10, color=GRAY, style="italic")

    if extra_note:
        cx = (A[0] + B[0] + C[0] + D[0]) / 4
        ax.text(cx, height + 0.5, extra_note, ha="center", va="bottom", fontsize=9, color=GRAY, style="italic")

    pad = max(1.8, abs(side_label is not None) * 0.5 + 1.8)
    ax.set_xlim(-2.2, base + lean + 2.2)
    ax.set_ylim(-1.6, height + 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_quiz1_parallelogram():
    """Quiz #1: base 9 cm, height 8 cm, slant side 10 cm, and a 17 cm
    diagonal drawn dashed from the bottom-left vertex to the top-right
    vertex (a second distractor — a diagonal is not a side at all)."""
    base, height, lean = 9, 8, 4
    A, B, C, D, P = _parallelogram_points(base, height, lean)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    # diagonal distractor
    ax.plot([A[0], C[0]], [A[1], C[1]], linestyle="--", color=GRAY, linewidth=1.6)
    ax.text((A[0] + C[0]) / 2 + 0.3, (A[1] + C[1]) / 2, "17 cm", color=GRAY, fontsize=10, style="italic")
    # left slant side
    ax.text((A[0] + D[0]) / 2 - 0.6, (A[1] + D[1]) / 2, "10 cm", color=GRAY, fontsize=10, style="italic", ha="right")
    # base
    ax.text((A[0] + B[0]) / 2, -0.55, "base = 9 cm", ha="center", va="top", fontsize=10.5, fontweight="bold", color=NAVY)
    # height, outside on the right like the book (dashed vertical + right angle)
    ax.plot([B[0], B[0]], [0, height], linestyle="--", color=RED, linewidth=1.8)
    ax.plot([B[0] - 0.3, B[0]], [0, 0], color=RED, linewidth=1.4)
    ax.plot([B[0], B[0]], [0, 0.3], color=RED, linewidth=1.4)
    ax.text(B[0] + 0.2, height / 2, "height = 8 cm", ha="left", va="center", fontsize=10, fontweight="bold", color=RED, rotation=90)
    ax.plot([B[0], C[0]], [height, height], linestyle=":", color=RED, linewidth=1.2)
    ax.set_xlim(-1.8, base + lean + 2.6)
    ax.set_ylim(-1.4, height + 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_kitchen_tile():
    """Quiz #2: base = 2 x height, height = 2.5 in, other side = 3 in
    (distractor). base = 5 in."""
    base, height, lean = 5, 2.5, 1.6
    return draw_labeled_parallelogram(base, height, lean, base_label="2 × 2.5 in", height_label="2.5 in",
                                       side_label="3 in (other side)", side_is="left")


def draw_quiz3_parallelogram():
    """Quiz #3: base = 6 1/5 ft, height = 5 ft, slant not given a number in
    the book (drawn dashed inside, right angle marked)."""
    base, height, lean = 6.2, 5, 1.4
    return draw_labeled_parallelogram(base, height, lean, base_label="6⅕ ft", height_label="5 ft")


def draw_sayali_design():
    """Quiz #4: a 42 in x 48 in rectangle holding an X made of four
    identical parallelograms, each base 12 in / height 21 in, crossing at
    the center — matches the sidewalk-chalk design in the book."""
    W, H = 48, 42
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="white", edgecolor=NAVY, linewidth=2.2))
    cx, cy = W / 2, H / 2
    half_w = 6  # half of the 12 in base, drawn as strip width
    # four arms of the X, each a thin rectangle/parallelogram strip rotated 45 deg-ish
    for sign in (1, -1):
        # diagonal strip 1: bottom-left to top-right direction
        dx, dy = W / 2, H / 2
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        px, py = -uy * half_w, ux * half_w
        pts = [
            (cx - dx * sign - px, cy - dy * sign - py),
            (cx - dx * sign + px, cy - dy * sign + py),
            (cx + dx * sign + px, cy + dy * sign + py),
            (cx + dx * sign - px, cy + dy * sign - py),
        ]
        ax.add_patch(Polygon(pts, closed=True, facecolor=FILL_CUT, edgecolor=NAVY, linewidth=1.4))
        # diagonal strip 2: bottom-right to top-left direction
        dx2, dy2 = -W / 2, H / 2
        length2 = math.hypot(dx2, dy2)
        ux2, uy2 = dx2 / length2, dy2 / length2
        px2, py2 = -uy2 * half_w, ux2 * half_w
        pts2 = [
            (cx - dx2 * sign - px2, cy - dy2 * sign - py2),
            (cx - dx2 * sign + px2, cy - dy2 * sign + py2),
            (cx + dx2 * sign + px2, cy + dy2 * sign + py2),
            (cx + dx2 * sign - px2, cy + dy2 * sign - py2),
        ]
        ax.add_patch(Polygon(pts2, closed=True, facecolor=FILL_CUT, edgecolor=NAVY, linewidth=1.4))
    # one arm's base/height callouts, like the book's 21 in / 12 in labels near the top-left
    ax.annotate("", xy=(0, H * 0.5), xytext=(0, H), arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.2))
    ax.text(-2.5, H * 0.75, "21 in.", ha="right", va="center", fontsize=9, fontweight="bold", color=NAVY)
    ax.annotate("", xy=(0, H * 0.5), xytext=(12, H * 0.5), arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.2))
    ax.text(6, H * 0.5 + 1.5, "12 in.", ha="center", va="bottom", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(W / 2, -3, "48 in.", ha="center", va="top", fontsize=10, fontweight="bold", color=NAVY)
    ax.text(-4, H / 2, "42 in.", ha="right", va="center", fontsize=10, fontweight="bold", color=NAVY, rotation=90)
    ax.set_xlim(-8, W + 4)
    ax.set_ylim(-6, H + 4)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_refine_example():
    """Refine, problem 2: base = 9 1/4 ft, height = 4 ft -> Area 37 ft^2."""
    base, height, lean = 9.25, 4, 1.6
    return draw_labeled_parallelogram(base, height, lean, base_label="9¼ ft", height_label="4 ft")


def draw_barn_window():
    """Refine, problem 3: height is half the base; base = 12 in, other side
    = 10 in (the number Juanita mistakenly multiplied by). height = 6 in."""
    base, height, lean = 12, 6, 3.5
    return draw_labeled_parallelogram(base, height, lean, base_label="12 in", height_label="6 in",
                                       side_label="10 in (other side)", side_is="left")


def draw_tiled_mirror():
    """Additional Practice #3: a parallelogram mirror on a wall of 4-in
    square tiles — base spans 5 tiles, height spans 6 tiles."""
    tiles_w, tiles_h, tile = 7, 8, 1
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    for i in range(tiles_w):
        for j in range(tiles_h):
            ax.add_patch(Rectangle((i * tile, j * tile), tile, tile, facecolor="white",
                                    edgecolor="#c7cfd8", linewidth=0.8))
    lean = 2
    base_tiles, height_tiles = 5, 6
    ox, oy = 0.5, 1
    A = (ox, oy)
    B = (ox + base_tiles, oy)
    C = (ox + base_tiles + lean, oy + height_tiles)
    D = (ox + lean, oy + height_tiles)
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2, alpha=0.85))
    ax.plot([A[0], B[0]], [oy - 0.4, oy - 0.4], color=NAVY, linewidth=1.2)
    ax.text((A[0] + B[0]) / 2, oy - 0.7, "base = 5 tiles", ha="center", va="top", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.plot([A[0] - 0.4, A[0] - 0.4], [oy, oy + height_tiles], color=RED, linewidth=1.2)
    ax.text(A[0] - 0.6, oy + height_tiles / 2, "height = 6 tiles", ha="right", va="center", fontsize=9.5,
             fontweight="bold", color=RED, rotation=90)
    ax.set_xlim(-2, tiles_w + 0.5)
    ax.set_ylim(-1.5, tiles_h + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Each tile is 4 in. × 4 in.", fontsize=10, color=NAVY)
    return fig


def draw_identify_base_height():
    """Additional Practice #4: 5 cm side (has the perpendicular tick, so it
    IS the base), 6.5 cm slanted side (distractor), and 5.2 cm height drawn
    from the top vertex down to (and past) the 5 cm side."""
    base, height, lean = 5, 5.2 * 0.7, 2.0  # scaled so slant reads ~6.5
    # rebuild geometry so the *right* side is length 6.5 exactly and the
    # perpendicular from the top-left vertex to the base is exactly 5.2
    height_val = 5.2
    base_val = 5
    slant_val = 6.5
    lean_val = math.sqrt(max(slant_val ** 2 - height_val ** 2, 0))
    A, B, C, D, P = _parallelogram_points(base_val, height_val, lean_val)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    ax.plot([D[0], P[0]], [D[1], P[1]], linestyle="--", color=RED, linewidth=1.8)
    ax.plot([P[0], P[0] + 0.25], [0, 0], color=RED, linewidth=1.4)
    ax.plot([P[0], P[0]], [0, 0.25], color=RED, linewidth=1.4)
    ax.text(P[0] + 0.15, height_val / 2, "5.2 cm", ha="left", va="center", fontsize=10, fontweight="bold", color=RED, rotation=90)
    ax.text((A[0] + B[0]) / 2, -0.5, "5 cm  (has the right-angle tick)", ha="center", va="top", fontsize=9.5,
             fontweight="bold", color=NAVY)
    ax.text((B[0] + C[0]) / 2 + 0.3, (B[1] + C[1]) / 2, "6.5 cm", ha="left", va="center", fontsize=10, color=GRAY, style="italic")
    ax.set_xlim(-1.5, base_val + lean_val + 2.2)
    ax.set_ylim(-1.3, height_val + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_eagle_logo():
    """Additional Practice #5: Eagle Express logo. base = 3.1 ft (bottom),
    perpendicular height = 3 ft (right side, dashed), slanted side = 3.2 ft
    (left side, the distractor)."""
    base_val, height_val = 3.1, 3
    lean_val = 0.9
    A, B, C, D, P = _parallelogram_points(base_val, height_val, lean_val)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=NAVY_LIGHT, edgecolor=NAVY, linewidth=2.2))
    ax.text((A[0] + D[0]) / 2 - 0.4, (A[1] + D[1]) / 2, "3.2 ft", ha="right", va="center", fontsize=10, color=GRAY, style="italic")
    ax.plot([B[0], B[0]], [0, height_val], linestyle="--", color=RED, linewidth=1.8)
    ax.plot([B[0] - 0.25, B[0]], [0, 0], color=RED, linewidth=1.4)
    ax.plot([B[0], B[0]], [0, 0.25], color=RED, linewidth=1.4)
    ax.text(B[0] + 0.15, height_val / 2, "3 ft", ha="left", va="center", fontsize=10.5, fontweight="bold", color=RED, rotation=90)
    ax.text((A[0] + B[0]) / 2, -0.5, "base = 3.1 ft", ha="center", va="top", fontsize=10.5, fontweight="bold", color=NAVY)
    ax.text((A[0] + B[0] + C[0] + D[0]) / 4, height_val / 2, "EAGLE\nEXPRESS", ha="center", va="center",
             fontsize=9, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.8, base_val + lean_val + 2.0)
    ax.set_ylim(-1.3, height_val + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_two_bases_parallelogram():
    """Quiz #5: a parallelogram with one pair of sides 36 units, the other
    pair 4 units, and area 24 sq units — so it has two honest base/height
    pairs: (36, 2/3) and (4, 6)."""
    base_val, side_val = 8, 3
    lean_val = 1.5
    A, B, C, D, P = _parallelogram_points(base_val, side_val, lean_val)
    fig, ax = plt.subplots(figsize=(4.6, 4.0))
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    ax.text((A[0] + B[0]) / 2, -0.55, "one pair of sides = 36 units", ha="center", va="top", fontsize=9.5,
             fontweight="bold", color=NAVY)
    ax.text((A[0] + D[0]) / 2 - 0.4, (A[1] + D[1]) / 2, "other pair\n= 4 units", ha="right", va="center",
             fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text((A[0] + B[0] + C[0] + D[0]) / 4, side_val / 2, "Area =\n24 sq units", ha="center", va="center",
             fontsize=10, fontweight="bold", color=RED)
    ax.set_xlim(-3.4, base_val + lean_val + 1.6)
    ax.set_ylim(-1.4, side_val + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def random_parallelogram():
    base = random.randint(7, 14)
    height = random.randint(3, 8)
    lean = random.randint(1, min(6, base - 2))
    return base, height, lean


# ----------------------------------------------------------------------
# Sidebar — Sign In + Roadmap (mirrors Day 5 / 6 / 7 / 8)
# ----------------------------------------------------------------------
with st.sidebar:
    st.subheader("Sign In")
    st.text_input("Your name:", key="student_name")
    st.selectbox("Choose your shape avatar:", ["Rectangle", "Square", "Parallelogram", "L-Shape", "T-Shape"], key="avatar")
    st.selectbox(
        "Pick your learning mode:",
        ["Focus Champ", "Growth Mode", "Problem Solver", "Data Boss", "Brain Builder"],
        key="learning_mode",
    )
    st.markdown("---")
    st.markdown('<p class="roadmap-title">Day 9 Roadmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-sub">55-minute period — i-Ready Lesson 1, Sessions 2–3: Refine &amp; Quiz</p>', unsafe_allow_html=True)

    steps = [
        "1. Welcome Back & Warm-Up",
        "2. Apply It: Finish Session 2",
        "3. Refine: Worked Example",
        "4. Refine: Juanita's Mistake",
        "5. Additional Practice 3–5",
        "6. Engage / Explore / Enrich",
        "7. Lesson 1 Quiz (Problems 1–3)",
        "8. Lesson 1 Quiz (Problems 4–5)",
        "9. Math Journal & Close",
    ]
    if "step" not in st.session_state:
        st.session_state.step = 0
    for i, label in enumerate(steps):
        marker = "▶ " if i == st.session_state.step else ""
        if st.button(marker + label, key=f"nav_{i}", use_container_width=True):
            st.session_state.step = i
            st.rerun()
    st.markdown("---")
    st.caption("Lesson mode: i-Ready Classroom Mathematics — Apply It → Refine → Additional Practice → Lesson Quiz → Math Journal, aligned page-for-page to the Grade 6 Teacher Edition.")
    st.caption("Standards: 6.G.A.1 (grade-level) · 3.MD.C.7d (foundational) · MP.2, MP.4, MP.5, MP.6")

# ----------------------------------------------------------------------
# Roadmap step content
# ----------------------------------------------------------------------
step = st.session_state.step
name = st.session_state.get("student_name", "") or "class"

st.markdown(f"## {steps[step]}")
st.progress((step + 1) / len(steps))

# ======================================================================
# STEP 0 — Welcome back / warm-up
# ======================================================================
if step == 0:
    st.markdown("### 🧠 Opener Question")
    st.write(
        "Both images below say the same thing: **Same Base. Same Height. Same Area.** "
        "Both get the *area* right. But only one of them describes **height** in a way "
        "that still works no matter how the parallelogram leans. Study both pictures, "
        "then pick the one that's right."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.image("assets/opener_option_A.jpg", caption="Option A", use_container_width=True)
    with col_b:
        st.image("assets/opener_option_B.jpg", caption="Option B", use_container_width=True)
    opener_pick = st.radio(
        "Which image correctly labels the height of a parallelogram?",
        ["Option A", "Option B"], key="opener_pick", index=None,
    )
    if st.button("Check my answer", key="check_opener"):
        attempt("opener")
        if opener_pick == "Option A":
            st.success(
                "Option A is the stronger diagram. Look at BOTH panels: it calls the height "
                "the “perpendicular distance” every time — for the square AND the leaning "
                "parallelogram. It also does exactly what today's lesson warns about: it "
                "labels the slanted side by name and tells you flat-out, “NOT the height and "
                "NOT used for area.” That's the exact trap you'll see later today in the barn "
                "window problem."
            )
        else:
            st.info(
                "Option B isn't wrong about the *area* — but look closely at its 'Before' "
                "label: it calls the height the “right side.” That description only happens "
                "to work because a square has a vertical right side. The moment the shape "
                "leans (the 'After' picture), “right side” stops meaning anything, so the "
                "label has to switch definitions mid-problem. A correct rule for height has "
                "to work in BOTH pictures without changing — compare it with Option A."
            )
    box(
        "literacy",
        "📖 WHY THIS MATTERS",
        "The height of a parallelogram is always the <b>perpendicular</b> distance between "
        "the base and the opposite side — never a side's position (like &ldquo;right "
        "side&rdquo;), and never the slanted side. Keep that one rule in your head all day.",
    )
    st.markdown("---")
    box(
        "observer",
        "🔎 TODAY'S FOCUS — continued from Day 8",
        "<p style='margin:0'>Day 8 proved the big idea: a parallelogram is a rectangle in disguise, so "
        "Area = base × height, using the perpendicular height and never the slant. Today doesn't teach "
        "a new idea — it's the i-Ready <b>Refine</b> session: guided practice on that same idea, a set "
        "of Additional Practice problems, and the Lesson 1 Quiz. Watch specifically for two things the "
        "book flags by name: multiplying the base by the <i>slanted side</i> instead of the height "
        "(Juanita's mistake), and forgetting that a parallelogram has <b>two</b> valid base/height "
        "pairs — one for each pair of parallel sides — that both give the same area.</p>",
    )
    read_aloud(
        "Yesterday you proved that a leaning parallelogram is really a rectangle wearing a costume. "
        "Today we put that idea to work on the exact same kinds of problems you'll see on your quiz — "
        "including a mistake another student made, so you can catch it before it becomes your mistake."
    )
    box(
        "literacy",
        "📖 QUICK REVIEW",
        "<b>Area of a parallelogram = base × height</b>, where the height is the <b>perpendicular</b> "
        "distance between the base and the opposite side — never the slanted side length, and never a "
        "diagonal drawn across the inside of the shape.",
    )
    ask_the_class("A parallelogram problem gives you three numbers: a base, a height, and a slanted "
                   "side. How many of those three do you actually multiply?")
    box("tools", "Today's tools",
        "Worktext / journal &middot; pencil &middot; today's Additional Practice page &middot; the "
        "Lesson 1 Quiz &middot; calculator only if your teacher allows it for the mixed-number problem.")

# ======================================================================
# STEP 1 — Apply It: finish Session 2 (problems 6, 7, 8)
# ======================================================================
elif step == 1:
    st.write("**i-Ready Session 2 — Apply It.** Use what you learned to solve these three problems, "
             "exactly as they appear in the worktext.")

    st.markdown("### Problem 6 — Spinach Pie")
    itext_source("Worktext text",
                  "Cyrus makes Greek spinach pie, called spanakopita, with his grandfather. They cut the "
                  "pie into pieces shaped like parallelograms. The dimensions of one piece are shown: "
                  "base 8 cm, height 4.5 cm. What is the area of the top of this piece of spinach pie?")
    st.pyplot(draw_labeled_parallelogram(8, 4.5, 2.5, base_label="8 cm", height_label="4.5 cm"), use_container_width=False)
    g6 = st.number_input("Area (cm²):", min_value=0.0, step=0.5, key="apply6")
    if st.button("Check Problem 6", key="check6"):
        n = attempt("apply6")
        if abs(g6 - 36) < 0.01:
            st.success("Correct! A = b · h = 8 · 4.5 = 36 cm².")
        else:
            st.error("Not yet — multiply the base by the height.")
            if n >= 2:
                explain("Redo help", ["A = b · h", "A = 8 · 4.5", "A = <b>36 cm²</b>"])

    st.markdown("### Problem 7 — Select All That Apply")
    itext_source("Worktext text", "A parallelogram has an area of 48 square units. Which dimensions "
                  "could it have? Select all that apply.")
    options = {
        "A. base = 8 units, height = 6 units": True,
        "B. height = 24 units, base = 24 units": False,
        "C. base = 4 units, height = 12 units": True,
        "D. base = 12 units, height = 36 units": False,
        "E. height = 4 units, base = 12 units": True,
    }
    picks = []
    for label in options:
        if st.checkbox(label, key=f"opt7_{label}"):
            picks.append(label)
    if st.button("Check Problem 7", key="check7"):
        n = attempt("apply7")
        correct = {k for k, v in options.items() if v}
        chosen = set(picks)
        if chosen == correct:
            st.balloons()
            st.success("Correct! A, C, and E each multiply to 48. B gives 576 (24 × 24) and D gives 432 "
                       "(12 × 36) — both too big.")
        else:
            st.error("Not quite — multiply each pair and see which ones equal exactly 48.")
            if n >= 2:
                explain("Redo help", [
                    "A: 8 × 6 = 48 ✔", "B: 24 × 24 = 576 ✘ (added instead of multiplying is a common slip)",
                    "C: 4 × 12 = 48 ✔", "D: 12 × 36 = 432 ✘", "E: 4 × 12 = 48 ✔",
                ])

    st.markdown("### Problem 8 — Grid Parallelogram")
    itext_source("Worktext text", "What is the area of the parallelogram shown on the grid? "
                  "(The book's possible work: area of parallelogram = area of rectangle = 5 × 3 = 15.)")
    st.pyplot(draw_labeled_parallelogram(5, 3, 1.5, base_label="5 units", height_label="3 units"), use_container_width=False)
    g8 = st.number_input("Area (square units):", min_value=0, step=1, key="apply8")
    if st.button("Check Problem 8", key="check8"):
        n = attempt("apply8")
        if g8 == 15:
            st.success("Correct! The parallelogram rearranges into a 5 × 3 rectangle — 15 square units.")
        else:
            st.error("Not yet — 15 is the target. Try decomposing it into a rectangle first.")
            if n >= 2:
                explain("Redo help", ["area of parallelogram = area of rectangle", "= 5 × 3", "= <b>15</b>"])
    pair_share("How did decomposing the grid parallelogram into a rectangle help you find its area?")

# ======================================================================
# STEP 2 — Refine: worked example (mixed number)
# ======================================================================
elif step == 2:
    st.write("**i-Ready Session 3 — Refine, Example.** The Refine session starts with a fully worked "
             "example so you can see the whole method laid out before you try one yourself.")
    read_aloud(
        "Refine problems still use A = base times height — they just dress the numbers up a little. "
        "Watch what happens when the base is a mixed number instead of a whole number."
    )
    st.markdown("### Example — base = 9¼ ft, height = 4 ft")
    st.pyplot(draw_refine_example(), use_container_width=False)
    consider_this("How can you rewrite the mixed number 9¼ so it's easier to multiply by 4?")
    box("method", "Possible work (from the worktext)",
        "A = b · h<br>"
        "= 9¼ · 4<br>"
        "= (9 + ¼) · 4<br>"
        "= 9 · 4 + ¼ · 4<br>"
        "= 36 + 1<br>"
        "= <b>37</b>")
    st.success("The area of the parallelogram is 37 ft².")
    pair_share("How could you solve this problem another way?")
    box(
        "existing",
        "🧠 WHY THIS WORKS",
        "Breaking 9¼ into 9 + ¼ and multiplying each part by 4 separately (the <b>distributive "
        "property</b>) is exactly the same move as decomposing a parallelogram into rectangles — you're "
        "just doing it with numbers instead of shapes.",
    )
    st.markdown("#### Now you try: same idea, new numbers")
    yb = st.selectbox("Pick a mixed-number base:", ["7½", "5¼", "10¾"], key="refine_base_pick")
    yh = st.slider("Height (ft):", 2, 8, 4, key="refine_height_pick")
    frac_map = {"7½": (7, 1, 2), "5¼": (5, 1, 4), "10¾": (10, 3, 4)}
    whole, num, den = frac_map[yb]
    true_area = (whole + num / den) * yh
    st.pyplot(draw_labeled_parallelogram(whole + num / den, yh, 1.5, base_label=f"{yb} ft", height_label=f"{yh} ft"),
              use_container_width=False)
    ga = st.number_input("Area (ft²):", min_value=0.0, step=0.25, key="refine_check")
    if st.button("Check my area", key="refine_check_btn"):
        n = attempt("refine_ex")
        if abs(ga - true_area) < 0.01:
            st.balloons()
            st.success(f"Correct! {yb} × {yh} = {true_area:g} ft².")
        else:
            st.error("Not yet — split the mixed number into a whole number plus a fraction, then "
                     "multiply each part by the height.")
            if n >= 2:
                explain("Redo help", [
                    f"A = ({whole} + {num}/{den}) × {yh}",
                    f"= {whole} × {yh} + ({num}/{den}) × {yh}",
                    f"= <b>{true_area:g} ft²</b>",
                ])

# ======================================================================
# STEP 3 — Refine problem 3: Juanita's mistake (barn window)
# ======================================================================
elif step == 3:
    st.write("**i-Ready Session 3 — Refine, Problem 3.** This is the problem the book uses to name the "
             "#1 mistake on this whole topic, out loud, by a student's name.")
    itext_source("Worktext text",
                  "A small window in a barn is shaped like a parallelogram. The height of the window is "
                  "half the length of the base of the window. The base of the window is 12 in. The "
                  "length of the other side of the window is 10 in. What is the area of the window?")
    st.pyplot(draw_barn_window(), use_container_width=False)
    consider_this("What are the two dimensions you need to find the area?")

    options8 = {"22 in.²": False, "60 in.²": False, "72 in.²": True, "120 in.²": False}
    pick = st.radio("Choose the area of the window:", list(options8.keys()), key="barn_pick", index=None)
    if st.button("Check my answer", key="check_barn"):
        n = attempt("barn")
        if pick == "72 in.²":
            st.success("Correct! height = 12 ÷ 2 = 6 in. Area = 12 × 6 = 72 in.²")
        else:
            st.error("Not yet — remember, the height is HALF the base, not the 10-in. side.")

    st.markdown("#### Juanita chose D (120 in.²) as her answer. How might she have gotten that?")
    juanita_guess = st.text_area("Type what you think Juanita did wrong:", key="juanita_guess", height=80)
    if st.button("Reveal the worktext's answer", key="reveal_juanita"):
        box("observer", "📕 FROM THE TEACHER EDITION — Error Alert",
            "<b>Possible answer:</b> Juanita multiplied the base by the side length, 10 in., instead of "
            "multiplying the base by the height. 12 × 10 = 120 — that's how she landed on D.")
    pair_share("How could you draw a diagram to show one possible shape of the window?")
    box(
        "literacy",
        "⚠️ THE #1 MISTAKE ON THIS TOPIC — restated",
        "Any time a parallelogram problem gives you a base, a height, AND a third side length, that "
        "third number is a <b>distractor</b>. It is real — it's a true side length of the shape — it is "
        "just never the number you multiply.",
    )

# ======================================================================
# STEP 4 — Additional Practice problems 3-5
# ======================================================================
elif step == 4:
    st.write("**Additional Practice, problems 3–5** — the page a student would do for homework "
             "after today's Refine session.")

    st.markdown("### Problem 3 — The Tiled-Wall Mirror")
    itext_source("Worktext text",
                  "The parallelogram shown on the grid represents a mirror. The mirror hangs on a wall "
                  "that is covered with square tiles. Each grid square represents one tile. The side "
                  "length of each square tile is 4 in. What is the area of the mirror?")
    st.pyplot(draw_tiled_mirror(), use_container_width=False)
    g_mirror = st.number_input("Area of the mirror (in.²):", min_value=0, step=1, key="mirror_area")
    if st.button("Check mirror area", key="check_mirror"):
        n = attempt("mirror")
        if g_mirror == 480:
            st.balloons()
            st.success("Correct! base = 5 tiles × 4 in. = 20 in., height = 6 tiles × 4 in. = 24 in. "
                       "Area = 20 × 24 = 480 in.²")
        else:
            st.error("Not yet — convert tiles to inches first (multiply by 4), THEN multiply base by height.")
            if n >= 2:
                explain("Redo help", [
                    "base = 5 tiles, so b = 5 · 4 = 20",
                    "height = 6 tiles, so h = 6 · 4 = 24",
                    "Area = b · h = 20 · 24 = <b>480 in.²</b>",
                ])

    st.markdown("### Problem 4 — Which Side Is the Base?")
    itext_source("Worktext text",
                  "Suppose you want to find the area of the parallelogram. Explain how you know which "
                  "lengths to use as the base and height in the area formula. (Sides shown: 5 cm and "
                  "6.5 cm; the height drawn from the top vertex is 5.2 cm.)")
    st.pyplot(draw_identify_base_height(), use_container_width=False)
    explain_text = st.text_area("Explain, in your own words, which side is the base and why:", key="explain4", height=80)
    if st.button("Compare with the worktext", key="check4"):
        box("existing", "📕 POSSIBLE ANSWER (from the Teacher Edition)",
            "Either the 5-cm side or the 6.5-cm side could be the base. But only the 5-cm side has a "
            "line segment drawn perpendicular to it. So, the 5-cm side is the base. The line segment "
            "perpendicular to the base measures 5.2 cm. That is the height.")
    ask_the_class("What visual clue in the diagram tells you which segment is the true height, before "
                  "you even read any numbers?")

    st.markdown("### Problem 5 — Eagle Express Logo")
    itext_source("Worktext text",
                  "The Eagle Express Shipping Service logo is in the shape of a parallelogram. The side "
                  "lengths of the logo painted on a delivery truck are shown: 3.2 ft and 3.1 ft. The "
                  "perpendicular distance from the bottom of the logo to the top of the logo is 3 ft. "
                  "What is the area of the logo on the truck?")
    st.pyplot(draw_eagle_logo(), use_container_width=False)
    g_eagle = st.number_input("Area of the logo (ft²):", min_value=0.0, step=0.1, key="eagle_area")
    if st.button("Check logo area", key="check_eagle"):
        n = attempt("eagle")
        if abs(g_eagle - 9.3) < 0.05:
            st.balloons()
            st.success("Correct! Area = base × height = 3.1 × 3 = 9.3 ft². The 3.2-ft side is the distractor.")
        else:
            st.error("Not yet — use the 3.1-ft base and the 3-ft perpendicular height. The 3.2-ft side "
                     "is not used at all.")
            if n >= 2:
                explain("Redo help", ["Area = base × height", "Area = 3.1 × 3", "= <b>9.3 ft²</b>"])

# ======================================================================
# STEP 5 — Engage / Explore / Enrich
# ======================================================================
elif step == 5:
    st.markdown("#### Engage / Explore / Enrich stations")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown(
            """
            <div class="box box-tools">
            <span class="pill">Engage · with teacher</span>
            <i>Still reaching for the slant or a diagonal instead of the true height.</i><br><br>
            1. Use the Hands-On Activity: cut a 12-by-5 rectangle along a slanted segment, slide the
            triangle, and confirm the parallelogram it forms still has base 12, height 5, area 60.<br>
            2. Redo the barn window (Refine #3) together and circle the right-angle mark before
            multiplying anything.<br>
            3. Additional Practice, problem 3 only.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            """
            <div class="box box-existing">
            <span class="pill">Explore · independent</span>
            <i>Comfortable with whole-number base × height, ready for mixed numbers and distractors.</i><br><br>
            1. Additional Practice, problems 3–5.<br>
            2. Lesson 1 Quiz, problems 1–3.<br>
            3. <a href="https://www.ixl.com/math/grade-6/area-of-parallelograms" target="_blank" rel="noopener noreferrer">📝 HMWK — IXL <b>GG.4</b>: Area of parallelograms</a>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            """
            <div class="box box-method">
            <span class="pill">Enrich · two bases, one shape</span>
            <i>Fluent with base × height, ready for Quiz problem 5's twist.</i><br><br>
            1. A parallelogram has area 24 sq units. One pair of sides is 36 units; the other pair is
            4 units. Find BOTH possible heights (one for each base choice).<br>
            2. Explain why both answers describe the very same parallelogram.<br>
            3. Full Lesson 1 Quiz, problems 1–5.
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.pyplot(draw_two_bases_parallelogram(), use_container_width=False)
    box("existing", "✏️ Homework reminder",
        "Show ALL work by hand — pencil and paper (graph paper is best), written out in your math "
        "notebook, and mark the right-angle height on every diagram before multiplying.")
    st.markdown("**Board self-check** — which board are you on?")
    board = st.radio("Board", ["Engage", "Explore", "Enrich"], horizontal=True, key="board_pick", label_visibility="collapsed")
    st.info(f"{name or 'You'} → **{board}** board. Grab your worksheet and go.")

# ======================================================================
# STEP 6 — Lesson 1 Quiz, problems 1-3
# ======================================================================
elif step == 6:
    st.write("**Lesson 1 · Quiz — Problems 1–3.** Same rules as the paper quiz: show your work, "
             "circle your final answer.")

    st.markdown("### Problem 1 (1 point)")
    itext_source("Worktext text", "What is the area of the parallelogram in square centimeters? "
                  "(base 9 cm, height 8 cm; a 10 cm side and a 17 cm diagonal are shown but not used.)")
    st.pyplot(draw_quiz1_parallelogram(), use_container_width=False)
    q1 = st.number_input("Area (cm²):", min_value=0, step=1, key="quiz1_1")
    if st.button("Check Problem 1", key="qcheck1"):
        n = attempt("quiz1")
        if q1 == 72:
            st.success("Correct! 9 × 8 = 72 cm². Neither the 10 cm side nor the 17 cm diagonal is used.")
        else:
            st.error("Not yet — multiply the 9 cm base by the 8 cm height only.")
            if n >= 2:
                explain("Redo help", ["A = b · h", "A = 9 · 8", "= <b>72 cm²</b>"])

    st.markdown("### Problem 2 (1 point)")
    itext_source("Worktext text",
                  "A kitchen wall tile is shaped like a parallelogram. The base of the tile is two times "
                  "the height of the tile. The height of the tile is 2.5 in. The length of the other "
                  "side of the tile is 3 in. What is the area of the tile?")
    st.pyplot(draw_kitchen_tile(), use_container_width=False)
    q2 = st.radio("Choose the area:", ["7.5 in.²", "8 in.²", "12.5 in.²", "15 in.²"], key="quiz1_2", index=None)
    if st.button("Check Problem 2", key="qcheck2"):
        n = attempt("quiz2")
        if q2 == "12.5 in.²":
            st.success("Correct! base = 2 × 2.5 = 5 in. Area = 5 × 2.5 = 12.5 in.² The 3-in. side is not used.")
        else:
            st.error("Not yet — find the base first (it's 2 times the height), then multiply base × height.")
            if n >= 2:
                explain("Redo help", ["height = 2.5 in.", "base = 2 × 2.5 = 5 in.", "Area = 5 × 2.5 = <b>12.5 in.²</b>"])

    st.markdown("### Problem 3 (2 points)")
    itext_source("Worktext text", "Find the area of the parallelogram. Show your work. "
                  "(base = 6⅕ ft, height = 5 ft.)")
    st.pyplot(draw_quiz3_parallelogram(), use_container_width=False)
    q3 = st.number_input("Area (ft²):", min_value=0.0, step=0.5, key="quiz1_3")
    if st.button("Check Problem 3", key="qcheck3"):
        n = attempt("quiz3")
        if abs(q3 - 31) < 0.01:
            st.balloons()
            st.success("Correct! A = 6⅕ · 5 = (6 + ⅕) · 5 = 6·5 + ⅕·5 = 30 + 1 = 31 ft².")
        else:
            st.error("Not yet — split 6⅕ into 6 + ⅕, multiply each part by 5, then add.")
            if n >= 2:
                explain("Redo help", ["A = b · h = 6⅕ · 5", "= (6 + ⅕) · 5",
                                       "= 6·5 + ⅕·5 = 30 + 1", "= <b>31 ft²</b>"])

# ======================================================================
# STEP 7 — Lesson 1 Quiz, problems 4-5
# ======================================================================
elif step == 7:
    st.write("**Lesson 1 · Quiz — Problems 4–5.** These two carry the most points on the quiz — "
             "take your time.")

    st.markdown("### Problem 4 (2 points) — Sayali's Sidewalk-Chalk Design")
    itext_source("Worktext text",
                  "Sayali drew the design shown with sidewalk chalk. The design has four identical "
                  "shaded parallelograms joined together. Each parallelogram has a base of 12 in. and a "
                  "height of 21 in. What is the area, in square inches, of the unshaded part of Sayali's "
                  "design? (The whole design is a 42 in. × 48 in. rectangle.)")
    st.pyplot(draw_sayali_design(), use_container_width=False)
    q4 = st.number_input("Area NOT shaded (in.²):", min_value=0, step=1, key="quiz1_4")
    if st.button("Check Problem 4", key="qcheck4"):
        n = attempt("quiz4")
        if q4 == 1008:
            st.balloons()
            st.success("Correct! Each parallelogram = 12 × 21 = 252 in.². Shaded total = 4 × 252 = "
                       "1,008 in.². Whole design = 42 × 48 = 2,016 in.². Unshaded = 2,016 − 1,008 = "
                       "1,008 in.².")
        else:
            st.error("Not yet — find the shaded area first, then subtract it from the whole rectangle's area.")
            if n >= 2:
                explain("Redo help", [
                    "Area of each parallelogram: 12 · 21 = 252",
                    "Area that is shaded: 4 · 252 = 1,008",
                    "Area of design: 42 · 48 = 2,016",
                    "Area that is NOT shaded: 2,016 − 1,008 = <b>1,008 in.²</b>",
                ])

    st.markdown("### Problem 5 (2 points) — Two Bases, Same Parallelogram")
    itext_source("Worktext text",
                  "The area of a parallelogram is 24 square units. One side of the parallelogram is 36 "
                  "units long. The other side is 4 units long. Which measurements could be the "
                  "parallelogram's height? Choose all the correct answers.")
    st.pyplot(draw_two_bases_parallelogram(), use_container_width=False)
    options5 = {
        "A. ⅙ unit": False,
        "B. ⅔ unit": True,
        "C. 1½ units": False,
        "D. 6 units": True,
        "E. 9 units": False,
    }
    picks5 = []
    for label in options5:
        if st.checkbox(label, key=f"opt5_{label}"):
            picks5.append(label)
    if st.button("Check Problem 5", key="qcheck5"):
        n = attempt("quiz5")
        correct = {k for k, v in options5.items() if v}
        if set(picks5) == correct:
            st.balloons()
            st.success("Correct! If 36 units is the base: 24 ÷ 36 = ⅔ unit. If 4 units is the base: "
                       "24 ÷ 4 = 6 units. Both are true heights of the SAME parallelogram — one for each "
                       "pair of parallel sides.")
        else:
            st.error("Not yet — try dividing 24 by each side length (36 and 4) separately.")
            if n >= 2:
                explain("Redo help", [
                    "If base = 36: height = 24 ÷ 36 = <b>⅔ unit</b> (choice B)",
                    "If base = 4: height = 24 ÷ 4 = <b>6 units</b> (choice D)",
                    "A parallelogram has two pairs of parallel sides — each pair has its own base/height "
                    "pair, but multiplying either pair gives the SAME area.",
                ])
    box(
        "existing",
        "🧠 THE BIG IDEA IN PROBLEM 5",
        "Every parallelogram has <b>two</b> correct base-and-height pairs, one for each pair of parallel "
        "sides. Area = 24 no matter which pair you use — that's why both ⅔ unit and 6 units are "
        "correct.",
    )

# ======================================================================
# STEP 8 — Math Journal, Error Alert, End of Lesson Checklist
# ======================================================================
elif step == 8:
    read_aloud(
        "Look for parallelograms that have dimensions correctly labeled as the base and height that "
        "will give an area of 12 square centimeters when multiplied."
    )
    box(
        "literacy",
        "⚠️ ERROR ALERT — straight from the Teacher Edition",
        "If students label two consecutive sides of their parallelograms with factors of 12 (instead of "
        "labeling a base and the corresponding height), that's the error to watch for. Every parallelogram "
        "you draw for the journal needs a <b>base</b> and a perpendicular <b>height</b> marked with a "
        "right-angle tick — not just any two side lengths that happen to multiply to 12.",
    )
    st.markdown("#### Math Journal")
    st.caption("Draw your own parallelogram on paper with area 12 cm². Mark the base, mark the height "
               "with a right-angle symbol, and label both so they multiply to 12.")
    j_base = st.number_input("My base (cm):", min_value=0.1, step=0.5, value=4.0, key="journal_base")
    j_height = st.number_input("My height (cm):", min_value=0.1, step=0.5, value=3.0, key="journal_height")
    j_area = j_base * j_height
    st.pyplot(draw_labeled_parallelogram(j_base, j_height, min(1.5, j_base * 0.3), base_label=f"{j_base:g} cm",
                                          height_label=f"{j_height:g} cm"), use_container_width=False)
    st.write(f"Your area: **{j_area:g} cm²**")
    if abs(j_area - 12) < 0.01:
        st.balloons()
        st.success("That's exactly 12 cm² — nice work choosing a true base/height pair!")
    else:
        st.info("Adjust the base or height until base × height = 12 exactly.")
    j = st.text_area("Journal sentence (optional — write it on paper too):", height=80, key="journal9")
    if j.strip():
        st.success("Journaled. Hand-drawn version goes in your notebook.")

    st.markdown("---")
    st.markdown("#### End of Lesson Checklist")
    checklist = [
        "I can decompose a parallelogram into rectangles and rearrange the pieces.",
        "I can find a parallelogram's area with Area = base × height.",
        "I can identify the true perpendicular height and ignore a slanted-side or diagonal distractor.",
        "I know a parallelogram has two valid base/height pairs, one per pair of parallel sides.",
        "I can explain, in writing, how I know which side is the base in a diagram.",
    ]
    checked = 0
    for i, item in enumerate(checklist):
        if st.checkbox(item, key=f"eol_{i}"):
            checked += 1
    st.progress(checked / len(checklist))
    if checked == len(checklist):
        st.success(f"{name or 'Mathematician'}, you've checked off every goal for Lesson 1!")

    st.markdown("---")
    icans = [
        ("REFINE", "I can apply Area = base × height to mixed numbers and multi-step problems. (6.G.A.1)"),
        ("PRECISION", "I can catch a base-times-slant mistake like Juanita's before I make it. (MP.6)"),
        ("STRUCTURE", "I can see that a parallelogram has two honest base/height pairs. (MP.2, MP.5)"),
        ("REASONING", "I can explain in writing which side is the base and why. (MP.4)"),
    ]
    for tag, text in icans:
        st.markdown(f'<div class="box box-existing" style="border-left:6px solid {GOLD};padding:0.7rem 1rem;">'
                     f'<span class="pill" style="background:{NAVY};">{tag}</span>{text}</div>', unsafe_allow_html=True)
    st.caption(
        "Standards in play: 6.G.A.1 (grade-level — area of a parallelogram) · 3.MD.C.7d "
        "(foundational — decomposing into rectangles) · MP.2 (reason abstractly/quantitatively) · "
        "MP.4 (model with mathematics) · MP.5 (use tools strategically) · MP.6 (attend to "
        "precision)."
    )
    st.markdown(
        f"""
        <div class="box box-tools">
        Lesson 1 is done — decomposed, modeled, practiced, and quizzed. You proved a parallelogram is a
        rectangle in disguise, and you know exactly where the trap doors are: the slant, the diagonal,
        and picking a base without its matching height.
        <br><br><b>{name or 'Mathematician'}, tomorrow that same rectangle-in-disguise trick is hiding
        inside a triangle.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
c_back, c_next = st.columns([1, 1])
if c_back.button("⬅ Back", disabled=(step == 0)):
    st.session_state.step = max(0, step - 1)
    st.rerun()
if c_next.button("Next ➡", disabled=(step == len(steps) - 1)):
    st.session_state.step = min(len(steps) - 1, step + 1)
    st.rerun()

st.caption("Standards in play: 6.G.A.1 (area of a parallelogram) · 3.MD.C.7d (decompose into "
           "rectangles — foundational) · MP.2, MP.4, MP.5, MP.6.")
st.markdown(
    "<div class='credit'>www.cognitivecloud.ai &middot; Developed by Xavier Honablue, M.Ed &middot; "
    "Chandler Park Academy</div>",
    unsafe_allow_html=True,
)
