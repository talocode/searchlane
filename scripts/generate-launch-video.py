#!/usr/bin/env python3
"""
SearchLane launch video.
Arc: Hook → Reveal → Points 1-3 → Proof → CTA
Kinetic typography motion graphics, 16:9.
"""
from __future__ import annotations

import math
import os
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "pillow", "--break-system-packages", "-q"]
    )
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 720
FPS = 15
OUT_DIR = "/tmp/searchlane-launch-frames"
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette (Talocode-adjacent: deep navy + electric cyan + hot magenta accent)
BG = (6, 8, 18)
BG2 = (12, 16, 36)
CYAN = (0, 229, 255)
MAGENTA = (255, 45, 149)
WHITE = (245, 247, 255)
MUTED = (140, 150, 180)
LIME = (80, 255, 160)
GOLD = (255, 210, 90)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]
FONT_BOLD = next((p for p in FONT_PATHS if os.path.exists(p) and "Bold" in p), None)
FONT_REG = next((p for p in FONT_PATHS if os.path.exists(p) and "Bold" not in p), FONT_BOLD)


def font(size: int, bold: bool = True):
    path = FONT_BOLD if bold else FONT_REG
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 3 * t * t - 2 * t * t * t


def lerp(a, b, t):
    return a + (b - a) * t


