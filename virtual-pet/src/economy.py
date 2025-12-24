# Economy.py
from collections import defaultdict
import uiTermVer as ui

class Economy:
    def __init__(self, starting_balance=1000):
        self.balance = starting_balance
        self.expenses = defaultdict(int)
        # initialize predefined categories if you want
        for category in ["food", "clothing", "entertainment", "toys", "vet", "other"]:
            self.expenses[category] = 0


    def spend(self, category: str, amount: int) -> bool:
        if category in self.expenses and amount <= self.balance:
            self.expenses[category] += amount
            self.balance -= amount
            return True
        print(f"Cannot spend {amount} on {category}. Current balance: {self.balance}")
        return False

        
    def earn(self, amount:int):
        if amount > 0:
            self.balance += amount
        else:
            print("Earning amount must be positive.")
            
    def get_balance(self):
        return self.balance
    
    def get_expenses(self):
        return self.expenses
    
    def report(self):
        print(f"Current Balance: {self.balance}")
        print("Expenses Breakdown:")
        for category, amount in self.expenses.items():
            print(f"  {category}: {amount}")
