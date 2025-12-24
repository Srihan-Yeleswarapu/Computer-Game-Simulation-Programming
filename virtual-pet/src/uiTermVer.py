# Ui.py
# ui.py
import os
import time

# ---------- Utility ----------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause(seconds=1):
    time.sleep(seconds)

def progress_bar(label, value, max_value=100, length=20):
    filled = int(length * value / max_value)
    bar = "█" * filled + "-" * (length - filled)
    return f"{label:12} [{bar}] {value}/{max_value}"

# ---------- Title Screen ----------
def title_screen():
    clear_screen()
    print("=" * 50)
    print("🐾 VIRTUAL PET SIMULATOR 🐾".center(50))
    print("=" * 50)
    print("Don't just own a pet, experience the joy and responsibility of caring for a virtual companion!")
    print("Press ENTER")
    input()

# ---------- Pet Display ----------
def show_pet(pet):
    print("\n🐶 PET STAT")
    print("-" * 50)
    print(f"Name: {pet.name}")
    print(f"Type: {pet.pet_type}")
    print(f"Age:  {pet.age_days} days")
    print(f"State: {pet.get_emotional_state().upper()}\n")

    print(progress_bar("hunger", pet.hunger, pet.pet_type.hunger))
    print(progress_bar("happiness", pet.happiness, pet.pet_type.happiness))
    print(progress_bar("health", pet.health, pet.pet_type.health))
    print(progress_bar("energy", pet.energy, pet.pet_type.energy))
    print(progress_bar("cleanliness", pet.cleanliness, pet.pet_type.cleanliness))
# ---------- Economy Display ----------
def show_economy(economy):
    print("\n💰 ECONOMY")
    print("-" * 50)
    print(f"Balance: ${economy.balance}")
    print("\nExpenses:")
    for category, amount in economy.expenses.items():
        print(f"  {category.capitalize():12} ${amount}")

# ---------- Main Menu ----------
def show_menu():
    print("\n🎮 ACTIONS")
    print("-" * 50)
    print("1. Feed pet ($10)")
    print("2. Play with pet ($5)")
    print("3. Sleep")
    print("4. Bath")
    print("5. Advance time")
    print("6. Show expenses")
    print("7. Save game")
    print("8. Load game")
    print("9. Quit")

# ---------- Messages ----------
def success(msg):
    print(f"\n✅ {msg}")
    pause(1)

def warning(msg):
    print(f"\n⚠️  {msg}")
    pause(1)

def game_over_screen(pet):
    clear_screen()
    print("💀 GAME OVER 💀".center(50))
    print("=" * 50)
    print(f"\n{pet.name} died, bcz you didn't treat it well.")
    print("Your clearly messed something up. You should play more to get better at the game.")
    print("Thanks for playing!")
    pause(3)
