# Economy.py
# Import the defaultdict class from collections module to create a dictionary with default integer values
from collections import defaultdict
# Import the ui module for terminal-based user interface functions
import uiTermVer as ui

# Define the Economy class to manage money and spending in the virtual pet game
class Economy:
    # Constructor that initializes the Economy with an optional starting balance (default 1000)
    def __init__(self, starting_balance=1000):
        # Set the initial balance to the provided starting amount
        self.balance = starting_balance
        # Create a defaultdict that automatically initializes missing keys with 0
        self.expenses = defaultdict(int)
        # Initialize predefined expense categories with 0 values
        for category in ["food", "clothing", "entertainment", "toys", "vet", "grooming", "investments", "other"]:
            # Set each category's initial expense to 0
            self.expenses[category] = 0

    # Method to spend money on a specific category if sufficient balance exists
    def spend(self, category: str, amount: int) -> bool:
        # Check if the category exists in expenses AND if the amount is within the current balance
        if category in self.expenses and amount <= self.balance:
            # Add the amount to the category's total spending
            self.expenses[category] += amount
            # Subtract the amount from the overall balance
            self.balance -= amount
            # Return True to indicate the spending was successful
            return True
        # Print an error message if the spending failed
        print(f"Cannot spend {amount} on {category}. Current balance: {self.balance}")
        # Return False to indicate the spending was unsuccessful
        return False

    # Method to add money to the balance from earnings
    def earn(self, amount:int):
        # Check if the earned amount is positive
        if amount > 0:
            # Add the earned amount to the current balance
            self.balance += amount
        # If the amount is not positive, display an error message
        else:
            print("Earning amount must be positive.")
            
    # Method to retrieve the current balance
    def get_balance(self):
        # Return the current balance value
        return self.balance
    
    # Method to retrieve all recorded expenses
    def get_expenses(self):
        # Return the entire expenses dictionary
        return self.expenses
    
    # Method to print a detailed report of balance and expenses
    def report(self):
        # Print the current balance
        print(f"Current Balance: {self.balance}")
        # Print a header for the expenses breakdown section
        print("Expenses Breakdown:")
        # Loop through each category and its spending amount
        for category, amount in self.expenses.items():
            # Print each category with its total spending, indented for readability
            print(f"  {category}: {amount}")
