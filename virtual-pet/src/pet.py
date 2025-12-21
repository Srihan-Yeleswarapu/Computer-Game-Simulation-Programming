# Pet.py
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
            self.hunger += 5
            self.happiness -= 3
            self.health -= 2
            self.energy -= 4
            self.cleanliness -= 3
            self.clamp_stats()
            
    def get_emotional_state(self):
        if self.happiness > 70:
            return "happy"
        elif self.happiness > 40:
            return "neutral"
        else:
            return "sad"
            
    def sleep(self, duration):
        self.energy = min(100, self.energy + duration * 10)

    def feed(self, amount):
        self.hunger = max(0, self.hunger - amount)

    def play(self, duration):
        self.happiness = min(100, self.happiness + duration)