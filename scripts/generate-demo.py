#!/usr/bin/env python3
"""Generate searchlane-demo.mp4 — terminal-style product demo."""
import os
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "--break-system-packages", "-q"])
    from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 15
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
]
FONT = next((p for p in FONT_PATHS if os.path.exists(p)), None)
FONTSIZE = 22
font = ImageFont.truetype(FONT, FONTSIZE) if FONT else ImageFont.load_default()

OUT_DIR = "/tmp/searchlane-frames"
os.makedirs(OUT_DIR, exist_ok=True)

SCRIPT = [
    ("", (180, 180, 190)),
    ("  SearchLane  v0.1.1", (120, 220, 255)),
    ("  Agent Web Search & Research API", (180, 200, 255)),
    ("  github.com/talocode/searchlane  ·  npm i @talocode/searchlane", (140, 140, 160)),
    ("", (180, 180, 190)),
    ('$ searchlane query --query "agent-native APIs"', (80, 220, 140)),
    ("", (180, 180, 190)),
    ("  {", (210, 210, 220)),
    ('    "query": "agent-native APIs",', (210, 210, 220)),
    ('    "provider": "duckduckgo",', (180, 220, 255)),
    ('    "count": 5,', (255, 220, 100)),
    ('    "results": [', (210, 210, 220)),
    ('      { "title": "Agent-native API design", "score": 0.94,', (200, 180, 255)),
    ('        "url": "https://example.com/agent-apis" },', (200, 180, 255)),
    ('      { "title": "MCP tools for agents", "score": 0.88,', (200, 180, 255)),
    ('        "url": "https://example.com/mcp" }', (200, 180, 255)),
    ("    ]", (210, 210, 220)),
    ("  }", (210, 210, 220)),
    ("", (180, 180, 190)),
    ('$ searchlane research --query "What is llms.txt?"', (80, 220, 140)),
    ("", (180, 180, 190)),
    ("  ## Key findings", (255, 220, 100)),
    ("  1. llms.txt helps AI systems understand a site", (210, 210, 220)),
    ("  2. Publish at /llms.txt with key pages + rules", (210, 210, 220)),
    ("  3. Pairs with robots.txt for crawler access", (210, 210, 220)),
    ("  ## Citations: [1] [2] [3]", (180, 220, 255)),
    ("", (180, 180, 190)),
    ("  ────────────────────────────────────────────", (100, 100, 120)),
    ("  npm install -g @talocode/searchlane", (255, 255, 255)),
    ("  Linux · macOS · Windows · Android · iOS (Node)", (180, 200, 220)),
    ("  Cloud: POST /v1/searchlane/query · 5 credits", (160, 180, 200)),
    ("  ────────────────────────────────────────────", (100, 100, 120)),
]


def render(up_to: int):
    img = Image.new("RGB", (W, H), (12, 14, 22))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 48], fill=(22, 28, 42))
    draw.text((24, 10), "● ● ●   searchlane — agent search terminal", font=font, fill=(120, 130, 150))
    y = 70
    for i, (text, color) in enumerate(SCRIPT):
        if i > up_to:
            break
        draw.text((32, y), text, font=font, fill=color)
        y += 28
    return img


frame_idx = 0
for current in range(len(SCRIPT)):
    for _ in range(4):
        render(current).save(f"{OUT_DIR}/frame_{frame_idx:05d}.png")
        frame_idx += 1
for _ in range(FPS * 3):
    render(len(SCRIPT) - 1).save(f"{OUT_DIR}/frame_{frame_idx:05d}.png")
    frame_idx += 1

print(f"Generated {frame_idx} frames", file=sys.stderr)
out_mp4 = os.environ.get(
    "SEARCHLANE_DEMO_OUT",
    os.path.join(os.path.dirname(__file__), "..", "release-assets", "searchlane-demo.mp4"),
)
os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True)
subprocess.check_call(
    [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{OUT_DIR}/frame_%05d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
        "-movflags", "+faststart",
        out_mp4,
    ]
)
print(out_mp4)
