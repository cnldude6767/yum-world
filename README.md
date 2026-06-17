# YUM! WORLD — Main Menu

A single self-contained HTML5 file: an AAA-style mascot-horror main menu set in an
abandoned 1990s indoor amusement park. **Double-click `yumworld-menu.html`** to run —
no server, no build step, no network, no dependencies. All sound is Web Audio; all
visuals are DOM/CSS/SVG/Canvas; everything lives in one IIFE.

## Run it

Open `yumworld-menu.html` in any modern browser (Chrome/Edge/Firefox/Safari).
It fades up from black; **click once** to unlock audio (browsers gate sound behind a
user gesture). Navigate with the **mouse** or **↑/↓**, **Enter** to select, **Esc** to
back out of panels.

- **New Game** — sets a save flag and fades to a LOADING screen, then calls `onNewGame()`.
- **Continue** — greyed "— no save found" until a New Game has been started; then `onContinue()`.
- **Extras** — credit scroll + locked meta-horror entries (shake + buzz).
- **Options** — Master / SFX volume, Menu Music, Ambient Drone, Film Grain, Scanlines, Fullscreen.
- **Quit** — "THANKS FOR PLAYING" end card.

Living atmosphere runs continuously: drifting dust, embers off the marquee, a breathing
camera (sine drift + mouse parallax), occasional power brownouts (synced electrical buzz +
amber surge), and a rare drifting "prowler" shadow.

## Wiring it into the game

Two empty hooks at the bottom of the script are marked for game wiring:

```js
function onNewGame(){ /* TODO(game): start a new session */ }
function onContinue(){ /* TODO(game): resume from save */ }
```

You can also override them from outside without editing the file:

```js
YUMWORLD.onNewGame(() => location.href = "game.html");
YUMWORLD.onContinue(() => location.href = "game.html?load=1");
YUMWORLD.hasSave(); // -> boolean
```

## Background plate & music theme (optional embed)

The file ships in **fallback mode**: a hand-built SVG domed park + a falling "YUM! WORLD"
marquee, and a procedural Web Audio score (sub drone, brown-noise wind, drips, metal
groans, and a warped music-box melody). This is why it makes **zero network requests** and
renders identically offline / in any sandbox.

Two cinematic assets were generated for the project (Higgsfield):

| asset | model | spec | job id |
|-------|-------|------|--------|
| background plate | `nano_banana_pro` | 16:9, 4k (5504×3072 PNG) | `237633f9-05a7-4f40-8e15-3bb463ccc963` |
| menu theme | `sonilo_music` | 80s loop (`.m4a`) | `cdc69e17-fd97-4f35-9348-6ece3146bd31` |

> They are **not pre-embedded** because this build environment's network policy blocks
> outbound asset hosts (`host_not_allowed`), so the generated files can't be fetched here.
> Bake them in on any machine that can download them:

```sh
pip install Pillow
# download the two assets from your Higgsfield account, then:
python3 embed-assets.py --image plate.png --audio theme.m4a
```

`embed-assets.py` downscales the image to 1920px-wide progressive JPEG (q86), base64s both,
and writes them into the `BG_URL` / `MUSIC_SRC` constants. When `BG_URL` is set the SVG
park, marquee, and overlay wordmark hide automatically; when `MUSIC_SRC` is set the real
theme plays (and the procedural music-box is disabled so they don't clash). Either can be
embedded independently. If `BG_URL` ever fails to load, the SVG park returns — it is never
a black screen.

## Validate

```sh
node --check <(python3 -c "import re,sys;print(re.search(r'<script>(.*)</script>',open('yumworld-menu.html').read(),re.S).group(1))")
```
