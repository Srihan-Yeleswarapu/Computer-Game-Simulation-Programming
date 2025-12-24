import tkinter as tk
from tkinter import messagebox
from pet import Pet
from economy import Economy

# =========================
# ASCII PET SKINS
# =========================

PET_SKINS = {
    "dog": {
        "happy": r"""
 /\_/\ 
( ^_^ )
 /   \
""",
        "sad": r"""
 /\_/\ 
( T_T )
 /   \
""",
        "hungry": r"""
 /\_/\ 
( o_o )
 /   \
""",
        "dirty": r"""
 /\_/\ 
( >_< )
 /xxx\
""",
        "excited": r"""
 /\_/\ 
( ^O^ )
 /   \
""",
        "bored": r"""
 /\_/\ 
( -_- )
 /   \
"""
    },

    "cat": {
        "happy": r"""
 /\_/\ 
( =^.^= )
  > ^ <
""",
        "sad": r"""
 /\_/\ 
( =T.T= )
  > ^ <
""",
        "hungry": r"""
 /\_/\ 
( =o.o= )
  > ^ <
""",
        "dirty": r"""
 /\_/\ 
( =>_< )
  >xxx<
""",
        "excited": r"""
 /\_/\ 
( =^O^= )
  > ^ <
""",
        "bored": r"""
 /\_/\ 
( =-.-= )
  > ^ <
"""
    },

    "guinea pig": {
        "happy": r"""
 (____)
 ( ^_^ )
 /____\
""",
        "sad": r"""
 (____)
 ( T_T )
 /____\
""",
        "hungry": r"""
 (____)
 ( o_o )
 /____\
""",
        "dirty": r"""
 (____)
 ( >_< )
 /xxxx\
""",
        "excited": r"""
 (____)
 ( ^O^ )
 /____\
""",
        "bored": r"""
 (____)
 ( -_- )
 /____\
"""
    }
}


class VirtualPetGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("600x500")
        self.root.configure(bg="#1e1e1e")

        self.pet = None
        self.economy = None

        self.create_start_screen()
        self.root.mainloop()



    def create_start_screen(self):
        self.clear()

        title = tk.Label(
            self.root,
            text="🐾 Virtual Pet Simulator 🐾",
            font=("Courier", 20, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        title.pack(pady=20)

        tk.Label(self.root, text="Pet Name:", fg="white", bg="#1e1e1e").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Pet Type:", fg="white", bg="#1e1e1e").pack()
        self.pet_type = tk.StringVar(value="dog")
        tk.OptionMenu(self.root, self.pet_type, "dog", "cat", "guinea pig").pack()

        tk.Button(
            self.root,
            text="Start Game",
            command=self.start_game,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)



    def start_game(self):
        name = self.name_entry.get()
        ptype = self.pet_type.get()

        if not name:
            messagebox.showerror("Error", "Name your pet!")
            return

        self.pet = Pet(name, ptype)
        self.economy = Economy()

        self.create_game_screen()


    def create_game_screen(self):
        self.clear()

        self.pet_display = tk.Label(
            self.root,
            font=("Courier", 14),
            fg="white",
            bg="#1e1e1e",
            justify="center"
        )
        self.pet_display.pack(pady=10)

        self.stats_label = tk.Label(
            self.root,
            font=("Courier", 10),
            fg="white",
            bg="#1e1e1e"
        )
        self.stats_label.pack()

        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Feed", command=self.feed).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Play", command=self.play).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Sleep", command=self.sleep).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Advance Day", command=self.advance).grid(row=0, column=3, padx=5)

        self.update_ui()


    def update_ui(self):
        state = self.pet.get_emotional_state()
        skin = PET_SKINS[self.pet.pet_type].get(state, "")

        self.pet_display.config(text=skin)

        self.stats_label.config(
            text=(
                f"{self.pet.name} ({self.pet.pet_type})\n"
                f"Hunger: {self.pet.hunger}\n"
                f"Happiness: {self.pet.happiness}\n"
                f"Health: {self.pet.health}\n"
                f"Energy: {self.pet.energy}\n"
                f"Cleanliness: {self.pet.cleanliness}\n"
                f"Balance: ${self.economy.balance}"
            )
        )


    def feed(self):
        if self.economy.spend("food", 10):
            self.pet.feed(20)
        self.update_ui()

    def play(self):
        if self.economy.spend("toys", 5):
            self.pet.play(10)
        self.update_ui()

    def sleep(self):
        self.pet.sleep(5)
        self.update_ui()

    def advance(self):
        self.pet.pass_time(1)
        self.update_ui()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    VirtualPetGUI()