def bg_frame(t_global: float) -> Image.Image:
    """Fast dark gradient + accent bars + grid."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        c = int(8 + 14 * (y / H))
        draw.rectangle([0, y, W, y + 8], fill=(c, c + 2, min(40, c + 16)))
    for i, col in enumerate([CYAN, MAGENTA, LIME]):
        x = int(W * (0.15 + 0.28 * i) + 40 * math.sin(t_global * 0.5 + i))
        dim = tuple(max(0, int(c * 0.22)) for c in col[:3])
        draw.rectangle([x, 0, x + 3, H], fill=dim)
    for x in range(0, W, 100):
        draw.line([(x, 0), (x, H)], fill=(18, 22, 40), width=1)
    for y in range(0, H, 100):
        draw.line([(0, y), (W, y)], fill=(18, 22, 40), width=1)
    return img


def text_size(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def draw_centered(draw, text, y, fnt, fill, opacity=1.0, x_offset=0):
    tw, th = text_size(draw, text, fnt)
    x = (W - tw) // 2 + x_offset
    if opacity < 1.0:
        # approximate with darker blend toward bg
        r, g, b = fill
        fill = (
            int(lerp(BG[0], r, opacity)),
            int(lerp(BG[1], g, opacity)),
            int(lerp(BG[2], b, opacity)),
        )
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + th


def word_reveal(draw, words, y, fnt, fill, progress, gap=18):
    """Reveal words left-to-right based on progress 0..1."""
    total = max(1, len(words))
    shown = int(progress * total + 0.001)
    # measure full line width for centering
    full = " ".join(words)
    tw, th = text_size(draw, full, fnt)
    x = (W - tw) // 2
    for i, w in enumerate(words):
        if i < shown:
            # pop-in scale approx via slight y bounce on newest word
            dy = 0
            if i == shown - 1:
                frac = (progress * total) - i
                dy = int((1 - ease_out_cubic(frac)) * 24)
            draw.text((x, y + dy), w, font=fnt, fill=fill)
        ww, _ = text_size(draw, w + " ", fnt)
        x += ww
    return y + th + 12


# Script beats: Hook → Reveal → Points → Proof → CTA
# (duration_sec, kind, payload)
BEATS = [
    # Hook ~3.5s
    (3.5, "hook", {
        "lines": ["Agents don't need another chatbot.", "They need the web."],
        "sub": "Search is broken for machines.",
    }),
    # Reveal ~4s
    (4.0, "reveal", {
        "title": "SearchLane",
        "tag": "Agent Web Search & Research API",
        "pill": "by Talocode",
    }),
    # Point 1 ~4s
    (4.0, "point", {
        "num": "01",
        "title": "Structured search hits",
        "body": "title · url · snippet · score",
        "cmd": 'searchlane query --query "agent tools"',
        "accent": CYAN,
    }),
    # Point 2 ~4s
    (4.0, "point", {
        "num": "02",
        "title": "Research with citations",
        "body": "multi-source dig → brief + sources",
        "cmd": 'searchlane research --query "llms.txt"',
        "accent": MAGENTA,
    }),
    # Point 3 ~4s
    (4.0, "point", {
        "num": "03",
        "title": "Built for agents",
        "body": "REST · MCP · SDK · CLI · credits",
        "cmd": "POST /v1/searchlane/query  ·  5 credits",
        "accent": LIME,
    }),
    # Proof ~4s
    (4.0, "proof", {
        "stats": [
            ("5cr", "query"),
            ("8cr", "news"),
            ("30cr", "research"),
        ],
        "line": "Pay per call. Brave · Serper · DuckDuckGo.",
    }),
    # CTA ~5s
    (5.0, "cta", {
        "lines": ["Ship search as a product.", "Not a raw model reseller."],
        "cmd": "npm i @talocode/searchlane",
        "url": "github.com/talocode/searchlane",
    }),
]


def render_beat(kind: str, payload: dict, local_t: float, duration: float, global_t: float) -> Image.Image:
    img = bg_frame(global_t)
    draw = ImageDraw.Draw(img, "RGBA")
    # progress within beat 0..1
    p = ease_out_cubic(min(1.0, local_t / max(0.01, duration * 0.35)))
    fade_out = 1.0
    if local_t > duration - 0.35:
        fade_out = ease_in_out((duration - local_t) / 0.35)

    if kind == "hook":
        f1, f2 = font(44), font(44)
        y = int(H * 0.32 + (1 - p) * 40)
        words1 = payload["lines"][0].split()
        words2 = payload["lines"][1].split()
        y = word_reveal(draw, words1, y, f1, WHITE, min(1.0, p * 1.4) * fade_out)
        y += 16
        y = word_reveal(draw, words2, y, f2, CYAN, max(0.0, min(1.0, p * 1.4 - 0.35)) * fade_out)
        if p > 0.6:
            sub_p = (p - 0.6) / 0.4
            draw_centered(draw, payload["sub"], y + 48, font(32, bold=False), MUTED, sub_p * fade_out)

    elif kind == "reveal":
        # logo bar
        bar_w = int(lerp(0, 280, p))
        draw.rounded_rectangle(
            [(W // 2 - bar_w // 2, int(H * 0.28)), (W // 2 + bar_w // 2, int(H * 0.28) + 8)],
            radius=4,
            fill=CYAN + (int(200 * fade_out),) if False else CYAN,
        )
        title = payload["title"]
        f = font(84)
        # glitch/slide
        xoff = int((1 - p) * -120)
        draw_centered(draw, title, int(H * 0.34), f, WHITE, fade_out, x_offset=xoff)
        # cyan underline glow text shadow
        draw_centered(draw, title, int(H * 0.34) + 4, f, CYAN, 0.25 * fade_out, x_offset=xoff)
        tag_p = max(0.0, min(1.0, (p - 0.3) / 0.5))
        draw_centered(draw, payload["tag"], int(H * 0.52), font(40, bold=False), MUTED, tag_p * fade_out)
        pill_p = max(0.0, min(1.0, (p - 0.5) / 0.4))
        # pill
        pill = payload["pill"]
        pf = font(28)
        tw, th = text_size(draw, pill, pf)
        px, py = (W - tw) // 2 - 28, int(H * 0.62)
        alpha = int(255 * pill_p * fade_out)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle(
            [px, py, px + tw + 56, py + th + 24],
            radius=24,
            fill=(MAGENTA[0], MAGENTA[1], MAGENTA[2], int(180 * pill_p * fade_out)),
        )
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        draw.text((px + 28, py + 10), pill, font=pf, fill=WHITE)

    elif kind == "point":
        accent = payload["accent"]
        # big number
        nf = font(120)
        draw_centered(draw, payload["num"], int(H * 0.18 + (1 - p) * 30), nf, accent, fade_out * 0.9)
        draw_centered(draw, payload["title"], int(H * 0.42), font(44), WHITE, fade_out)
        draw_centered(draw, payload["body"], int(H * 0.52), font(26, bold=False), MUTED, fade_out * min(1.0, p * 1.2))
        # terminal card
        card_p = max(0.0, min(1.0, (p - 0.25) / 0.5))
        cmd = payload["cmd"]
        cf = font(28)
        tw, th = text_size(draw, "$ " + cmd, cf)
        cw, ch = tw + 80, th + 48
        cx, cy = (W - cw) // 2, int(H * 0.68)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        oy = cy + int((1 - ease_out_cubic(card_p)) * 40)
        od.rounded_rectangle(
            [cx, oy, cx + cw, oy + ch],
            radius=16,
            fill=(18, 22, 40, int(230 * card_p * fade_out)),
            outline=accent + (int(180 * card_p * fade_out),),
            width=2,
        )
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        if card_p > 0.2:
            draw.text((cx + 32, oy + 16), "$ ", font=cf, fill=LIME)
            # typewriter for command
            chars = int(min(1.0, (local_t - duration * 0.35) / (duration * 0.45)) * len(cmd))
            draw.text((cx + 32 + text_size(draw, "$ ", cf)[0], oy + 16), cmd[: max(0, chars)], font=cf, fill=WHITE)

    elif kind == "proof":
        draw_centered(draw, "Credit-metered. Agent-ready.", int(H * 0.18), font(48), WHITE, fade_out)
        stats = payload["stats"]
        for i, (big, label) in enumerate(stats):
            sp = max(0.0, min(1.0, (p - i * 0.12) / 0.5))
            box_w, box_h = 360, 280
            gap = 48
            total_w = 3 * box_w + 2 * gap
            x0 = (W - total_w) // 2 + i * (box_w + gap)
            y0 = int(H * 0.32 + (1 - ease_out_cubic(sp)) * 50)
            overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.rounded_rectangle(
                [x0, y0, x0 + box_w, y0 + box_h],
                radius=20,
                fill=(16, 20, 38, int(220 * sp * fade_out)),
                outline=(CYAN[0], CYAN[1], CYAN[2], int(120 * sp * fade_out)),
                width=2,
            )
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
            if sp > 0.2:
                bf = font(72)
                tw, th = text_size(draw, big, bf)
                draw.text((x0 + (box_w - tw) // 2, y0 + 70), big, font=bf, fill=GOLD)
                lf = font(32, bold=False)
                tw2, _ = text_size(draw, label, lf)
                draw.text((x0 + (box_w - tw2) // 2, y0 + 180), label, font=lf, fill=MUTED)
        draw_centered(draw, payload["line"], int(H * 0.78), font(32, bold=False), MUTED, fade_out * min(1.0, p))

    elif kind == "cta":
        draw_centered(draw, payload["lines"][0], int(H * 0.28 + (1 - p) * 30), font(56), WHITE, fade_out)
        draw_centered(draw, payload["lines"][1], int(H * 0.38), font(56), CYAN, fade_out * min(1.0, p * 1.3))
        # big install box
        cp = max(0.0, min(1.0, (p - 0.25) / 0.5))
        cmd = payload["cmd"]
        cf = font(42)
        tw, th = text_size(draw, cmd, cf)
        cw, ch = tw + 100, th + 56
        cx, cy = (W - cw) // 2, int(H * 0.55)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle(
            [cx, cy, cx + cw, cy + ch],
            radius=18,
            fill=(0, 229, 255, int(40 * cp * fade_out)),
            outline=(0, 229, 255, int(220 * cp * fade_out)),
            width=3,
        )
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        if cp > 0.15:
            draw.text((cx + 50, cy + 16), cmd, font=cf, fill=WHITE)
        draw_centered(draw, payload["url"], int(H * 0.72), font(32, bold=False), MUTED, fade_out * cp)
        # corner brand
        draw.text((64, H - 64), "Talocode Cloud", font=font(24, bold=False), fill=MUTED)

    return img


def main():
    frames = []
    t = 0.0
    frame_idx = 0
    for duration, kind, payload in BEATS:
        n = int(duration * FPS)
        for i in range(n):
            local_t = i / FPS
            img = render_beat(kind, payload, local_t, duration, t + local_t)
            path = f"{OUT_DIR}/frame_{frame_idx:05d}.png"
            img.save(path, optimize=True)
            frame_idx += 1
        t += duration
        print(f"beat {kind}: {n} frames", file=sys.stderr)

    # hold end 1s
    last = f"{OUT_DIR}/frame_{frame_idx-1:05d}.png"
    for _ in range(FPS):
        import shutil

        shutil.copy(last, f"{OUT_DIR}/frame_{frame_idx:05d}.png")
        frame_idx += 1

    out = os.environ.get(
        "SEARCHLANE_LAUNCH_OUT",
        os.path.join(os.path.dirname(__file__), "..", "release-assets", "searchlane-launch-video.mp4"),
    )
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    print(f"Encoding {frame_idx} frames → {out}", file=sys.stderr)
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            f"{OUT_DIR}/frame_%05d.png",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-movflags",
            "+faststart",
            out,
        ]
    )
    print(out)
    return out


if __name__ == "__main__":
    main()
