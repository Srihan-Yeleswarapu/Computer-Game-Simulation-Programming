# Pet.py
# Import the ui module for terminal-based user interface functions
import uiTermVer as ui
# Import dataclass decorator to create lightweight data container classes
from dataclasses import dataclass
# Import Enum for creating enumeration types
from enum import Enum
# Import type hints for optional and union types
from typing import Optional, Union

# Define a dataclass that holds the base stats for a pet species
@dataclass
class petStats:
    # The type/species name of the pet (e.g., "dog", "cat")
    type: str
    # The maximum hunger level for this pet species (default 100)
    hunger: int = 100
    # The maximum happiness level for this pet species (default 100)
    happiness: int = 100
    # The maximum health level for this pet species (default 100)
    health: int = 100
    # The maximum energy level for this pet species (default 100)
    energy: int = 100
    # The maximum cleanliness level for this pet species (default 100)
    cleanliness: int = 100

# Define the Pet class to represent an individual virtual pet instance
class Pet:
    # Constructor that initializes a pet with name, type, age, and optional UI flag
    def __init__(self, name: str, pet_type: Union[petStats, str], age_days: int = 0, use_terminal_ui: bool = True):
        # Store the pet's name
        self.name = name

        # Check if pet_type is already a petStats object or if it's a string species name
        if isinstance(pet_type, petStats):
            # Use the provided petStats profile directly
            self.pet_profile = pet_type
        else:
            # Create a new petStats with default values using the string as the species type
            self.pet_profile = petStats(pet_type.lower())

        # Keep compatibility with code that expects pet_type to expose stat caps
        self.pet_type = self.pet_profile
        # Store the species/type name for easy access
        self.species = self.pet_profile.type

        # Initialize hunger stat to the maximum value from the pet profile
        self.hunger = 1 * self.pet_profile.hunger
        # Initialize happiness stat to the maximum value from the pet profile
        self.happiness = 1 * self.pet_profile.happiness
        # Initialize health stat to the maximum value from the pet profile
        self.health = 1 * self.pet_profile.health
        # Initialize energy stat to the maximum value from the pet profile
        self.energy = 1 * self.pet_profile.energy
        # Initialize cleanliness stat to the maximum value from the pet profile
        self.cleanliness = 1 * self.pet_profile.cleanliness
        # Store the pet's age in days
        self.age_days = age_days
        # Track how many consecutive emotional states the pet has been sad
        self.sad_streak = 0
        # Store the reason for the pet's death/loss condition
        self.last_death_reason = ""
        # Store whether to use terminal UI for game over screen
        self.use_terminal_ui = use_terminal_ui
        
    # Method to ensure all stats stay within valid bounds (0 to max)
    def clamp_stats(self):
        # Get the max stat values from the pet's profile
        max_stats = self.pet_profile
        # Ensure hunger is between 0 and the max hunger value
        self.hunger = max(0, min(1 * max_stats.hunger, self.hunger))
        # Ensure happiness is between 0 and the max happiness value
        self.happiness = max(0, min(1 * max_stats.happiness, self.happiness))
        # Ensure health is between 0 and the max health value
        self.health = max(0, min(1 * max_stats.health, self.health))
        # Ensure energy is between 0 and the max energy value
        self.energy = max(0, min(1 * max_stats.energy, self.energy))
        # Ensure cleanliness is between 0 and the max cleanliness value
        self.cleanliness = max(0, min(1 * max_stats.cleanliness, self.cleanliness))
        # Ensure age is not negative
        self.age_days = max(0, self.age_days)
        
    # Method to advance time by a specified number of days, degrading stats
    def pass_time(self, days=1):
        # Loop through each day to advance
        for _ in range(days):
            # Increment the pet's age by 1 day
            self.age_days += 1
            # Decrease hunger stat by 2 per day
            self.hunger -= 2
            # Decrease happiness stat by 2 per day
            self.happiness -= 2
            # Decrease energy stat by 2 per day
            self.energy -= 2
            # Decrease cleanliness stat by 2 per day
            self.cleanliness -= 2
            
            # If hunger or cleanliness gets too low, degrade health
            if self.hunger < 20 or self.cleanliness < 20:
                # Decrease health by 5 if either condition is met
                self.health -= 5
            # Clamp all stats to their valid ranges
            self.clamp_stats()
            # Update the sad streak counter based on current emotional state
            self._update_sad_streak()
            # Check if the pet has reached a loss condition; break if true
            if self.detectLoss(trigger_ui=self.use_terminal_ui):
                break
                
    # Method to determine the pet's current emotional state based on stats
    def get_emotional_state(self):
        # If health is critically low, the pet is sick
        if self.health < 30:
            return "sick"
        # If hunger is critically low, the pet is hungry
        if self.hunger < 30:
            return "hungry"
        # If energy is critically low, the pet is tired
        if self.energy < 30:
            return "tired"
        # If cleanliness is critically low, the pet is dirty
        if self.cleanliness < 30:
            return "dirty"
        # If happiness is critically low, the pet is sad
        if self.happiness < 30:
            return "sad"
        # If happiness is high, the pet is happy
        if self.happiness > 70:
            return "happy"
        # Otherwise, the pet is in a neutral state
        return "neutral"
            
    # Method to make the pet sleep, which restores energy and reduces hunger
    def sleep(self, duration):
        # Increase energy by 10 times the duration
        self.energy += duration * 10
        # Decrease hunger by 2 times the duration
        self.hunger -= duration * 2
        # Re-apply energy increase (redundant but kept for code structure)
        self.energy = min(100, self.energy + duration * 10)
        # Clamp all stats to ensure they stay within valid bounds
        self.clamp_stats()
        # Update the sad streak counter
        self._update_sad_streak()

    # Method to feed the pet, which reduces hunger and improves health
    def feed(self, amount):
        # Increase hunger reduction by the feed amount
        self.hunger += amount
        # Increase health by 1/5 of the feed amount
        self.health += amount // 5
        # Clamp all stats to ensure they stay within valid bounds
        self.clamp_stats()
        # Update the sad streak counter
        self._update_sad_streak()

    # Method to bathe/shower the pet, improving cleanliness at the cost of happiness
    def shower(self, amount):
        # Decrease happiness by 2 times the shower duration
        self.happiness -= amount *2
        # Increase cleanliness by 4 times the shower duration
        self.cleanliness += amount * 4
        # Clamp all stats to ensure they stay within valid bounds
        self.clamp_stats()
        # Update the sad streak counter
        self._update_sad_streak()

    # Method to play with the pet, which increases happiness but costs energy and hunger
    def play(self, duration):
        # Increase happiness by 5 times the play duration
        self.happiness += duration * 5
        # Decrease energy by 3 times the play duration
        self.energy -= duration * 3
        # Decrease hunger by 2 times the play duration
        self.hunger -= duration * 2
        # Re-apply happiness increase capped at 100 (redundant but kept for structure)
        self.happiness = min(100, self.happiness + duration)
        # Clamp all stats to ensure they stay within valid bounds
        self.clamp_stats()
        # Update the sad streak counter
        self._update_sad_streak()

    # Method to update the sad streak counter based on emotional state
    def _update_sad_streak(self):
        # Get the current emotional state of the pet
        state = self.get_emotional_state()
        # If the state is sad, increment the sad streak counter
        if state == "sad":
            self.sad_streak += 1
        # Otherwise, reset the sad streak to 0
        else:
            self.sad_streak = 0

    # Method to detect if the pet has reached a loss condition
    def detectLoss(self, trigger_ui: Optional[bool] = None) -> bool:
        """
        Returns True if the pet has reached a loss condition.
        When trigger_ui is True (used by the terminal UI), it will call the UI game over screen if available.
        """
        # Use the instance variable if trigger_ui is not explicitly provided
        if trigger_ui is None:
            trigger_ui = self.use_terminal_ui
        # Initialize an empty reason string
        reason = ""
        # If health reaches 0 or below, set the loss reason
        if self.health <= 0:
            reason = "Health collapsed."
        # If hunger drops to 5 or below, set the loss reason
        elif self.hunger <= 5:
            reason = "Hunger fell too low."
        # If energy drops to 5 or below, set the loss reason
        elif self.energy <= 5:
            reason = "Energy fell too low."
        # If happiness reaches 0, set the loss reason
        elif self.happiness <= 0:
            reason = "Happiness hit zero."
        # If cleanliness reaches 0, set the loss reason
        elif self.cleanliness <= 0:
            reason = "Cleanliness hit zero."
        # If sad streak reaches 3 or more days, set the loss reason
        elif self.sad_streak >= 3:
            reason = "Stayed sad for too long."

        # Store the death reason in the instance variable
        self.last_death_reason = reason

        # If no loss condition was triggered, return False
        if not reason:
            return False

        # If UI triggering is enabled and the game_over_screen function exists, call it
        if trigger_ui and hasattr(ui, "game_over_screen"):
            ui.game_over_screen(self.name)
        # Return True to indicate a loss condition was detected
        return True
