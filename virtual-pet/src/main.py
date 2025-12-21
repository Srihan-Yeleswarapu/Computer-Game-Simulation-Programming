# Main.py
from pet import Pet
from economy import Economy
import json 

def print_pet_status(pet: Pet):
    print(f"Pet Name: {pet.name}")
    print(f"Type: {pet.pet_type}")
    print(f"Age (days): {pet.age_days}")
    print(f"Hunger: {pet.hunger}")
    print(f"Happiness: {pet.happiness}")
    print(f"Health: {pet.health}")
    print(f"Energy: {pet.energy}")
    print(f"Cleanliness: {pet.cleanliness}")
    print(f"Emotional State: {pet.get_emotional_state()}")
    print("")
    
# --- Save/Load Functions ---
def save_game(pet, economy, filename="save.json"):
    data = {
        "pet": pet.__dict__,
        "economy": {
            "balance": economy.balance,
            "expenses": economy.expenses
        }
    }
    with open(filename, "w") as f:
        json.dump(data, f)

def load_game(filename="save.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    pet_data = data["pet"]
    economy_data = data["economy"]
    
    pet = Pet(pet_data["name"], pet_data["pet_type"], pet_data["age_days"])
    pet.hunger = pet_data["hunger"]
    pet.happiness = pet_data["happiness"]
    pet.health = pet_data["health"]
    pet.energy = pet_data["energy"]
    pet.cleanliness = pet_data["cleanliness"]
    
    economy = Economy(economy_data["balance"])
    economy.expenses = economy_data["expenses"]
    
    return pet, economy
# --- End of Save/Load ---

    
def main():
    # Create pet and economy
    name = input("Enter your pet's name: ")
    pet_type = input("Enter pet type (e.g., dog, cat, dragon): ")
    pet = Pet(name, pet_type)
    economy = Economy(starting_balance=1000)

    while True:
        print_pet_status(pet)
        print(f"Current Balance: ${economy.get_balance()}")
        print("\nActions:")
        print("1. Feed pet ($10 per feed)")
        print("2. Play with pet ($5 per play)")
        print("3. Sleep")
        print("4. Advance time")
        print("5. Show expenses report")
        print("6. Quit")

        choice = input("Choose an action: ")

        if choice == "1":
            cost = 10
            if economy.spend("food", cost):
                pet.feed(20)  # increase hunger by 20
                print(f"{pet.name} was fed!")
        elif choice == "2":
            cost = 5
            if economy.spend("toys", cost):
                pet.play(15)  # increase happiness by 15
                print(f"{pet.name} played and is happier!")
        elif choice == "3":
            try:
                duration = get_int_input("Enter hours of sleep: ", 0, 24)
                pet.sleep(duration)
                print(f"{pet.name} slept for {duration} hours.")
            except ValueError:
                print("Please enter a valid number. ")
        elif choice == "4":
            try: 
                days = int(input("Advance how many days? "))
                pet.pass_time(days)
                print(f"{days} day(s) have passed.")
            except ValueError:
                print("Please enter a valid number: ")
        elif choice == "5":
            economy.report()
        elif choice == "6":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            
def __str__(self):
    return (f"{self.name} ({self.pet_type}) - Age: {self.age_days} days\n"
                f"Hunger: {self.hunger}, Happiness: {self.happiness}, Health: {self.health}\n"
                f"Energy: {self.energy}, Cleanliness: {self.cleanliness}, State: {self.get_emotional_state()}")
    
def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
