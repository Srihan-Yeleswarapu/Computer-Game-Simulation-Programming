# Main.py - Entry point for the Virtual Pet game application
# Imports the UI module for terminal-based user interface
import uiTermVer as ui
# Imports Pet class and petStats data structure for pet management
from pet import Pet, petStats
# Imports Economy class for managing in-game currency and expenses
from economy import Economy
# Imports json module for save/load game data persistence
import json 
# Imports random module for generating random events
import random

# Defines a list of available pet types with their stats (type, cost, max_hunger, max_happiness, max_health, max_energy, max_cleanliness)
validPets = [petStats("dog", 10, 80, 70, 90), petStats("cat", 5, 70, 60, 80), petStats("dragon", 15, 90, 80, 100)]
# Displays the title/welcome screen to the user
ui.title_screen()

# Function to display all current pet statistics in a readable format
def print_pet_status(pet: Pet):
    # Prints the pet's name
    print(f"Pet Name: {pet.name}")
    # Prints the type of pet (dog, cat, dragon, etc.)
    print(f"Type: {pet.pet_type}")
    # Prints the pet's age in days
    print(f"Age (days): {pet.age_days}")
    # Prints the pet's current hunger level
    print(f"Hunger: {pet.hunger}")
    # Prints the pet's current happiness level
    print(f"Happiness: {pet.happiness}")
    # Prints the pet's current health level
    print(f"Health: {pet.health}")
    # Prints the pet's current energy level
    print(f"Energy: {pet.energy}")
    # Prints the pet's current cleanliness level
    print(f"Cleanliness: {pet.cleanliness}")
    # Prints the pet's current emotional state based on its stats
    print(f"Emotional State: {pet.get_emotional_state()}")
    # Prints a blank line for formatting
    print("")
    
# --- Save/Load Functions ---
# Function to serialize the current game state (pet and economy) to a JSON file
def save_game(pet, economy, filename="save.json"):
    # Creates a dictionary containing all relevant pet and economy data
    data = {
        # Stores all pet-related data
        "pet": {
            # Saves the pet's name
            "name": pet.name,
            # Saves the pet's type (extracting type from the petStats object)
            "pet_type": pet.pet_type.type,
            # Saves the pet's age in days
            "age_days": pet.age_days,
            # Saves the pet's hunger level
            "hunger": pet.hunger,
            # Saves the pet's happiness level
            "happiness": pet.happiness,
            # Saves the pet's health level
            "health": pet.health,
            # Saves the pet's energy level
            "energy": pet.energy,
            # Saves the pet's cleanliness level
            "cleanliness": pet.cleanliness
        },
        # Stores all economy-related data
        "economy": {
            # Saves the player's current balance
            "balance": economy.balance,
            # Saves the player's expense tracking data
            "expenses": economy.expenses
        }
    }
    # Opens the save file in write mode (creates it if it doesn't exist)
    with open(filename, "w") as f:
        # Converts the data dictionary to JSON format and writes it to the file
        json.dump(data, f)

# Function to deserialize a saved game from a JSON file and reconstruct the game state
def load_game(filename="save.json"):
    # Opens the save file in read mode
    with open(filename, "r") as f:
        # Parses the JSON data from the file into a Python dictionary
        data = json.load(f)
    # Extracts the pet data from the loaded dictionary
    pet_data = data["pet"]
    # Extracts the economy data from the loaded dictionary
    economy_data = data["economy"]

    # Finds the pet stats object that matches the saved pet type from the validPets list
    # Creates a new Pet object with the saved data
    pet = Pet(pet_data["name"], [pet for pet in validPets if pet.type == pet_data["pet_type"]][0], pet_data["age_days"])
    # Restores the pet's hunger level from the saved data
    pet.hunger = pet_data["hunger"]
    # Restores the pet's happiness level from the saved data
    pet.happiness = pet_data["happiness"]
    # Restores the pet's health level from the saved data
    pet.health = pet_data["health"]
    # Restores the pet's energy level from the saved data
    pet.energy = pet_data["energy"]
    # Restores the pet's cleanliness level from the saved data
    pet.cleanliness = pet_data["cleanliness"]
    
    # Creates a new Economy object with the saved balance
    economy = Economy(economy_data["balance"])
    # Restores the economy's expense tracking data
    economy.expenses = economy_data["expenses"]
    
    # Returns both the reconstructed pet and economy objects
    return pet, economy
