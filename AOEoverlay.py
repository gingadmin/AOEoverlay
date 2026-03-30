"""
AoE2 Build Order Overlay
Run: python aoe2_overlay.py
Requires: pip install pynput

Global hotkeys work even while AoE2 has focus.
Page Down = next step   (change HOTKEY_NEXT below)
Page Up   = prev step   (change HOTKEY_PREV below)

Drag the window to move it. Right-click to close.
"""

import tkinter as tk
import threading
from pynput import keyboard as pynput_kb

# ─────────────────────────────────────────────
# HOTKEY CONFIG  (safe keys not used by AoE2)
# Options: Key.page_down, Key.page_up, Key.f9,
#          Key.f10, Key.f12, Key.insert, Key.pause
# ─────────────────────────────────────────────
HOTKEY_NEXT = pynput_kb.Key.page_down
HOTKEY_PREV = pynput_kb.Key.page_up

# ─────────────────────────────────────────────
# BUILD ORDER DATA
# ─────────────────────────────────────────────
BUILD_ORDERS = [
    {
        "name": "Fast Castle",
        "tags": "Economic · ~21 pop",
        "steps": [
            {"pop": 3,  "F": 3,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep under TC."},
            {"pop": 4,  "F": 4,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build a House."},
            {"pop": 5,  "F": 4,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "5th on wood."},
            {"pop": 6,  "F": 5,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "6th on sheep."},
            {"pop": 7,  "F": 5,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "7th on wood. Build a House."},
            {"pop": 8,  "F": 6,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "8th on sheep. Lure Boar 1."},
            {"pop": 9,  "F": 6,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "9th on wood."},
            {"pop": 10, "F": 7,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "10th on berries. Build Mill."},
            {"pop": 11, "F": 8,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "11th on berries."},
            {"pop": 12, "F": 8,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "12th on wood. Build a House."},
            {"pop": 13, "F": 9,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "13th on food. Lure Boar 2."},
            {"pop": 14, "F": 9,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "14th on wood."},
            {"pop": 15, "F": 10, "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "15th on food. Build 2 Farms."},
            {"pop": 16, "F": 10, "W": 5, "G": 1, "S": 0, "age": "Dark",   "note": "16th on gold. Build Mining Camp."},
            {"pop": 17, "F": 11, "W": 5, "G": 1, "S": 0, "age": "Dark",   "note": "17th on food. More farms."},
            {"pop": 18, "F": 11, "W": 5, "G": 2, "S": 0, "age": "Dark",   "note": "18th on gold."},
            {"pop": 19, "F": 11, "W": 5, "G": 3, "S": 0, "age": "Dark",   "note": "19th on gold."},
            {"pop": 20, "F": 11, "W": 6, "G": 3, "S": 0, "age": "Dark",   "note": "20th on wood."},
            {"pop": 21, "F": 11, "W": 6, "G": 4, "S": 0, "age": "Dark",   "note": "21st on gold. ➜ CLICK FEUDAL AGE!"},
            {"pop": 21, "F": 11, "W": 6, "G": 4, "S": 0, "age": "Feudal", "note": "Build Blacksmith + Market. Keep queuing vills."},
            {"pop": 23, "F": 11, "W": 6, "G": 6, "S": 0, "age": "Feudal", "note": "2 new vills to gold."},
            {"pop": 23, "F": 11, "W": 6, "G": 6, "S": 0, "age": "Castle", "note": "800F + 200G ➜ CLICK CASTLE AGE!"},
        ],
    },
    {
        "name": "Scouts Rush",
        "tags": "Aggressive · ~21 pop",
        "steps": [
            {"pop": 3,  "F": 3,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep. Scout the map!"},
            {"pop": 4,  "F": 4,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build House."},
            {"pop": 5,  "F": 4,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "5th on wood."},
            {"pop": 6,  "F": 5,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "6th on sheep."},
            {"pop": 7,  "F": 5,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "7th on wood. Build House."},
            {"pop": 8,  "F": 6,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "8th on food. Lure Boar 1."},
            {"pop": 9,  "F": 6,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "9th on wood."},
            {"pop": 10, "F": 7,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "10th on berries. Build Mill."},
            {"pop": 11, "F": 7,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "11th on wood."},
            {"pop": 12, "F": 8,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "12th on food. Lure Boar 2. Build House."},
            {"pop": 13, "F": 8,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "13th on wood."},
            {"pop": 14, "F": 9,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "14th on food."},
            {"pop": 15, "F": 10, "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "15th on food. Build 2 Farms."},
            {"pop": 16, "F": 11, "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "16th on food."},
            {"pop": 17, "F": 12, "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "17th on food. Very food-heavy!"},
            {"pop": 18, "F": 12, "W": 6, "G": 0, "S": 0, "age": "Dark",   "note": "18th on wood. Build House."},
            {"pop": 19, "F": 13, "W": 6, "G": 0, "S": 0, "age": "Dark",   "note": "19th on food."},
            {"pop": 20, "F": 13, "W": 7, "G": 0, "S": 0, "age": "Dark",   "note": "20th on wood."},
            {"pop": 21, "F": 14, "W": 7, "G": 0, "S": 0, "age": "Dark",   "note": "21st on food. ➜ CLICK FEUDAL AGE!"},
            {"pop": 21, "F": 14, "W": 7, "G": 0, "S": 0, "age": "Feudal", "note": "2 vills build Stable + Barracks. Produce Scouts!"},
            {"pop": 23, "F": 14, "W": 7, "G": 2, "S": 0, "age": "Feudal", "note": "2 new vills to gold. Raid enemy vills!"},
        ],
    },
    {
        "name": "Archer Rush",
        "tags": "Aggressive · Feudal Push",
        "steps": [
            {"pop": 3,  "F": 3,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep."},
            {"pop": 4,  "F": 4,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build House."},
            {"pop": 5,  "F": 4,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "5th on wood."},
            {"pop": 6,  "F": 5,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "6th on sheep."},
            {"pop": 7,  "F": 5,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "7th on wood. Build House."},
            {"pop": 8,  "F": 6,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "8th on food. Lure Boar 1."},
            {"pop": 9,  "F": 6,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "9th on wood."},
            {"pop": 10, "F": 7,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "10th on berries. Build Mill."},
            {"pop": 11, "F": 7,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "11th on wood. (Need wood for Ranges)"},
            {"pop": 12, "F": 8,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "12th on food. Lure Boar 2. Build House."},
            {"pop": 13, "F": 8,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "13th on wood."},
            {"pop": 14, "F": 9,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "14th on food."},
            {"pop": 15, "F": 9,  "W": 5, "G": 1, "S": 0, "age": "Dark",   "note": "15th on gold. Build Mining Camp."},
            {"pop": 16, "F": 10, "W": 5, "G": 1, "S": 0, "age": "Dark",   "note": "16th on food. Build Farms. Build House."},
            {"pop": 17, "F": 10, "W": 5, "G": 2, "S": 0, "age": "Dark",   "note": "17th on gold."},
            {"pop": 18, "F": 10, "W": 6, "G": 2, "S": 0, "age": "Dark",   "note": "18th on wood."},
            {"pop": 19, "F": 11, "W": 6, "G": 2, "S": 0, "age": "Dark",   "note": "19th on food."},
            {"pop": 20, "F": 11, "W": 6, "G": 3, "S": 0, "age": "Dark",   "note": "20th on gold."},
            {"pop": 21, "F": 11, "W": 6, "G": 4, "S": 0, "age": "Dark",   "note": "21st on wood. ➜ CLICK FEUDAL AGE!"},
            {"pop": 21, "F": 11, "W": 6, "G": 4, "S": 0, "age": "Feudal", "note": "2 vills build 2x Archery Range + Barracks. Research Fletching!"},
            {"pop": 23, "F": 11, "W": 6, "G": 6, "S": 0, "age": "Feudal", "note": "2 new vills to gold. Produce Archers constantly!"},
            {"pop": 25, "F": 11, "W": 6, "G": 8, "S": 0, "age": "Feudal", "note": "Add 3rd Range. Raid enemy villagers!"},
        ],
    },
    {
        "name": "MAA + Archers",
        "tags": "Flush · Versatile",
        "steps": [
            {"pop": 3,  "F": 3,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep."},
            {"pop": 4,  "F": 4,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build House."},
            {"pop": 5,  "F": 4,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "5th on wood."},
            {"pop": 6,  "F": 5,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "6th on sheep."},
            {"pop": 7,  "F": 5,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "7th on wood. Build House."},
            {"pop": 8,  "F": 6,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "8th on food. Lure Boar 1."},
            {"pop": 9,  "F": 6,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "9th on wood."},
            {"pop": 10, "F": 7,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "10th on berries. Build Mill."},
            {"pop": 11, "F": 8,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "11th on food."},
            {"pop": 12, "F": 8,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "12th on wood. Build Barracks! Build House."},
            {"pop": 13, "F": 9,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "13th on food. Lure Boar 2."},
            {"pop": 14, "F": 9,  "W": 4, "G": 1, "S": 0, "age": "Dark",   "note": "14th on gold. Build Mining Camp."},
            {"pop": 15, "F": 9,  "W": 4, "G": 2, "S": 0, "age": "Dark",   "note": "15th on gold."},
            {"pop": 16, "F": 10, "W": 5, "G": 2, "S": 0, "age": "Dark",   "note": "16th on wood. Build Farms. Build House."},
            {"pop": 17, "F": 11, "W": 5, "G": 2, "S": 0, "age": "Dark",   "note": "17th on food."},
            {"pop": 18, "F": 11, "W": 5, "G": 3, "S": 0, "age": "Dark",   "note": "18th on gold."},
            {"pop": 19, "F": 11, "W": 6, "G": 3, "S": 0, "age": "Dark",   "note": "19th on wood."},
            {"pop": 20, "F": 12, "W": 6, "G": 3, "S": 0, "age": "Dark",   "note": "20th on food."},
            {"pop": 21, "F": 12, "W": 6, "G": 3, "S": 0, "age": "Dark",   "note": "21st → build Archery Range. ➜ CLICK FEUDAL!"},
            {"pop": 21, "F": 12, "W": 6, "G": 3, "S": 0, "age": "Feudal", "note": "Research Man-at-Arms upgrade. Produce MAA + Archers!"},
            {"pop": 23, "F": 12, "W": 6, "G": 5, "S": 0, "age": "Feudal", "note": "2 new vills to gold. MAA in front, Archers behind!"},
        ],
    },
    {
        "name": "FC Boom",
        "tags": "Economic · Late Game",
        "steps": [
            {"pop": 3,  "F": 3,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "3 vills on sheep."},
            {"pop": 4,  "F": 4,  "W": 0, "G": 0, "S": 0, "age": "Dark",   "note": "4th on sheep. Build House."},
            {"pop": 5,  "F": 4,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "5th on wood."},
            {"pop": 6,  "F": 5,  "W": 1, "G": 0, "S": 0, "age": "Dark",   "note": "6th on sheep."},
            {"pop": 7,  "F": 5,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "7th on wood. Build House."},
            {"pop": 8,  "F": 6,  "W": 2, "G": 0, "S": 0, "age": "Dark",   "note": "8th on food. Lure Boar 1."},
            {"pop": 9,  "F": 6,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "9th on wood."},
            {"pop": 10, "F": 7,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "10th on berries. Build Mill."},
            {"pop": 11, "F": 8,  "W": 3, "G": 0, "S": 0, "age": "Dark",   "note": "11th on berries."},
            {"pop": 12, "F": 8,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "12th on wood. Build House."},
            {"pop": 13, "F": 9,  "W": 4, "G": 0, "S": 0, "age": "Dark",   "note": "13th on food. Lure Boar 2."},
            {"pop": 14, "F": 9,  "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "14th on wood."},
            {"pop": 15, "F": 10, "W": 5, "G": 0, "S": 0, "age": "Dark",   "note": "15th on food. Build 2 Farms."},
            {"pop": 16, "F": 10, "W": 5, "G": 1, "S": 0, "age": "Dark",   "note": "16th on gold. Mining Camp."},
            {"pop": 17, "F": 10, "W": 5, "G": 2, "S": 0, "age": "Dark",   "note": "17th on gold."},
            {"pop": 18, "F": 10, "W": 5, "G": 3, "S": 0, "age": "Dark",   "note": "18th on gold."},
            {"pop": 19, "F": 11, "W": 5, "G": 3, "S": 0, "age": "Dark",   "note": "19th on food (farms)."},
            {"pop": 20, "F": 11, "W": 5, "G": 4, "S": 0, "age": "Dark",   "note": "20th on gold."},
            {"pop": 21, "F": 11, "W": 5, "G": 4, "S": 0, "age": "Dark",   "note": "➜ CLICK FEUDAL AGE!"},
            {"pop": 21, "F": 11, "W": 5, "G": 4, "S": 0, "age": "Feudal", "note": "2 vills build Blacksmith + Market. No military — pure boom!"},
            {"pop": 24, "F": 12, "W": 5, "G": 6, "S": 1, "age": "Feudal", "note": "New vills: 2 gold, 1 stone. Queue stone for TCs."},
            {"pop": 24, "F": 12, "W": 5, "G": 6, "S": 1, "age": "Castle", "note": "800F + 200G ➜ CASTLE AGE! Build 2-3 TCs. Research Wheelbarrow!"},
        ],
    },
]

# ─────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────
COLORS = {
    "bg":         "#141008",
    "bg2":        "#1c1810",
    "border":     "#3a3020",
    "gold":       "#c8a020",
    "gold_dim":   "#6a5010",
    "text":       "#ddd0a8",
    "text_dim":   "#706050",
    "food":       "#d85030",
    "wood":       "#50a030",
    "gold_res":   "#e8b830",
    "stone":      "#909090",
    "dark_age":   "#2a1008",
    "feudal_age": "#201808",
    "castle_age": "#081828",
    "imp_age":    "#180820",
    "btn_bg":     "#201c14",
    "btn_hover":  "#302820",
    "white":      "#f0e8d0",
    "advance":    "#c85020",
}

AGE_COLORS = {
    "Dark":     ("#2a1008", "#c06040", "🏚 Dark Age"),
    "Feudal":   ("#201808", "#c09030", "⚔  Feudal Age"),
    "Castle":   ("#081828", "#3090c0", "🏰 Castle Age"),
    "Imperial": ("#180820", "#a040c0", "👑 Imperial Age"),
}

RES_CFG = [
    ("F", "🌾", COLORS["food"],     "Food"),
    ("W", "🪵", COLORS["wood"],     "Wood"),
    ("G", "💰", COLORS["gold_res"], "Gold"),
    ("S", "⛏", COLORS["stone"],    "Stone"),
]


class AoE2Overlay:
    def __init__(self, root):
        self.root = root
        self.bo_idx = 0
        self.step_idx = 0
        self._drag_x = 0
        self._drag_y = 0

        self._setup_window()
        self._build_ui()
        self._render()
        # Position after UI is built so tkinter knows the true height
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"300x{self.root.winfo_reqheight()}+{sw - 320}+40")

    # ── Window Setup ───────────────────────────
    def _setup_window(self):
        r = self.root
        r.title("AoE2 Overlay")
        r.configure(bg=COLORS["bg"])
        r.overrideredirect(True)          # no title bar
        r.attributes("-topmost", True)    # always on top
        r.attributes("-alpha", 0.92)      # slight transparency

        r.resizable(False, False)

        # Drag support
        r.bind("<ButtonPress-1>",   self._drag_start)
        r.bind("<B1-Motion>",       self._drag_move)
        # Right-click to close
        r.bind("<Button-3>", lambda e: r.destroy())
        # Arrow keys
        r.bind("<Left>",  lambda e: self._step(-1))
        r.bind("<Right>", lambda e: self._step(1))
        r.bind("<Up>",    lambda e: self._change_bo(-1))
        r.bind("<Down>",  lambda e: self._change_bo(1))

    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        x = e.x_root - self._drag_x
        y = e.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    # ── UI Build ───────────────────────────────
    def _build_ui(self):
        PAD = 6
        r = self.root

        # ── Title bar (drag handle + close) ──
        title_bar = tk.Frame(r, bg=COLORS["bg2"], height=22)
        title_bar.pack(fill="x")
        title_bar.bind("<ButtonPress-1>",   self._drag_start)
        title_bar.bind("<B1-Motion>",       self._drag_move)

        tk.Label(title_bar, text="⚔ AoE2 Build Order", bg=COLORS["bg2"],
                 fg=COLORS["gold"], font=("Helvetica", 9, "bold")).pack(side="left", padx=6, pady=2)
        tk.Label(title_bar, text="✕ right-click", bg=COLORS["bg2"],
                 fg=COLORS["text_dim"], font=("Helvetica", 7)).pack(side="right", padx=6)

        # ── Build order selector buttons ──
        BO_SHORT = ["FC", "Scouts", "Archers", "MAA", "Boom"]
        bo_frame = tk.Frame(r, bg=COLORS["bg"], pady=2)
        bo_frame.pack(fill="x", padx=PAD)
        self.bo_btns = []
        for i, bo in enumerate(BUILD_ORDERS):
            label = BO_SHORT[i] if i < len(BO_SHORT) else bo["name"]
            btn = tk.Label(bo_frame, text=label, bg=COLORS["bg2"],
                           fg=COLORS["text_dim"], font=("Helvetica", 7),
                           padx=4, pady=2, cursor="hand2", relief="flat")
            btn.pack(side="left", padx=1)
            btn.bind("<Button-1>", lambda e, idx=i: self._select_bo(idx))
            self.bo_btns.append(btn)

        # ── Age banner ──
        self.age_lbl = tk.Label(r, text="", font=("Helvetica", 9, "bold"),
                                pady=3, padx=6)
        self.age_lbl.pack(fill="x", padx=PAD, pady=(2, 0))

        # ── Pop + step info ──
        info_row = tk.Frame(r, bg=COLORS["bg"])
        info_row.pack(fill="x", padx=PAD, pady=2)

        self.pop_lbl = tk.Label(info_row, text="Pop: 0", bg=COLORS["bg"],
                                fg=COLORS["text_dim"], font=("Helvetica", 8))
        self.pop_lbl.pack(side="left")

        self.step_lbl = tk.Label(info_row, text="1/1", bg=COLORS["bg"],
                                 fg=COLORS["text_dim"], font=("Helvetica", 8))
        self.step_lbl.pack(side="right")

        # ── Note ──
        note_frame = tk.Frame(r, bg=COLORS["bg2"], padx=8, pady=6)
        note_frame.pack(fill="x", padx=PAD, pady=2)
        self.note_lbl = tk.Label(note_frame, text="", bg=COLORS["bg2"],
                                 fg=COLORS["white"], font=("Helvetica", 9),
                                 wraplength=268, justify="left", anchor="w")
        self.note_lbl.pack(fill="x")

        # ── Resources ──
        res_frame = tk.Frame(r, bg=COLORS["bg"])
        res_frame.pack(fill="x", padx=PAD, pady=2)
        self.res_labels = {}
        for i, (key, icon, color, label) in enumerate(RES_CFG):
            col_f = tk.Frame(res_frame, bg=COLORS["bg2"], padx=6, pady=4)
            col_f.grid(row=0, column=i, padx=2, sticky="ew")
            res_frame.columnconfigure(i, weight=1)

            tk.Label(col_f, text=icon, bg=COLORS["bg2"],
                     font=("Helvetica", 11)).pack()
            tk.Label(col_f, text=label, bg=COLORS["bg2"],
                     fg=COLORS["text_dim"], font=("Helvetica", 6)).pack()
            val_lbl = tk.Label(col_f, text="0", bg=COLORS["bg2"],
                               fg=color, font=("Helvetica", 11, "bold"))
            val_lbl.pack()
            self.res_labels[key] = val_lbl

        # ── Progress dots ──
        self.dots_frame = tk.Frame(r, bg=COLORS["bg"])
        self.dots_frame.pack(fill="x", padx=PAD, pady=(4, 2))

        # ── Nav buttons ──
        nav_frame = tk.Frame(r, bg=COLORS["bg"])
        nav_frame.pack(fill="x", padx=PAD, pady=(2, 2))

        self.prev_btn = tk.Button(nav_frame, text="◀ Prev", command=lambda: self._step(-1),
                                  bg=COLORS["btn_bg"], fg=COLORS["text"],
                                  font=("Helvetica", 8), relief="flat",
                                  activebackground=COLORS["btn_hover"],
                                  activeforeground=COLORS["gold"],
                                  padx=10, pady=4, cursor="hand2", bd=0)
        self.prev_btn.pack(side="left", expand=True, fill="x", padx=(0,2))

        self.next_btn = tk.Button(nav_frame, text="Next ▶", command=lambda: self._step(1),
                                  bg=COLORS["btn_bg"], fg=COLORS["text"],
                                  font=("Helvetica", 8), relief="flat",
                                  activebackground=COLORS["btn_hover"],
                                  activeforeground=COLORS["gold"],
                                  padx=10, pady=4, cursor="hand2", bd=0)
        self.next_btn.pack(side="left", expand=True, fill="x", padx=(2,0))

        # ── Keyboard hint ──
        tk.Label(r, text="PgDn/PgUp: next/prev step  ↑↓: build order  right-click: close",
                 bg=COLORS["bg"], fg=COLORS["text_dim"], font=("Helvetica", 6)).pack(pady=(0,2))

    # ── Rendering ──────────────────────────────
    def _render(self):
        bo = BUILD_ORDERS[self.bo_idx]
        step = bo["steps"][self.step_idx]
        total = len(bo["steps"])

        # BO buttons highlight
        for i, btn in enumerate(self.bo_btns):
            if i == self.bo_idx:
                btn.config(bg=COLORS["gold_dim"], fg=COLORS["gold"])
            else:
                btn.config(bg=COLORS["bg2"], fg=COLORS["text_dim"])

        # Age banner
        age = step["age"]
        age_bg, age_fg, age_txt = AGE_COLORS.get(age, AGE_COLORS["Dark"])
        self.age_lbl.config(bg=age_bg, fg=age_fg, text=age_txt)

        # Pop & step
        self.pop_lbl.config(text=f"Pop: {step['pop']}")
        self.step_lbl.config(text=f"Step {self.step_idx+1}/{total}")

        # Note — highlight advance steps
        note = step["note"]
        is_advance = "CLICK" in note or "➜" in note
        self.note_lbl.config(
            text=note,
            fg=COLORS["advance"] if is_advance else COLORS["white"]
        )

        # Resources
        for key, icon, color, label in RES_CFG:
            val = step[key]
            self.res_labels[key].config(
                text=str(val),
                fg=color if val > 0 else COLORS["text_dim"]
            )

        # Dots
        for w in self.dots_frame.winfo_children():
            w.destroy()
        max_dots = 22
        step_range = list(range(total))
        if total > max_dots:
            half = max_dots // 2
            start_range = step_range[:half]
            end_range = step_range[total - half:]
            display_steps = start_range + [-1] + end_range  # -1 = ellipsis
        else:
            display_steps = step_range

        for d in display_steps:
            if d == -1:
                tk.Label(self.dots_frame, text="…", bg=COLORS["bg"],
                         fg=COLORS["text_dim"], font=("Helvetica", 7)).pack(side="left")
                continue
            if d == self.step_idx:
                color = COLORS["gold"]
                size = 8
            elif d < self.step_idx:
                color = COLORS["gold_dim"]
                size = 6
            else:
                color = COLORS["border"]
                size = 6
            dot = tk.Canvas(self.dots_frame, width=size+2, height=size+2,
                            bg=COLORS["bg"], highlightthickness=0, cursor="hand2")
            dot.create_oval(1, 1, size+1, size+1, fill=color, outline="")
            dot.pack(side="left", padx=1, pady=3)
            dot.bind("<Button-1>", lambda e, idx=d: self._goto(idx))

        # Buttons state
        self.prev_btn.config(state="normal" if self.step_idx > 0 else "disabled")
        self.next_btn.config(state="normal" if self.step_idx < total - 1 else "disabled")

    # ── Controls ───────────────────────────────
    def _step(self, d):
        bo = BUILD_ORDERS[self.bo_idx]
        self.step_idx = max(0, min(len(bo["steps"]) - 1, self.step_idx + d))
        self._render()

    def _goto(self, idx):
        self.step_idx = idx
        self._render()

    def _select_bo(self, idx):
        self.bo_idx = idx
        self.step_idx = 0
        self._render()

    def _change_bo(self, d):
        self.bo_idx = (self.bo_idx + d) % len(BUILD_ORDERS)
        self.step_idx = 0
        self._render()


# ─────────────────────────────────────────────
# GLOBAL HOTKEY LISTENER
# Runs in a daemon thread so it works even when
# the game window has focus.
# ─────────────────────────────────────────────
def start_hotkey_listener(app):
    def on_press(key):
        if key == HOTKEY_NEXT:
            app.root.after(0, lambda: app._step(1))
        elif key == HOTKEY_PREV:
            app.root.after(0, lambda: app._step(-1))

    listener = pynput_kb.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AoE2Overlay(root)
    start_hotkey_listener(app)
    root.mainloop()
