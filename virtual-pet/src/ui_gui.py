import tkinter as tk  # GUI toolkit
from tkinter import messagebox, ttk  # dialogs + themed widgets
import audioop  # raw audio processing helpers
import math  # math helpers for scaling
import os  # filesystem paths
import tempfile  # temp file creation
import wave  # WAV file reading/writing
from pet import Pet, petStats  # pet model + stat profiles
from economy import Economy  # cash tracking
from stock_market import StockMarket  # market simulator

# Theme colors used throughout the UI.
BACKGROUND = "#0f172a"  # app background
CARD_BG = "#111827"  # card background
INPUT_BG = "#0b1220"  # input background
BORDER = "#1f2937"  # borders and separators
TEXT_PRIMARY = "#e5e7eb"  # main text color
TEXT_SECONDARY = "#9ca3af"  # secondary text
ACCENT = "#22c55e"  # primary accent
ACCENT_DARK = "#16a34a"  # active accent
BUTTON_BG = "#2563eb"  # button background
BUTTON_BG_ACTIVE = "#1d4ed8"  # button active state
STOCK_COLORS = {
    "PAW": "#60a5fa",
    "MEOW": "#f472b6",
    "BONE": "#a78bfa",
    "NUT": "#fbbf24",
}

# Absolute path to the assets directory.
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
# Map display names to asset filename slugs.
PET_SLUGS = {
    "dog": "dog",
    "cat": "cat",
    "guinea pig": "guinea-pig",
}

# Default stat profiles used for the GUI.
GUI_PET_PROFILES = {
    "dog": petStats("dog", 40, 80, 70, 90),
    "cat": petStats("cat", 80, 70, 60, 80),
    "guinea pig": petStats("guinea pig", 60, 75, 65, 70, 90),
}

def format_bar(label: str, value: int, max_value: int, width: int = 18) -> str:
    # Normalize values so the bar stays aligned and bounded.
    max_value = max_value or 1
    value = max(0, min(value, max_value))
    filled = int((value / max_value) * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"{label:<12} [{bar}] {value:>3}/{max_value}"


class Tooltip:
    def __init__(self, widget: tk.Widget, text: str, delay_ms: int = 400):
        # Attach a hover tooltip to a widget.
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self._after_id = None
        self._tip = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _schedule(self, _event=None):
        # Wait before showing so it does not flash.
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _show(self):
        # Create a small top-level tooltip window.
        if self._tip:
            return
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self._tip,
            text=self.text,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            font=("Consolas", 10),
            relief="solid",
            bd=1,
            padx=8,
            pady=4
        )
        label.pack()

    def _hide(self, _event=None):
        # Cancel pending show or close the tooltip.
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self._tip:
            self._tip.destroy()
            self._tip = None


class TextTooltip:
    def __init__(self, widget: tk.Text):
        # Tooltip controller that anchors to a text widget.
        self.widget = widget
        self._tip = None

    def show_at(self, text: str, x_root: int, y_root: int):
        # Show tooltip at a specific screen position.
        self.hide()
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x_root}+{y_root}")
        label = tk.Label(
            self._tip,
            text=text,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            font=("Consolas", 10),
            relief="solid",
            bd=1,
            padx=8,
            pady=4
        )
        label.pack()

    def hide(self):
        # Close the tooltip if it exists.
        if self._tip:
            self._tip.destroy()
            self._tip = None


