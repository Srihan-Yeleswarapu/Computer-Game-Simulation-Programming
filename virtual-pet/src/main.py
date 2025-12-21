# Main.py
from pet import Pet
from economy import Economy

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
            duration = int(input("Enter hours of sleep: "))
            pet.sleep(duration)
            print(f"{pet.name} slept for {duration} hours.")
        elif choice == "4":
            days = int(input("Advance how many days? "))
            pet.pass_time(days)
            print(f"{days} day(s) have passed.")
        elif choice == "5":
            economy.report()
        elif choice == "6":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
    
    
if __name__ == "__main__":
    main()