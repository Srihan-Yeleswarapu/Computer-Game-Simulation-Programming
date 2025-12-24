# Pet.py
import ui

class Pet:
    def __init__(self, name:str, pet_type:str, age_days:int=0):
        self.name = name
        
        
        self.pet_type = pet_type
        self.hunger = 100
        self.happiness = 100
        self.health = 100
        self.energy = 100
        self.cleanliness = 100
        self.age_days = age_days
        
    def clamp_stats(self):
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.health = max(0, min(100, self.health))
        self.energy = max(0, min(100, self.energy))
        self.cleanliness = max(0, min(100, self.cleanliness))
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
            self.detectLoss()
            
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
        self.hunger = max(0, self.hunger - amount)
        self.clamp_stats()

    def play(self, duration):
        self.happiness += duration * 5
        self.energy -= duration * 3
        self.hunger -= duration * 2
        self.happiness = min(100, self.happiness + duration)
        self.clamp_stats()

    def detectLoss(self):
        if self.health <= 0 or self.energy <= 0:
            return True
        return False
