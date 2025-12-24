# Pet.py
import ui
from dataclasses import dataclass
from enum import Enum


@dataclass
class petStats:
    type: str
    hunger: int = 100
    happiness: int = 100
    health: int = 100
    energy: int = 100
    cleanliness: int = 100
class Pet:
    def __init__(self, name:str, pet_type:petStats, age_days:int=0):
        self.name = name
        
        
        self.pet_type = pet_type
        self.hunger = 1 * pet_type.hunger
        self.happiness = 1 * pet_type.happiness
        self.health = 1 * pet_type.health
        self.energy = 1 * pet_type.energy
        self.cleanliness = 1 * pet_type.cleanliness
        self.age_days = age_days
        
    def clamp_stats(self):
        self.hunger = max(0, min(1 * self.pet_type.hunger, self.hunger))
        self.happiness = max(0, min(1 * self.pet_type.happiness, self.happiness))
        self.health = max(0, min(1 * self.pet_type.health, self.health))
        self.energy = max(0, min(1 * self.pet_type.energy, self.energy))
        self.cleanliness = max(0, min(1 * self.pet_type.cleanliness, self.cleanliness))
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
            if(self.detectLoss()):
                ui.game_over_screen(self.name)
                
            
    def get_emotional_state(self):
        if self.happiness > 70:
            return "happy"
        elif self.happiness > 40:
            return "neutral"
        elif self.health < 30:
            return "sick"
        elif self.hunger > 70:
            return "hungry"
        elif self.energy < 30:
            return "tired"
        elif self.cleanliness < 30:
            return "dirty"
        else:
            return "sad"
            
    def sleep(self, duration):
        self.energy += duration * 10
        self.hunger -= duration * 2
        self.energy = min(100, self.energy + duration * 10)
        self.clamp_stats()

    def feed(self, amount):
        self.hunger += amount
        self.health += amount // 5
        self.clamp_stats()

    def shower(self, amount):
        self.happiness -= amount *2
        self.cleanliness += amount * 4
        self.clamp_stats()

    def play(self, duration):
        self.happiness += duration * 5
        self.energy -= duration * 3
        self.hunger -= duration * 2
        self.happiness = min(100, self.happiness + duration)
        self.clamp_stats()

    def detectLoss(self):
        if self.health <= 0 or self.energy <= 0 or self.happiness <= 0 or self.cleanliness<= 0:
            return True
        return False
