import tkinter as tk
from tkinter import messagebox
from pet import Pet, petStats
from economy import Economy

BACKGROUND = "#0f172a"
CARD_BG = "#111827"
INPUT_BG = "#0b1220"
BORDER = "#1f2937"
TEXT_PRIMARY = "#e5e7eb"
TEXT_SECONDARY = "#9ca3af"
ACCENT = "#22c55e"
ACCENT_DARK = "#16a34a"
BUTTON_BG = "#2563eb"
BUTTON_BG_ACTIVE = "#1d4ed8"

# =========================
# ASCII PET SKINS
# =========================

PET_SKINS = {
    "dog": {
        "happy": r"""
+--------------+
| / \__        |
|(    @\___    |
|/         O   |
+--------------+
""",
        "neutral": r"""
+--------------+
| / \__        |
|(    @\___    |
|/         o   |
+--------------+
""",
        "hungry": r"""
+--------------+
| / \__        |
|(    @\___    |
|/       ( )~  |
+--------------+
""",
        "tired": r"""
+--------------+
| / \__        |
|(   -@\___    |
|/         z   |
+--------------+
""",
        "dirty": r"""
+--------------+
| / \__   . .  |
|(  x @\___    |
|/    ~    o   |
+--------------+
""",
        "sick": r"""
+--------------+
| / \__  *     |
|(  u @\___    |
|/     _   o   |
+--------------+
""",
        "sad": r"""
+--------------+
| / \__        |
|(  T @\___    |
|/        _    |
+--------------+
"""
    },

    "cat": {
        "happy": r"""
+--------------+
| /\_/\  /\    |
|( =^.^= ) )   |
| >  w  <(/    |
+--------------+
""",
        "neutral": r"""
+--------------+
| /\_/\  /\    |
|( =o.o= ) )   |
| >  -  <(/    |
+--------------+
""",
        "hungry": r"""
+--------------+
| /\_/\  /\    |
|( =o.o= ) )   |
| >  ~  <(/    |
+--------------+
""",
        "tired": r"""
+--------------+
| /\_/\  /\    |
|( =-.-= ) )   |
| >  -  <(/    |
+--------------+
""",
        "dirty": r"""
+--------------+
| /\_/\  /\ .  |
|( =x.x= ) )   |
| >  ~  <(/    |
+--------------+
""",
        "sick": r"""
+--------------+
| /\_/\  /\    |
|( =u.u= ) )   |
| >  _  <(/    |
+--------------+
""",
        "sad": r"""
+--------------+
| /\_/\  /\    |
|( =T.T= ) )   |
| >  _  <(/    |
+--------------+
"""
    },

    "guinea pig": {
        "happy": r"""
+--------------+
| (\__//)      |
|( 'u'  )  o ) |
| \____/  (_/  |
+--------------+
""",
        "neutral": r"""
+--------------+
| (\__//)      |
|( 'o'  )  o ) |
| \____/  (_/  |
+--------------+
""",
        "hungry": r"""
+--------------+
| (\__//)      |
|( 'o'  )  o ) |
| \_~~_/  (_/  |
+--------------+
""",
        "tired": r"""
+--------------+
| (\__//)      |
|( -.-  )  o ) |
| \____/  (_/  |
+--------------+
""",
        "dirty": r"""
+--------------+
| (\__//)  .   |
|( 'x'  )  o ) |
| \_~~_/  (_/  |
+--------------+
""",
        "sick": r"""
+--------------+
| (\__//)      |
|( 'u'  )  o ) |
| \_--_/  (_/  |
+--------------+
""",
        "sad": r"""
+--------------+
| (\__//)      |
|( 'T'  )  o ) |
| \____/  (_/  |
+--------------+
"""
    }
}

GUI_PET_PROFILES = {
    "dog": petStats("dog", 40, 80, 70, 90),
    "cat": petStats("cat", 80, 70, 60, 80),
    # No preset existed in main.py for guinea pig; provide a balanced profile here
    "guinea pig": petStats("guinea pig", 60, 75, 65, 70, 90),
}