# --- End of Save/Load ---

# Function to randomly trigger special events during gameplay with a 20% chance per action
def random_event(pet, economy):
    """Occasionally triggers a random event."""
    # Defines a list of lambda functions, each representing a possible random event
    events = [
        # Event 1: Pet finds a toy and gains 10 happiness (capped at 100)
        lambda: setattr(pet, "happiness", min(100, pet.happiness + 10)) or print(f"{pet.name} found a toy and got happier!"),
        # Event 2: Pet gets sick and loses 5 health points
        lambda: setattr(pet, "health", max(0, pet.health - 5)) or print(f"{pet.name} got a little sick..."),
        # Event 3: Player finds $50 and adds it to their balance
        lambda: economy.earn(50) or print("You found $50!"),
        # Event 4: Pet gets dirty outside and loses 10 cleanliness points
        lambda: setattr(pet, "cleanliness", max(0, pet.cleanliness - 10)) or print(f"{pet.name} got dirty outside!")
    ]
    # Generates a random number between 0 and 1; if less than 0.2 (20% chance), execute an event
    if random.random() < 0.2:  # 20% chance per action
        # Randomly selects one event from the events list and executes it
        random.choice(events)()

# Main game loop function that handles all gameplay
def main():
    # Prompts the user to enter a name for their pet
    name = input("Enter your pet's name: ")
    # Prompts the user to select a pet type
    pet_type = input("Enter pet type (e.g., dog, cat, dragon): ")
    # Validates the pet type input by checking if it exists in the validPets list; keeps asking until valid
    while(pet_type.lower() not in [pet.type for pet in validPets]):
        # Re-prompts the user if they entered an invalid pet type
        pet_type = input("Enter pet type (e.g., dog, cat, dragon): ")
    # Finds and extracts the petStats object for the chosen pet type
    petStat = [pet for pet in validPets if pet.type == pet_type.lower()][0]
    # Creates a new Pet object with the user's chosen name and pet type
    pet = Pet(name, petStat, age_days=0)
    # Creates a new Economy object with an initial balance of $1000
    economy = Economy(starting_balance=1000)

    # Infinite loop that continues until the user chooses to quit
    while True:
        # Clears the terminal screen to refresh the display
        ui.clear_screen()
        # Displays the current pet's visual representation and stats
        ui.show_pet(pet)
        # Displays the current economy status (balance and expenses)
        ui.show_economy(economy)
        # Displays the main menu options to the user
        ui.show_menu()

        # print("\nActions:")
        # print("1. Feed pet ($10 per feed)")
        # print("2. Play with pet ($5 per play)")
        # print("3. Sleep")
        # print("4. Advance time")
        # print("5. Show expenses report")
        # print("6. Save game")
        # print("7. Load game")
        # print("8. Quit")

        choice = input("Choose an action: ")

        # Checks if the user chose to feed the pet (option 1)
        if choice == "1":
            # Sets the cost of feeding the pet to $10
            cost = 10
            # Attempts to spend $10 from the economy; if successful, proceeds with feeding
            if economy.spend("food", cost):
                # Feeds the pet, reducing hunger and increasing satisfaction
                pet.feed(20)
                # Prints a confirmation message
                print(f"{pet.name} was fed!")
            # Triggers a random event with 20% probability
            random_event(pet, economy)
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")

        # Checks if the user chose to play with the pet (option 2)
        elif choice == "2":
            # Sets the cost of playing with the pet to $5
            cost = 5
            # Attempts to spend $5 from the economy; if successful, proceeds with playing
            if economy.spend("toys", cost):
                # Plays with the pet, increasing happiness and reducing boredom
                pet.play(15)
                # Prints a confirmation message
                print(f"{pet.name} played and is happier!")
            # Triggers a random event with 20% probability
            random_event(pet, economy)
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to let the pet sleep (option 3)
        elif choice == "3":
            # Prompts the user to input hours of sleep (must be between 0 and 24)
            duration = get_int_input("Enter hours of sleep: ", 0, 24)
            # Commands the pet to sleep for the specified duration
            pet.sleep(duration)
            # Prints a confirmation message with the duration
            print(f"{pet.name} slept for {duration} hours.")
            # Triggers a random event with 20% probability
            random_event(pet, economy)
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to shower the pet (option 4)
        elif choice == "4":
            # Prompts the user to input shower duration in minutes (must be between 1 and 30)
            duration = get_int_input("Enter minutes of bath: ", 1, 30)
            # Commands the pet to shower for the specified duration
            pet.shower(duration)
            # Prints a confirmation message with the duration
            print(f"{pet.name} took a bath for {duration} minutes.")
            # Triggers a random event with 20% probability
            random_event(pet, economy)
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to advance time (option 5)
        elif choice == "5":
            # Prompts the user to input how many days to advance (minimum 1 day)
            days = get_int_input("Advance how many days? ", 1)
            # Advances the pet's time by the specified number of days, aging and changing stats
            pet.pass_time(days)
            # Prints a confirmation message with the number of days
            print(f"{days} day(s) have passed.")
            # Triggers a random event with 20% probability
            random_event(pet, economy)
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to view expenses report (option 6)
        elif choice == "6":
            # Displays a detailed report of all expenses incurred
            economy.report()
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to save the game (option 7)
        elif choice == "7":
            # Saves the current game state to a file
            save_game(pet, economy)
            # Displays a success message to the user
            ui.success("Game saved successfully!")
        # Checks if the user chose to load a previously saved game (option 8)
        elif choice == "8":
            # Attempts to load a previously saved game
            try:
                # Calls the load_game function to restore pet and economy from save file
                pet, economy = load_game()
                # Prints a success message if the game loaded correctly
                print("Game loaded successfully!")
            # Catches the error if no save file exists
            except FileNotFoundError:
                # Displays a warning message if no save file is found
                ui.warning("No save file found.")
        # Checks if the user chose to quit the game (option 9)
        elif choice == "9":
            # Prints a farewell message
            print("Exiting the game. Goodbye!")
            # Breaks out of the infinite game loop, ending the program
            break
        # Handles any invalid input that doesn't match the valid choices
        else:
            # Prints an error message prompting the user to try again
            print("Invalid choice. Try again.")

            
#def __str__(self):
#    return (f"{self.name} ({self.pet_type}) - Age: {self.age_days} days\n"
#            f"Hunger: {self.hunger}, Happiness: {self.happiness}, Health: {self.health}\n"
#            f"Energy: {self.energy}, Cleanliness: {self.cleanliness}, State: {self.get_emotional_state()}")
    
# Helper function to safely get integer input from the user with validation
def get_int_input(prompt, min_val=None, max_val=None):
    # Infinite loop that continues until valid input is received
    while True:
        # Attempts to convert user input to an integer
        try:
            # Converts the input string to an integer value
            val = int(input(prompt))
            # Checks if the value is within the specified minimum and maximum bounds
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                # Prints an error message showing the valid range
                print(f"Enter a value between {min_val} and {max_val}.")
                # Continues the loop to ask for input again
                continue
            # Returns the valid integer value to the caller
            return val
        # Catches the error if the input cannot be converted to an integer
        except ValueError:
            # Prints an error message asking for a valid number
            print("Please enter a valid number.")


# Checks if this file is being run directly (not imported as a module)
if __name__ == "__main__":
    # Calls the main game loop function to start the game
    main()