class VirtualPetGUI:
    def __init__(self):
        # Main app setup for the window and state.
        self.root = tk.Tk()
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("1280x720")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Runtime state for pet and economy.
        self.pet = None
        self.economy = None
        # Tooltip instance for stat labels.
        self._stat_tooltip = None
        # Music playback tracking.
        self._music_temp_path = None
        self._music_started = False
        # Cache scaled PhotoImage objects to avoid repeated disk loads.
        self._pet_image_cache = {}
        self._current_pet_image = None

        # Build the initial screen and start the loop.
        self.create_start_screen()
        self.root.mainloop()

    def create_start_screen(self):
        # Build the name/species selection screen.
        self.clear()

        # Intro view for naming and choosing the pet type.
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
        # Validate input and create the game model.
        name = self.name_entry.get().strip()
        ptype = self.pet_type.get()

        if not name:
            messagebox.showerror("Error", "Please give your pet a name.")
            return

        # Pick a stats profile for the selected pet type.
        profile = GUI_PET_PROFILES.get(ptype.lower(), petStats(ptype.lower()))
        self.pet = Pet(name, profile)
        self.economy = Economy()
        self.stock_market = StockMarket(self.economy)

        # Move into the main game layout.
        self.create_game_screen()
        self.root.after(150, self.show_instructions_popup)
        self.start_music()

    def create_game_screen(self):
        # Build notebook tabs for care, economy, and charts.
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

    def start_music(self):
        # Start background music if supported.
        if self._music_started:
            return
        try:
            import winsound
        except ImportError:
            return

        # Load and loop the background track if available.
        music_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "musicfx-dj-1768763823614.wav")
        )
        if not os.path.exists(music_path):
            return

        faded_path = self.create_faded_wav(music_path, fade_seconds=6, volume_scale=0.5)
        if not faded_path:
            return
        self._music_temp_path = faded_path
        self._music_started = True
        winsound.PlaySound(self._music_temp_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def stop_music(self):
        # Stop playback and clean up temp files.
        try:
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
        except ImportError:
            pass
        if self._music_temp_path and os.path.exists(self._music_temp_path):
            try:
                os.remove(self._music_temp_path)
            except OSError:
                pass
        self._music_temp_path = None
        self._music_started = False

    def create_faded_wav(self, input_path: str, fade_seconds: int = 3, volume_scale: float = 1.0):
        # Read a wav file and apply fade-in/out for smoother looping.
        try:
            with wave.open(input_path, "rb") as wf:
                params = wf.getparams()
                frames = wf.readframes(wf.getnframes())
        except (wave.Error, FileNotFoundError):
            return None

        # Apply a fade-in/out and optional volume scaling to avoid harsh loops.
        frame_bytes = params.sampwidth * params.nchannels
        if frame_bytes <= 0:
            return None

        total_frames = params.nframes
        fade_frames = int(params.framerate * fade_seconds)
        fade_frames = min(fade_frames, max(0, total_frames // 2))
        if fade_frames <= 0:
            return input_path

        # Convert frames to a mutable bytearray for processing.
        data = bytearray(frames)
        volume_scale = max(0.0, min(volume_scale, 1.0))

        # Fade in.
        for i in range(fade_frames):
            scale = (i / fade_frames) * volume_scale
            start = i * frame_bytes
            end = start + frame_bytes
            data[start:end] = audioop.mul(data[start:end], params.sampwidth, scale)

        # Fade out.
        for i in range(fade_frames):
            scale = ((fade_frames - i) / fade_frames) * volume_scale
            start = (total_frames - fade_frames + i) * frame_bytes
            end = start + frame_bytes
            data[start:end] = audioop.mul(data[start:end], params.sampwidth, scale)

        # Apply mid-section scaling if requested.
        if volume_scale < 1.0:
            mid_start = fade_frames * frame_bytes
            mid_end = (total_frames - fade_frames) * frame_bytes
            if mid_end > mid_start:
                data[mid_start:mid_end] = audioop.mul(
                    data[mid_start:mid_end], params.sampwidth, volume_scale
                )

        try:
            temp_fd, temp_path = tempfile.mkstemp(suffix=".wav")
            os.close(temp_fd)
            # Write the processed audio to a temp file.
            with wave.open(temp_path, "wb") as wf:
                wf.setparams(params)
                wf.writeframes(bytes(data))
            return temp_path
        except OSError:
            return None

    def show_instructions_popup(self):
        # Show a modal popup with gameplay instructions.
        popup = tk.Toplevel(self.root)
        popup.title("How to Play")
        popup.configure(bg=BACKGROUND)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        popup_width = 760
        popup_height = 520
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (popup_width // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        header = tk.Frame(popup, bg=BACKGROUND, pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Welcome to Virtual Pet Studio",
            font=("Consolas", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=BACKGROUND
        ).pack()
        tk.Label(
            header,
            text="Keep your pet happy, healthy, and well-funded.",
            font=("Consolas", 11),
            fg=TEXT_SECONDARY,
            bg=BACKGROUND
        ).pack()

        card = tk.Frame(popup, bg=CARD_BG, padx=20, pady=16, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=16, pady=10)

        left = tk.Frame(card, bg=CARD_BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(card, bg=CARD_BG)
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        tk.Label(left, text="Care Loop", font=("Consolas", 13, "bold"), fg=ACCENT, bg=CARD_BG).pack(anchor="w")
        tk.Label(
            left,
            text=(
                "- Feed boosts hunger\n"
                "- Play raises happiness\n"
                "- Sleep restores energy\n"
                "- Bathe improves cleanliness\n"
                "- Advance Day progresses time\n"
            ),
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            justify="left"
        ).pack(anchor="w", pady=(6, 12))

        tk.Label(left, text="Your Goal", font=("Consolas", 13, "bold"), fg=ACCENT, bg=CARD_BG).pack(anchor="w")
        tk.Label(
            left,
            text=(
                "Keep all stats healthy.\n"
                "If any stat hits zero,\n"
                "the game ends."
            ),
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            justify="left"
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(right, text="Economy & Stocks", font=("Consolas", 13, "bold"), fg="#60a5fa", bg=CARD_BG).pack(anchor="w")
        tk.Label(
            right,
            text=(
                "- Balance funds your actions\n"
                "- Buy shares to grow wealth\n"
                "- Sell to lock in profits\n"
                "- Charts show market history"
            ),
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            justify="left"
        ).pack(anchor="w", pady=(6, 12))

        tip_frame = tk.Frame(popup, bg=INPUT_BG, padx=14, pady=10, highlightbackground=BORDER, highlightthickness=1)
        tip_frame.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(
            tip_frame,
            text="Pro Tip: Advance Day to move the market and refresh your pet's needs.",
            font=("Consolas", 10, "bold"),
            fg=TEXT_PRIMARY,
            bg=INPUT_BG
        ).pack(anchor="w")

        tk.Button(
            popup,
            text="Start Caring",
            command=popup.destroy,
            bg=ACCENT,
            fg=BACKGROUND,
            activebackground=ACCENT_DARK,
            activeforeground=BACKGROUND,
            font=("Consolas", 12, "bold"),
            relief="flat",
            padx=16,
            pady=6
        ).pack(pady=(0, 12))

    def build_care_tab(self):
        # Assemble the care tab layout and controls.
        container = tk.Frame(self.care_tab, bg=BACKGROUND, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        # Primary panel with pet display and action buttons.
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

        self.stats_label = tk.Text(
            display_frame,
            font=("Consolas", 11),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            relief="flat",
            height=7,
            wrap="none",
            padx=6,
            pady=8
        )
        self.stats_label.pack(fill="x", pady=(8, 0))
        self.stats_label.config(state="disabled")
        self.stats_label.tag_configure("low", foreground="#f87171")
        self.stats_label.tag_configure("normal", foreground=TEXT_PRIMARY)
        self._stat_tooltip = TextTooltip(self.stats_label)
        self.bind_stat_tooltips()

        # Button bar for pet actions.
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

        feed_btn = tk.Button(btn_frame, text="Feed", command=self.feed, **btn_style)
        feed_btn.grid(row=0, column=0, padx=6, pady=6)
        play_btn = tk.Button(btn_frame, text="Play", command=self.play, **btn_style)
        play_btn.grid(row=0, column=1, padx=6, pady=6)
        sleep_btn = tk.Button(btn_frame, text="Sleep", command=self.sleep, **btn_style)
        sleep_btn.grid(row=0, column=2, padx=6, pady=6)
        advance_btn = tk.Button(btn_frame, text="Advance Day", command=self.advance, **btn_style)
        advance_btn.grid(row=0, column=3, padx=6, pady=6)
        shower_btn = tk.Button(btn_frame, text="Bathe/Shower", command=self.shower, **btn_style)
        shower_btn.grid(row=0, column=4, padx=6, pady=6)

        Tooltip(feed_btn, "Spend $10 to reduce hunger.")
        Tooltip(play_btn, "Spend $5 to raise happiness.")
        Tooltip(sleep_btn, "Restore energy without spending money.")
        Tooltip(advance_btn, "Advance time; market prices update.")
        Tooltip(shower_btn, "Spend $8 to improve cleanliness.")

    def build_economy_tab(self):
        # Assemble the economy tab layout and controls.
        container = tk.Frame(self.economy_tab, bg=BACKGROUND, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        # Trading view for balances, prices, and holdings.
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

        buy_btn = tk.Button(control_row, text="Buy", command=self.buy_stock, **action_style)
        buy_btn.grid(row=1, column=2, padx=4, sticky="ew")
        sell_btn = tk.Button(control_row, text="Sell", command=self.sell_stock, **action_style)
        sell_btn.grid(row=1, column=3, padx=4, sticky="ew")
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

        Tooltip(self.balance_label, "Your available cash for pet care and investing.")
        Tooltip(self.portfolio_label, "Estimated value of all shares you own.")
        Tooltip(self.profit_label, "Total profit or loss from all trades.")
        Tooltip(self.market_prices_label, "Current prices for each stock symbol.")
        Tooltip(symbol_menu, "Choose which stock symbol to trade.")
        Tooltip(self.shares_entry, "Enter how many shares to buy or sell.")
        Tooltip(buy_btn, "Buy shares using your balance.")
        Tooltip(sell_btn, "Sell shares to add to your balance.")
        Tooltip(self.holdings_text, "Your current positions and profit/loss per symbol.")
        Tooltip(self.market_message, "Status messages for your trades and market updates.")

    def build_chart_tab(self):
        # Assemble the chart tab layout.
        container = tk.Frame(self.chart_tab, bg=BACKGROUND, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        # Canvas used for the stock price history chart.
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

    def load_pet_image(self, species: str, state: str):
        # Load and scale a pet image for the given species/state.
        species = species.lower()
        state = state.lower()
        slug = PET_SLUGS.get(species, PET_SLUGS["dog"])
        cache_key = (slug, state)
        if cache_key in self._pet_image_cache:
            return self._pet_image_cache[cache_key]

        # Fall back to neutral if a specific state image is missing.
        path = os.path.join(ASSETS_DIR, f"{state}-{slug}.png")
        if not os.path.exists(path) and state != "neutral":
            path = os.path.join(ASSETS_DIR, f"neutral-{slug}.png")
        if not os.path.exists(path):
            return None
        try:
            image = tk.PhotoImage(file=path)
        except tk.TclError:
            return None

        # Subsample large sprites to fit the display panel.
        max_dim = 320
        scale = max(1, int(math.ceil(max(image.width(), image.height()) / max_dim)))
        if scale > 1:
            image = image.subsample(scale, scale)

        # Store in cache to reuse later.
        self._pet_image_cache[cache_key] = image
        return image

    def update_ui(self):
        # Refresh pet display and stat readout.
        state = self.pet.get_emotional_state()
        species = getattr(self.pet, "species", getattr(self.pet.pet_type, "type", "dog")).lower()
        image = self.load_pet_image(species, state)
        if image:
            self.pet_display.config(image=image, text="")
            self._current_pet_image = image
        else:
            self.pet_display.config(image="", text="(missing image)")
            self._current_pet_image = None

        # Update the stat readout and color tags in the text widget.
        stats = self.pet.pet_type
        lines = [
            (f"{self.pet.name} - {species.title()}\n", ["normal"]),
            self.format_bar_line("Hunger", self.pet.hunger, stats.hunger),
            self.format_bar_line("Happiness", self.pet.happiness, stats.happiness),
            self.format_bar_line("Health", self.pet.health, stats.health),
            self.format_bar_line("Energy", self.pet.energy, stats.energy),
            self.format_bar_line("Cleanliness", self.pet.cleanliness, stats.cleanliness),
            (f"Balance:      ${self.economy.balance}\n", ["normal"]),
        ]
        self.stats_label.config(state="normal")
        self.stats_label.delete("1.0", "end")
        for text, tags in lines:
            self.stats_label.insert("end", text, tuple(tags))
        self.stats_label.config(state="disabled")
        self.update_economy_ui()

    def format_bar_line(self, label: str, value: int, max_value: int):
        # Format one stat line with a color tag.
        line = format_bar(label, value, max_value) + "\n"
        max_value = max_value or 1
        ratio = max(0, min(value, max_value)) / max_value
        color_tag = "low" if ratio <= 0.25 else "normal"
        stat_tag = f"stat_{label.lower()}"
        return line, [stat_tag, color_tag]

    def bind_stat_tooltips(self):
        # Bind tooltip text to stat labels.
        tooltips = {
            "stat_hunger": "Increases: Feed.  Decreases: Time passing, Play.",
            "stat_happiness": "Increases: Play.  Decreases: Time passing, Bathe.",
            "stat_health": "Increases: Overall good care, feed.  Decreases: Neglect of other stats.",
            "stat_energy": "Increases: Sleep.  Decreases: Play, time passing.",
            "stat_cleanliness": "Increases: Bathe/Shower.  Decreases: Time passing.",
        }

        for tag, text in tooltips.items():
            self.stats_label.tag_bind(tag, "<Enter>", lambda e, t=text: self._show_stat_tip(e, t))
            self.stats_label.tag_bind(tag, "<Motion>", lambda e, t=text: self._show_stat_tip(e, t))
            self.stats_label.tag_bind(tag, "<Leave>", lambda e: self._hide_stat_tip())

    def _show_stat_tip(self, event, text: str):
        # Show stat tooltip near the cursor.
        if not self._stat_tooltip:
            return
        x = event.x_root + 12
        y = event.y_root + 12
        self._stat_tooltip.show_at(text, x, y)

    def _hide_stat_tip(self):
        # Hide the stat tooltip.
        if self._stat_tooltip:
            self._stat_tooltip.hide()

    def update_economy_ui(self):
        # Update economy labels and holdings list.
        if not hasattr(self, "stock_market"):
            return
        # Sync labels and holdings with the latest market values.
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
        # Feed action: spend money and reduce hunger.
        if self.economy.spend("food", 10):
            self.pet.feed(20)
        self.update_ui()
        self.check_game_over()

    def play(self):
        # Play action: spend money and raise happiness.
        if self.economy.spend("toys", 5):
            self.pet.play(10)
        self.update_ui()
        self.check_game_over()

    def sleep(self):
        # Sleep action: restore energy without spending.
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
        # Bath action: spend money and improve cleanliness.
        if self.economy.spend("grooming", 8):
            self.pet.shower(5)
        self.update_ui()
        self.check_game_over()

    def buy_stock(self):
        # Attempt to buy shares based on the entry field.
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
        # Attempt to sell shares based on the entry field.
        try:
            shares = int(self.shares_entry.get() or "0")
        except ValueError:
            self.market_message.config(text="Enter a whole number of shares.", fg="#fca5a5")
            return

        success, msg = self.stock_market.sell(self.market_symbol.get(), shares)
        self.market_message.config(text=msg, fg="#22c55e" if success else "#fca5a5")
        self.update_economy_ui()
        self.update_ui()

    def draw_chart(self):
        # Render the stock history chart to the canvas.
        if not hasattr(self, "chart_canvas") or not hasattr(self, "stock_market"):
            return
        canvas = self.chart_canvas
        canvas.delete("all")

        history = self.stock_market.price_history()
        if not history:
            return

        # Determine bounds
        all_points = [(day, price) for points in history.values() for day, price in points]
        if not all_points:
            return
        min_day = min(d for d, _ in all_points)
        max_day = max(d for d, _ in all_points)
        min_price = min(p for _, p in all_points)
        max_price = max(p for _, p in all_points)

        # Compute drawing bounds based on the current canvas size.
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

        # Gridlines for nicer readability
        grid_lines = 4
        for i in range(1, grid_lines + 1):
            y = pad + (height - 2 * pad) * i / (grid_lines + 1)
            canvas.create_line(pad, y, width - pad, y, fill="#1f2937", dash=(2, 2))

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

            # Legend item
            legend_y = pad + 14 * idx
            color = STOCK_COLORS.get(symbol, TEXT_PRIMARY)
            canvas.create_rectangle(width - pad - 140, legend_y, width - pad - 125, legend_y + 10, fill=color, outline=color)
            canvas.create_text(width - pad - 115, legend_y + 5, text=symbol, fill=TEXT_PRIMARY, anchor="w", font=("Consolas", 9))

    def clear(self):
        # Remove all widgets from the root window.
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_game_over(self):
        # Stop the game if the pet reaches a loss state.
        if not self.pet.detectLoss():
            return False
        reason = getattr(self.pet, "last_death_reason", "") or "Your pet's wellbeing dropped too low."
        messagebox.showinfo("Game Over", f"{self.pet.name} has died.\n{reason}")
        self.stop_music()
        self.root.destroy()
        return True

    def on_close(self):
        # Handle window close events.
        self.stop_music()
        self.root.destroy()


if __name__ == "__main__":
    # Launch the GUI when run directly.
    VirtualPetGUI()
