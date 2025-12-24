# Pet.py
import uiTermVer as ui
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


@dataclass
class petStats:
    type: str
    hunger: int = 100
    happiness: int = 100
    health: int = 100
    energy: int = 100
    cleanliness: int = 100
class Pet:
    def __init__(self, name: str, pet_type: Union[petStats, str], age_days: int = 0, use_terminal_ui: bool = True):
        self.name = name

        # Accept either a predefined petStats profile or a simple species string (GUI uses strings)
        if isinstance(pet_type, petStats):
            self.pet_profile = pet_type
        else:
            self.pet_profile = petStats(pet_type.lower())

        # Keep compatibility with existing code paths that expect pet_type to expose stat caps
        self.pet_type = self.pet_profile
        self.species = self.pet_profile.type

        self.hunger = 1 * self.pet_profile.hunger
        self.happiness = 1 * self.pet_profile.happiness
        self.health = 1 * self.pet_profile.health
        self.energy = 1 * self.pet_profile.energy
        self.cleanliness = 1 * self.pet_profile.cleanliness
        self.age_days = age_days
        self.sad_streak = 0
        self.last_death_reason = ""
        self.use_terminal_ui = use_terminal_ui
        
    def clamp_stats(self):
        max_stats = self.pet_profile
        self.hunger = max(0, min(1 * max_stats.hunger, self.hunger))
        self.happiness = max(0, min(1 * max_stats.happiness, self.happiness))
        self.health = max(0, min(1 * max_stats.health, self.health))
        self.energy = max(0, min(1 * max_stats.energy, self.energy))
        self.cleanliness = max(0, min(1 * max_stats.cleanliness, self.cleanliness))
        self.age_days = max(0, self.age_days)
        
    def pass_time(self, days=1):
        for _ in range(days):
            self.age_days += 1
            self.hunger -= 5
            self.happiness -= 3
            self.energy -= 4
            self.cleanliness -= 3
            
            if self.hunger < 20 or self.cleanliness < 20:
                self.health -= 5
            self.clamp_stats()
            self._update_sad_streak()
            if self.detectLoss(trigger_ui=self.use_terminal_ui):
                break
                
            
    def get_emotional_state(self):
        if self.health < 30:
            return "sick"
        if self.hunger < 30:
            return "hungry"
        if self.energy < 30:
            return "tired"
        if self.cleanliness < 30:
            return "dirty"
        if self.happiness < 30:
            return "sad"
        if self.happiness > 70:
            return "happy"
        return "neutral"
            
    def sleep(self, duration):
        self.energy += duration * 10
        self.hunger -= duration * 2
        self.energy = min(100, self.energy + duration * 10)
        self.clamp_stats()
        self._update_sad_streak()

    def feed(self, amount):
        self.hunger += amount
        self.health += amount // 5
        self.clamp_stats()
        self._update_sad_streak()

    def shower(self, amount):
        self.happiness -= amount *2
        self.cleanliness += amount * 4
        self.clamp_stats()
        self._update_sad_streak()

    def play(self, duration):
        self.happiness += duration * 5
        self.energy -= duration * 3
        self.hunger -= duration * 2
        self.happiness = min(100, self.happiness + duration)
        self.clamp_stats()
        self._update_sad_streak()

    def _update_sad_streak(self):
        state = self.get_emotional_state()
        if state == "sad":
            self.sad_streak += 1
        else:
            self.sad_streak = 0

    def detectLoss(self, trigger_ui: Optional[bool] = None) -> bool:
        """
        Returns True if the pet has reached a loss condition.
        When trigger_ui is True (used by the terminal UI), it will call the UI game over screen if available.
        """
        if trigger_ui is None:
            trigger_ui = self.use_terminal_ui
        reason = ""
        if self.health <= 0:
            reason = "Health collapsed."
        elif self.hunger <= 5:
            reason = "Hunger fell too low."
        elif self.energy <= 5:
            reason = "Energy fell too low."
        elif self.happiness <= 0:
            reason = "Happiness hit zero."
        elif self.cleanliness <= 0:
            reason = "Cleanliness hit zero."
        elif self.sad_streak >= 3:
            reason = "Stayed sad for too long."

        self.last_death_reason = reason

        if not reason:
            return False

        if trigger_ui and hasattr(ui, "game_over_screen"):
            ui.game_over_screen(self.name)
        return True