def format_bar(label: str, value: int, max_value: int, width: int = 18) -> str:
    max_value = max_value or 1
    value = max(0, min(value, max_value))
    filled = int((value / max_value) * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"{label:<12} [{bar}] {value:>3}/{max_value}"


class VirtualPetGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("1280x720")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(True, True)

        self.pet = None
        self.economy = None

        self.create_start_screen()
        self.root.mainloop()

    def create_start_screen(self):
        self.clear()

        header = tk.Frame(self.root, bg=BACKGROUND, pady=10)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Virtual Pet Studio",
            font=("Consolas", 22, "bold"),
            fg=TEXT_PRIMARY,
            bg=BACKGROUND
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Name your companion and pick their species to begin.",
            font=("Consolas", 11),
            fg=TEXT_SECONDARY,
            bg=BACKGROUND
        )
        subtitle.pack()

        form = tk.Frame(self.root, bg=CARD_BG, padx=20, pady=20, highlightbackground=BORDER, highlightthickness=1)
        form.pack(pady=20, fill="x", padx=20)

        tk.Label(form, text="Pet Name", fg=TEXT_PRIMARY, bg=CARD_BG, font=("Consolas", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form, font=("Consolas", 12), bg=INPUT_BG, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=(4, 10))

        tk.Label(form, text="Pet Type", fg=TEXT_PRIMARY, bg=CARD_BG, font=("Consolas", 12, "bold")).grid(row=2, column=0, sticky="w")
        self.pet_type = tk.StringVar(value="dog")
        pet_selector = tk.OptionMenu(form, self.pet_type, *GUI_PET_PROFILES.keys())
        pet_selector.config(bg=INPUT_BG, fg=TEXT_PRIMARY, activebackground=BORDER, activeforeground=TEXT_PRIMARY, relief="flat", highlightthickness=0, font=("Consolas", 11))
        pet_selector["menu"].config(bg=INPUT_BG, fg=TEXT_PRIMARY, activebackground=BORDER, activeforeground=TEXT_PRIMARY, font=("Consolas", 11))
        pet_selector.grid(row=3, column=0, sticky="ew", pady=(4, 12))

        start_btn = tk.Button(
            form,
            text="Start Game",
            command=self.start_game,
            bg=ACCENT,
            fg=BACKGROUND,
            activebackground=ACCENT_DARK,
            activeforeground=BACKGROUND,
            font=("Consolas", 12, "bold"),
            relief="flat",
            padx=10,
            pady=6
        )
        start_btn.grid(row=4, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

    def start_game(self):
        name = self.name_entry.get().strip()
        ptype = self.pet_type.get()

        if not name:
            messagebox.showerror("Error", "Please give your pet a name.")
            return

        profile = GUI_PET_PROFILES.get(ptype.lower(), petStats(ptype.lower()))
        self.pet = Pet(name, profile, use_terminal_ui=False)
        self.economy = Economy()

        self.create_game_screen()

    def create_game_screen(self):
        self.clear()

        container = tk.Frame(self.root, bg=BACKGROUND, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        header = tk.Label(
            container,
            text="Care Dashboard",
            font=("Consolas", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=BACKGROUND
        )
        header.pack(anchor="w", pady=(0, 8))

        display_frame = tk.Frame(container, bg=CARD_BG, padx=14, pady=14, highlightbackground=BORDER, highlightthickness=1)
        display_frame.pack(fill="both", expand=True)

        self.pet_display = tk.Label(
            display_frame,
            font=("Consolas", 14),
            fg=TEXT_PRIMARY,
            bg=INPUT_BG,
            justify="center",
            relief="ridge",
            bd=1,
            padx=10,
            pady=10
        )
        self.pet_display.pack(fill="both", expand=True)

        self.stats_label = tk.Label(
            display_frame,
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            justify="left",
            anchor="w",
            pady=8
        )
        self.stats_label.pack(fill="x", pady=(8, 0))

        btn_frame = tk.Frame(container, bg=BACKGROUND)
        btn_frame.pack(pady=12)

        btn_style = {
            "bg": BUTTON_BG,
            "fg": TEXT_PRIMARY,
            "activebackground": BUTTON_BG_ACTIVE,
            "activeforeground": TEXT_PRIMARY,
            "font": ("Consolas", 11, "bold"),
            "relief": "flat",
            "padx": 12,
            "pady": 6,
            "bd": 0
        }

        tk.Button(btn_frame, text="Feed", command=self.feed, **btn_style).grid(row=0, column=0, padx=6, pady=6)
        tk.Button(btn_frame, text="Play", command=self.play, **btn_style).grid(row=0, column=1, padx=6, pady=6)
        tk.Button(btn_frame, text="Sleep", command=self.sleep, **btn_style).grid(row=0, column=2, padx=6, pady=6)
        tk.Button(btn_frame, text="Advance Day", command=self.advance, **btn_style).grid(row=0, column=3, padx=6, pady=6)
        tk.Button(btn_frame, text="Bathe/Shower", command=self.shower, **btn_style).grid(row=0, column=4, padx=6, pady=6)

        self.update_ui()

    def update_ui(self):
        state = self.pet.get_emotional_state()
        species = getattr(self.pet, "species", getattr(self.pet.pet_type, "type", "dog")).lower()
        skins = PET_SKINS.get(species, PET_SKINS["dog"])
        skin = skins.get(state) or skins.get("neutral", "")

        self.pet_display.config(text=skin)

        stats = self.pet.pet_type
        self.stats_label.config(
            text=(
                f"{self.pet.name} - {species.title()}\n"
                f"{format_bar('Hunger', self.pet.hunger, stats.hunger)}\n"
                f"{format_bar('Happiness', self.pet.happiness, stats.happiness)}\n"
                f"{format_bar('Health', self.pet.health, stats.health)}\n"
                f"{format_bar('Energy', self.pet.energy, stats.energy)}\n"
                f"{format_bar('Cleanliness', self.pet.cleanliness, stats.cleanliness)}\n"
                f"Balance:      ${self.economy.balance}"
            )
        )

    def feed(self):
        if self.economy.spend("food", 10):
            self.pet.feed(20)
        self.update_ui()
        self.check_game_over()

    def play(self):
        if self.economy.spend("toys", 5):
            self.pet.play(10)
        self.update_ui()
        self.check_game_over()

    def sleep(self):
        self.pet.sleep(5)
        self.update_ui()
        self.check_game_over()

    def advance(self):
        self.pet.pass_time(1)
        self.update_ui()
        self.check_game_over()

    def shower(self):
        if self.economy.spend("grooming", 8):
            self.pet.shower(5)
        self.update_ui()
        self.check_game_over()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_game_over(self):
        if not self.pet.detectLoss():
            return False
        reason = getattr(self.pet, "last_death_reason", "") or "Your pet's wellbeing dropped too low."
        messagebox.showinfo("Game Over", f"{self.pet.name} couldn't continue.\n{reason}")
        self.root.destroy()
        return True


if __name__ == "__main__":
    VirtualPetGUI()
