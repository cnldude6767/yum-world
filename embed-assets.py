#!/usr/bin/env python3
"""
embed-assets.py — bake the YUM! WORLD background plate + music theme into
yumworld-menu.html as base64 data URIs (the BG_URL / MUSIC_SRC constants).

The menu is fully playable WITHOUT this step (built-in SVG park + procedural
Web Audio). Run this only to swap in the generated AAA plate / theme.

Pipeline (matches the build spec):
  * image -> downscaled to 1920px wide, progressive JPEG q86, then base64
  * audio -> base64 as-is (mime inferred from extension; .m4a -> audio/mp4)

Usage:
  python3 embed-assets.py --image plate.png --audio theme.m4a
  python3 embed-assets.py --image plate.png            # image only
  python3 embed-assets.py --audio theme.m4a            # audio only
  python3 embed-assets.py --image plate.png --out menu-baked.html

Re-running is safe: it replaces whatever the constants currently hold.

The two assets generated for this project (download from your Higgsfield
account, then point --image / --audio at them):
  image  job 237633f9-05a7-4f40-8e15-3bb463ccc963  (nano_banana_pro, 16:9, 4k)
  audio  job cdc69e17-fd97-4f35-9348-6ece3146bd31  (sonilo_music, 80s, .m4a)
"""
import argparse, base64, io, os, re, sys

HTML_DEFAULT = "yumworld-menu.html"
TARGET_WIDTH = 1920
JPEG_QUALITY = 86

AUDIO_MIME = {
    ".m4a": "audio/mp4", ".mp4": "audio/mp4", ".aac": "audio/aac",
    ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".oga": "audio/ogg",
    ".webm": "audio/webm", ".wav": "audio/wav",
}


def image_data_uri(path):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is required for image embedding:  pip install Pillow")
    im = Image.open(path).convert("RGB")
    if im.width > TARGET_WIDTH:
        h = round(im.height * TARGET_WIDTH / im.width)
        im = im.resize((TARGET_WIDTH, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=JPEG_QUALITY, progressive=True, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    print(f"  image: {im.width}x{im.height} JPEG q{JPEG_QUALITY}  "
          f"-> {len(b64)/1024:.0f} KB base64")
    return "data:image/jpeg;base64," + b64


def audio_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = AUDIO_MIME.get(ext)
    if not mime:
        sys.exit(f"Unknown audio extension '{ext}'. Supported: {', '.join(AUDIO_MIME)}")
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    print(f"  audio: {mime}  -> {len(b64)/1024:.0f} KB base64")
    return f"data:{mime};base64," + b64


def replace_const(html, name, value):
    # matches:  const NAME = "...anything...";
    pattern = re.compile(r'(const\s+%s\s*=\s*)"(?:[^"\\]|\\.)*"' % re.escape(name))
    if not pattern.search(html):
        sys.exit(f"Could not find `const {name} = \"...\"` in the HTML.")
    return pattern.sub(lambda m: m.group(1) + '"' + value + '"', html, count=1)


def main():
    ap = argparse.ArgumentParser(description="Embed plate/theme into yumworld-menu.html")
    ap.add_argument("--image", help="background plate (png/jpg/webp)")
    ap.add_argument("--audio", help="music theme (m4a/mp3/ogg/...)")
    ap.add_argument("--html", default=HTML_DEFAULT, help=f"input HTML (default {HTML_DEFAULT})")
    ap.add_argument("--out", help="output HTML (default: overwrite input)")
    a = ap.parse_args()
    if not a.image and not a.audio:
        ap.error("give --image and/or --audio")

    html = open(a.html, encoding="utf-8").read()
    if a.image:
        html = replace_const(html, "BG_URL", image_data_uri(a.image))
    if a.audio:
        html = replace_const(html, "MUSIC_SRC", audio_data_uri(a.audio))

    out = a.out or a.html
    open(out, "w", encoding="utf-8").write(html)
    print(f"  wrote {out}  ({len(html.encode('utf-8'))/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
