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
    print("\nCare for your pet, manage money, and see how your")
    print("choices affect its happiness and health.\n")
    print("Press ENTER to begin...")
    input()

# ---------- Pet Display ----------
def show_pet(pet):
    print("\n🐶 PET STATUS")
    print("-" * 50)
    print(f"Name: {pet.name}")
    print(f"Type: {pet.pet_type}")
    print(f"Age:  {pet.age_days} days")
    print(f"State: {pet.get_emotional_state().upper()}\n")

    print(progress_bar("Hunger", pet.hunger))
    print(progress_bar("Happiness", pet.happiness))
    print(progress_bar("Health", pet.health))
    print(progress_bar("Energy", pet.energy))
    print(progress_bar("Cleanliness", pet.cleanliness))

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
    print("4. Advance time")
    print("5. Show expenses")
    print("6. Save game")
    print("7. Load game")
    print("8. Quit")

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
    print(f"\n{pet.name} could not be cared for anymore.")
    print("Your choices matter.\n")
    print("Thanks for playing!")
    pause(3)
