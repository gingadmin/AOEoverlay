# ⚔️ AoE2 Build Order Overlay

A lightweight, always-on-top Python overlay for **Age of Empires II: Definitive Edition** that guides you through villager build orders step by step — without ever leaving the game.

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)

---

## Download

**Just want to run it?** Grab the latest `aoe2_overlay.exe` from the [Releases page](../../releases) — no Python install required. Just double-click and go.

**Want to run from source or add your own build orders?** See the [Installation](#installation) section below.

## Features

- **5 build orders** included out of the box
- **Global hotkeys** — navigate steps while AoE2 has focus (no alt-tabbing)
- Always-on-top, no title bar, semi-transparent
- Color-coded by Age (Dark / Feudal / Castle / Imperial)
- Villager counts per resource at every step
- Progress dots so you can see how far along you are
- Draggable — place it anywhere on screen
- Tiny footprint — single Python file, one dependency

---

## Build Orders Included

| Short | Full Name | Style |
|---|---|---|
| FC | Fast Castle | Economic, ~21 pop |
| Scouts | Scouts Rush | Aggressive, Feudal cavalry |
| Archers | Archer Rush | Aggressive, Feudal ranged |
| MAA | Men-at-Arms + Archers | Flush, versatile |
| Boom | Fast Castle Boom | Economic, late game |

---

## Requirements

- Python 3.7+
- `pynput` (for global hotkeys)


---

## Installation

### Option A — Download the .exe *(easiest)*

1. Go to the [Releases page](../../releases)
2. Download `aoe2_overlay.exe` from the latest release
3. Double-click it — that's it

No Python, no Command Prompt, nothing else to install.

---

### Option B — Run from source

**1. Install Python** (if you don't have it)

Download from [python.org/downloads](https://www.python.org/downloads/) and run the installer.
> ⚠️ On the first screen, check **"Add Python to PATH"** before clicking Install.

**2. Download this repo**

Click the green **Code** button on this page → **Download ZIP** → extract the folder somewhere (e.g. your Desktop).

**3. Navigate to the folder in Command Prompt**

Open **Command Prompt** (`Win + R` → type `cmd` → Enter), then type `cd` followed by the path to the extracted folder. For example:

```
cd C:\Users\Paul\Desktop\aoe2-overlay
```

> 💡 Tip: you can drag the folder from File Explorer into the Command Prompt window and it will paste the path for you.

**4. Install dependencies**

Now that Command Prompt is in the right folder, run:

```
pip install -r requirements.txt
```

**5. Run the overlay**

```
python aoe2_overlay.py
```

Or just double-click `aoe2_overlay.py` in File Explorer if Python is associated with `.py` files on your system.

---

## Controls

| Input | Action |
|---|---|
| `Page Down` | Next step *(works while in-game)* |
| `Page Up` | Previous step *(works while in-game)* |
| `↑` / `↓` arrow keys | Switch build order |
| `←` / `→` arrow keys | Previous / next step *(overlay focused)* |
| Click nav buttons | Previous / next step |
| Click a dot | Jump to any step |
| **Drag** | Move the overlay window |
| **Right-click** | Close |

### Why Page Up / Page Down?

These keys are not bound by AoE2's default hotkey scheme, so they won't interfere with gameplay. The global listener (`pynput`) captures them system-wide, meaning they work even while the game window has focus.

**Want different hotkeys?** Edit these two lines near the top of `aoe2_overlay.py`:

```python
HOTKEY_NEXT = pynput_kb.Key.page_down
HOTKEY_PREV = pynput_kb.Key.page_up
```

Other safe options: `Key.f9`, `Key.f10`, `Key.f12`, `Key.insert`

---

## Adding Your Own Build Orders

Build orders are defined as a plain Python list near the top of `aoe2_overlay.py`. Each entry looks like this:

```python
{
    "name": "My Build Order",
    "tags": "Aggressive · ~20 pop",
    "steps": [
        {"pop": 3, "F": 3, "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep."},
        {"pop": 4, "F": 4, "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build House."},
        # ... more steps
        {"pop": 21, "F": 11, "W": 6, "G": 4, "S": 0, "age": "Feudal", "note": "➜ CLICK FEUDAL AGE!"},
    ],
}
```

**Fields:**

| Field | Description |
|---|---|
| `pop` | Total population at this step |
| `F` | Villagers on Food |
| `W` | Villagers on Wood |
| `G` | Villagers on Gold |
| `S` | Villagers on Stone |
| `age` | `"Dark"`, `"Feudal"`, `"Castle"`, or `"Imperial"` |
| `note` | Instruction shown on screen |

Steps containing `➜` or `CLICK` are highlighted in orange automatically.

Also add a short label to the `BO_SHORT` list so the tab fits in the window:

```python
BO_SHORT = ["FC", "Scouts", "Archers", "MAA", "Boom", "MyBO"]
```

---

## Not affiliated with Microsoft or Ensemble Studios. Age of Empires II is a trademark of Microsoft Corporation.

