import tkinter as tk
from tkinter import messagebox, ttk
from pet import Pet, petStats
from economy import Economy
from stock_market import StockMarket

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
STOCK_COLORS = {
    "PAW": "#60a5fa",
    "MEOW": "#f472b6",
    "BONE": "#a78bfa",
    "NUT": "#fbbf24",
}
PRED_COLOR = "#f97316"
MA_COLOR = "#10b981"

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
        self.stock_market = StockMarket(self.economy)

        self.create_game_screen()

    def create_game_screen(self):
        self.clear()

        self.notebook = ttk.Notebook(self.root)
        self.care_tab = tk.Frame(self.notebook, bg=BACKGROUND)
        self.economy_tab = tk.Frame(self.notebook, bg=BACKGROUND)
        self.chart_tab = tk.Frame(self.notebook, bg=BACKGROUND)
        self.notebook.add(self.care_tab, text="Care")
        self.notebook.add(self.economy_tab, text="Economy")
        self.notebook.add(self.chart_tab, text="Charts")
        self.notebook.pack(fill="both", expand=True)

        self.build_care_tab()
        self.build_economy_tab()
        self.build_chart_tab()

        self.update_ui()
        self.update_economy_ui()

    def build_care_tab(self):
        container = tk.Frame(self.care_tab, bg=BACKGROUND, padx=10, pady=10)
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

    def build_economy_tab(self):
        container = tk.Frame(self.economy_tab, bg=BACKGROUND, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        header = tk.Label(
            container,
            text="Economy & Investments",
            font=("Consolas", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=BACKGROUND
        )
        header.pack(anchor="w", pady=(0, 8))

        top_row = tk.Frame(container, bg=BACKGROUND)
        top_row.pack(fill="x", pady=(0, 10))

        self.balance_label = tk.Label(top_row, text="", font=("Consolas", 12, "bold"), fg=TEXT_PRIMARY, bg=BACKGROUND)
        self.balance_label.pack(side="left")

        self.portfolio_label = tk.Label(top_row, text="", font=("Consolas", 12), fg=TEXT_SECONDARY, bg=BACKGROUND)
        self.portfolio_label.pack(side="right")

        self.profit_label = tk.Label(container, text="", font=("Consolas", 12, "bold"), fg=TEXT_PRIMARY, bg=BACKGROUND)
        self.profit_label.pack(anchor="w", pady=(0, 6))

        market_card = tk.Frame(container, bg=CARD_BG, padx=14, pady=14, highlightbackground=BORDER, highlightthickness=1)
        market_card.pack(fill="both", expand=True)

        self.market_prices_label = tk.Label(market_card, text="", font=("Consolas", 11), fg=TEXT_PRIMARY, bg=CARD_BG, justify="left", anchor="nw")
        self.market_prices_label.pack(fill="x")

        control_row = tk.Frame(market_card, bg=CARD_BG, pady=10)
        control_row.pack(fill="x")

        tk.Label(control_row, text="Symbol", font=("Consolas", 11, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG).grid(row=0, column=0, sticky="w")
        tk.Label(control_row, text="Shares", font=("Consolas", 11, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG).grid(row=0, column=1, sticky="w")

        self.market_symbol = tk.StringVar(value="PAW")
        symbols = list(self.stock_market.prices.keys())
        symbol_menu = tk.OptionMenu(control_row, self.market_symbol, *symbols)
        symbol_menu.config(bg=INPUT_BG, fg=TEXT_PRIMARY, activebackground=BORDER, activeforeground=TEXT_PRIMARY, relief="flat", highlightthickness=0, font=("Consolas", 11))
        symbol_menu["menu"].config(bg=INPUT_BG, fg=TEXT_PRIMARY, activebackground=BORDER, activeforeground=TEXT_PRIMARY, font=("Consolas", 11))
        symbol_menu.grid(row=1, column=0, padx=(0, 8), pady=(4, 0), sticky="ew")

        self.shares_entry = tk.Entry(control_row, font=("Consolas", 11), bg=INPUT_BG, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.shares_entry.grid(row=1, column=1, padx=(0, 8), pady=(4, 0), sticky="ew")

        action_style = {
            "bg": BUTTON_BG,
            "fg": TEXT_PRIMARY,
            "activebackground": BUTTON_BG_ACTIVE,
            "activeforeground": TEXT_PRIMARY,
            "font": ("Consolas", 11, "bold"),
            "relief": "flat",
            "padx": 10,
            "pady": 6,
            "bd": 0
        }

        tk.Button(control_row, text="Buy", command=self.buy_stock, **action_style).grid(row=1, column=2, padx=4, sticky="ew")
        tk.Button(control_row, text="Sell", command=self.sell_stock, **action_style).grid(row=1, column=3, padx=4, sticky="ew")
        control_row.columnconfigure(0, weight=1)
        control_row.columnconfigure(1, weight=1)

        holdings_card = tk.Frame(market_card, bg=INPUT_BG, padx=12, pady=12, relief="ridge", bd=1)
        holdings_card.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(holdings_card, text="Holdings", font=("Consolas", 12, "bold"), fg=TEXT_PRIMARY, bg=INPUT_BG).pack(anchor="w")
        self.holdings_text = tk.Text(
            holdings_card,
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=INPUT_BG,
            relief="flat",
            height=8,
            wrap="none"
        )
        self.holdings_text.pack(fill="both", expand=True, pady=(6, 0))
        self.holdings_text.config(state="disabled")
        self.holdings_text.tag_configure("gain", foreground="#22c55e")
        self.holdings_text.tag_configure("loss", foreground="#f87171")
        self.holdings_text.tag_configure("neutral", foreground=TEXT_PRIMARY)

        self.market_message = tk.Label(market_card, text="", font=("Consolas", 10), fg=TEXT_SECONDARY, bg=CARD_BG, justify="left", anchor="w")
        self.market_message.pack(fill="x", pady=(8, 0))

    def build_chart_tab(self):
        container = tk.Frame(self.chart_tab, bg=BACKGROUND, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        header = tk.Label(
            container,
            text="Market Charts",
            font=("Consolas", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=BACKGROUND
        )
        header.pack(anchor="w", pady=(0, 8))

        self.chart_canvas = tk.Canvas(container, bg="#0b1220", highlightthickness=1, highlightbackground=BORDER)
        self.chart_canvas.pack(fill="both", expand=True)
        self.chart_canvas.bind("<Configure>", lambda e: self.draw_chart())

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
        self.update_economy_ui()

    def update_economy_ui(self):
        if not hasattr(self, "stock_market"):
            return
        balance = self.economy.balance
        portfolio = self.stock_market.portfolio_value()
        total_profit = self.stock_market.total_profit()
        self.balance_label.config(text=f"Balance: ${balance}")
        self.portfolio_label.config(text=f"Portfolio: ${portfolio:,.2f}")
        self.profit_label.config(text=f"Total P/L: ${total_profit:,.2f}", fg="#22c55e" if total_profit > 0 else ("#f87171" if total_profit < 0 else TEXT_PRIMARY))

        price_lines = [f"{sym:<4} ${price:>6.2f}" for sym, price in self.stock_market.prices.items()]
        self.market_prices_label.config(text="\n".join(price_lines))

        holding_lines = self.stock_market.holdings_lines()
        self.holdings_text.config(state="normal")
        self.holdings_text.delete("1.0", "end")
        for line, pl in holding_lines:
            tag = "neutral"
            if pl > 0:
                tag = "gain"
            elif pl < 0:
                tag = "loss"
            self.holdings_text.insert("end", line + "\n", tag)
        self.holdings_text.config(state="disabled")
        self.draw_chart()

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
        # Market advances with time to prevent spamming ticks
        self.stock_market.tick()
        self.market_message.config(text="Day advanced. Market moved.", fg=TEXT_SECONDARY)
        self.pet.pass_time(1)
        self.update_ui()
        self.check_game_over()

    def shower(self):
        if self.economy.spend("grooming", 8):
            self.pet.shower(5)
        self.update_ui()
        self.check_game_over()

    def buy_stock(self):
        try:
            shares = int(self.shares_entry.get() or "0")
        except ValueError:
            self.market_message.config(text="Enter a whole number of shares.", fg="#fca5a5")
            return

        success, msg = self.stock_market.buy(self.market_symbol.get(), shares)
        self.market_message.config(text=msg, fg="#22c55e" if success else "#fca5a5")
        self.update_economy_ui()
        self.update_ui()

    def sell_stock(self):
        try:
            shares = int(self.shares_entry.get() or "0")
        except ValueError:
            self.market_message.config(text="Enter a whole number of shares.", fg="#fca5a5")
            return

        success, msg = self.stock_market.sell(self.market_symbol.get(), shares)
        self.market_message.config(text=msg, fg="#22c55e" if success else "#fca5a5")
        self.update_economy_ui()
        self.update_ui()

    def tick_market(self):
        # Manual ticks are disabled; market moves with Advance Day
        self.market_message.config(text="Advance the day to move the market.", fg=TEXT_SECONDARY)

    def draw_chart(self):
        if not hasattr(self, "chart_canvas") or not hasattr(self, "stock_market"):
            return
        canvas = self.chart_canvas
        canvas.delete("all")

        history = self.stock_market.price_history()
        if not history:
            return

        # Determine bounds
        projections = {sym: self.stock_market.predict(sym) for sym in history}
        all_points = [(day, price) for points in history.values() for day, price in points]
        all_proj_points = [(day, price) for points in projections.values() for day, price in points]
        if not all_points:
            return
        min_day = min(d for d, _ in all_points)
        max_day = max(d for d, _ in all_points + all_proj_points) if all_proj_points else max(d for d, _ in all_points)
        min_price = min(p for _, p in all_points + all_proj_points) if all_proj_points else min(p for _, p in all_points)
        max_price = max(p for _, p in all_points + all_proj_points) if all_proj_points else max(p for _, p in all_points)

        width = canvas.winfo_width() or 800
        height = canvas.winfo_height() or 400
        pad = 40

        def x_scale(day):
            if max_day == min_day:
                return pad
            return pad + (day - min_day) / (max_day - min_day) * (width - 2 * pad)

        def y_scale(price):
            if max_price == min_price:
                return height - pad
            return height - pad - (price - min_price) / (max_price - min_price) * (height - 2 * pad)

        # Axes
        canvas.create_line(pad, height - pad, width - pad, height - pad, fill=TEXT_SECONDARY)
        canvas.create_line(pad, pad, pad, height - pad, fill=TEXT_SECONDARY)

        # Labels
        canvas.create_text(pad, pad - 10, text=f"Max ${max_price:.2f}", fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 10))
        canvas.create_text(pad, height - pad + 10, text=f"Min ${min_price:.2f}", fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 10))
        canvas.create_text(width - pad, height - pad + 10, text=f"Day {max_day}", fill=TEXT_PRIMARY, anchor="e", font=("Consolas", 10))

        # Plot lines
        symbols_order = list(history.keys())
        for idx, symbol in enumerate(symbols_order):
            points = history.get(symbol, [])
            if len(points) >= 2:
                color = STOCK_COLORS.get(symbol, TEXT_PRIMARY)
                coords = []
                for day, price in points:
                    coords.extend([x_scale(day), y_scale(price)])
                canvas.create_line(*coords, fill=color, width=2, smooth=True)

            # Moving average line
            ma_points = self.stock_market.moving_average(symbol)
            if len(ma_points) >= 2:
                ma_coords = []
                for day, price in ma_points:
                    ma_coords.extend([x_scale(day), y_scale(price)])
                canvas.create_line(*ma_coords, fill=MA_COLOR, width=1, dash=(3, 3))

            # Prediction line
            proj_points = projections.get(symbol, [])
            if proj_points:
                # Connect forecast to last known point for continuity
                start_chain = []
                if points:
                    start_chain.append(points[-1])
                start_chain.extend(proj_points)
                if len(start_chain) >= 2:
                    proj_coords = []
                    for day, price in start_chain:
                        proj_coords.extend([x_scale(day), y_scale(price)])
                    canvas.create_line(*proj_coords, fill=PRED_COLOR, width=1, dash=(4, 4))

            # Legend item
            legend_y = pad + 14 * idx
            color = STOCK_COLORS.get(symbol, TEXT_PRIMARY)
            canvas.create_rectangle(width - pad - 140, legend_y, width - pad - 125, legend_y + 10, fill=color, outline=color)
            canvas.create_text(width - pad - 115, legend_y + 5, text=symbol, fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 9))

        # Legend for indicators
        legend_base = pad + 14 * (len(symbols_order) + 1)
        canvas.create_rectangle(width - pad - 140, legend_base, width - pad - 125, legend_base + 10, fill=MA_COLOR, outline=MA_COLOR)
        canvas.create_text(width - pad - 115, legend_base + 5, text="MA", fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 9))
        canvas.create_rectangle(width - pad - 140, legend_base + 14, width - pad - 125, legend_base + 24, fill=PRED_COLOR, outline=PRED_COLOR)
        canvas.create_text(width - pad - 115, legend_base + 19, text="Forecast", fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 9))

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_game_over(self):
        if not self.pet.detectLoss():
            return False
        reason = getattr(self.pet, "last_death_reason", "") or "Your pet's wellbeing dropped too low."
        messagebox.showinfo("Game Over", f"{self.pet.name} has died.\n{reason}")
        self.root.destroy()
        return True


if __name__ == "__main__":
    VirtualPetGUI()
