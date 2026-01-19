# Import random module for generating random price movements and events
import random
# Import defaultdict to create dictionaries with default integer values
from collections import defaultdict
# Import type hints for dictionary and tuple types
from typing import Dict, Tuple

# Import the Economy class to manage balance updates
from economy import Economy

# Define the StockMarket class for simulating stock price changes and trading
class StockMarket:
    """
    Lightweight stock market simulator for the GUI economy tab.
    Prices move a bit each tick; buy/sell adjusts the shared Economy balance.
    Includes occasional crashes and surges to keep risk meaningful.
    """

    # Constructor that initializes the stock market with an economy object and optional seed
    def __init__(self, economy: Economy, seed: int = None):
        # Store a reference to the shared Economy object
        self.economy = economy
        # Initialize price dictionary with four stock symbols and their starting prices
        self.prices: Dict[str, float] = {
            "PAW": 50.0,
            "MEOW": 35.0,
            "BONE": 20.0,
            "NUT": 15.0,
        }
        # Initialize price history as a dict mapping each symbol to a list of (day, price) tuples
        self.history = {symbol: [(0, price)] for symbol, price in self.prices.items()}
        # Initialize holdings as a defaultdict tracking shares owned of each symbol
        self.holdings = defaultdict(int)
        # Initialize holdings_cost to track total cost basis for each symbol
        self.holdings_cost = defaultdict(float)
        # Initialize realized_profit to track profit from completed stock sales
        self.realized_profit = 0.0
        # Initialize day counter starting at 0
        self.day = 0
        # Initialize momentum dict for each symbol to influence price direction
        self.momentum: Dict[str, float] = {symbol: random.uniform(-0.02, 0.03) for symbol in self.prices}
        # Set the random seed if provided for reproducible results
        if seed is not None:
            random.seed(seed)

    # Method to advance the market one day and adjust all stock prices
    def tick(self) -> Dict[str, float]:
        """Advance market one step and slightly move prices."""
        # Increment the day counter
        self.day += 1
        # Loop through each stock symbol and its current price
        for symbol, price in self.prices.items():
            # Generate a random swing between -0.1 and 0.1 for natural variation
            swing = random.uniform(-0.1, 0.1)  # wider range to allow dips
            # Add the symbol's momentum to the swing
            swing += self.momentum.get(symbol, 0.0)

            # 7% chance for a market surge (positive price movement)
            if random.random() < 0.07:
                # Add a large positive swing between 0.15 and 0.4
                swing += random.uniform(0.15, 0.4)

            # 4% chance for a market crash (negative price movement)
            if random.random() < 0.04:
                # Set crash factor between 0.2 and 0.7 (multiply current price)
                crash_factor = random.uniform(0.2, 0.7)
                # Apply the crash factor and ensure price doesn't go below 0.5
                price = max(0.75, price * crash_factor)
                # Set momentum negative after crash to simulate prolonged downturn
                self.momentum[symbol] = random.uniform(-0.05, -0.01)

            # Calculate new price using the swing percentage
            new_price = max(0.5, round(price * (1 + swing), 2))
            # Slowly mean-revert momentum to prevent unlimited growth or decline
            self.momentum[symbol] = max(-0.1, min(0.08, self.momentum.get(symbol, 0.0) * 0.9 + random.uniform(-0.01, 0.02)))
            # Update the price for this symbol
            self.prices[symbol] = new_price
            # Append the new price and day to the history
            self.history.setdefault(symbol, []).append((self.day, new_price))
        # Return the updated prices dictionary
        return self.prices
        
    # Method to buy shares of a stock, spending from the economy balance
    def buy(self, symbol: str, shares: int) -> Tuple[bool, str]:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()
        # Validate that the share count is positive
        if shares <= 0:
            # Return failure with an error message
            return False, "Enter a positive share count."
        # Get the current price of the symbol
        price = self.prices.get(symbol)
        # Check if the symbol exists in the market
        if price is None:
            # Return failure if the symbol is unknown
            return False, "Unknown symbol."

        # Calculate the total cost of the purchase
        cost = int(round(price * shares))
        # Attempt to spend the cost from the economy
        if not self.economy.spend("investments", cost):
            # Return failure if there's insufficient balance
            return False, "Not enough balance."

        # Increase the holdings of this symbol by the purchased shares
        self.holdings[symbol] += shares
        # Add the cost basis to track average purchase price
        self.holdings_cost[symbol] += price * shares
        # Return success with a confirmation message
        return True, f"Bought {shares} {symbol} for ${cost}"

    # Method to sell shares of a stock, earning money back to the economy
    def sell(self, symbol: str, shares: int) -> Tuple[bool, str]:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()
        # Validate that the share count is positive
        if shares <= 0:
            # Return failure if share count is not positive
            return False, "Enter a positive share count."
        # Get the current holdings for this symbol
        owned = self.holdings.get(symbol, 0)
        # Check if we have enough shares to sell
        if shares > owned:
            # Return failure if trying to sell more shares than owned
            return False, "Not enough shares to sell."

        # Get the current market price of the symbol
        price = self.prices.get(symbol)
        # Check if the symbol exists in the market
        if price is None:
            # Return failure if the symbol is unknown
            return False, "Unknown symbol."

        # Calculate the average cost per share for this symbol
        avg_cost = self.average_cost(symbol)
        # Calculate the cost basis for the shares being sold
        cost_basis = avg_cost * shares
        # Calculate the proceeds from selling at current market price
        proceeds = int(round(price * shares))
        # Decrease holdings for this symbol
        self.holdings[symbol] -= shares
        # Decrease the cost basis tracking accordingly
        self.holdings_cost[symbol] = max(0.0, self.holdings_cost[symbol] - cost_basis)
        # Add profit/loss to realized profit (proceeds minus cost basis)
        self.realized_profit += proceeds - cost_basis
        # Add the proceeds back to the economy balance
        self.economy.earn(proceeds)
        # Return success with a confirmation message
        return True, f"Sold {shares} {symbol} for ${proceeds}"

    # Method to calculate the total current value of all holdings
    def portfolio_value(self) -> float:
        # Sum the market value of all holdings (shares * current price)
        return round(sum(self.prices[symbol] * shares for symbol, shares in self.holdings.items()), 2)

    # Method to calculate the average purchase price per share for a symbol
    def average_cost(self, symbol: str) -> float:
        # Get the number of shares held for this symbol
        shares = self.holdings.get(symbol, 0)
        # If no shares are held, return 0
        if shares <= 0:
            return 0.0
        # Return total cost basis divided by shares (average cost per share)
        return self.holdings_cost.get(symbol, 0.0) / shares

    # Method to calculate unrealized profit/loss on current holdings
    def unrealized_profit(self) -> float:
        # Initialize total unrealized profit to 0
        total = 0.0
        # Loop through each symbol and its share count
        for symbol, shares in self.holdings.items():
            # Skip symbols with no shares
            if shares <= 0:
                continue
            # Add the profit/loss: (current price - avg cost) * shares
            total += (self.prices.get(symbol, 0) - self.average_cost(symbol)) * shares
        # Return the total unrealized profit rounded to 2 decimal places
        return round(total, 2)

    # Method to calculate total profit (realized + unrealized)
    def total_profit(self) -> float:
        # Return the sum of realized and unrealized profit
        return round(self.realized_profit + self.unrealized_profit(), 2)

    # Method to retrieve the complete price history for all symbols
    def price_history(self) -> Dict[str, list]:
        # Return the history dictionary mapping symbols to lists of (day, price) tuples
        return self.history

    # Method to format current holdings as text lines with profit/loss information
    def holdings_lines(self):
        # Initialize an empty list to store formatted holding lines
        lines = []
        # Loop through each symbol and share count, sorted by symbol
        for symbol, shares in sorted(self.holdings.items()):
            # Calculate the market value of this holding
            value = self.prices.get(symbol, 0) * shares
            # Get the average purchase price for this symbol
            avg = self.average_cost(symbol)
            # Calculate unrealized profit/loss for this holding
            unreal = (self.prices.get(symbol, 0) - avg) * shares
            # Only include holdings with shares
            if shares > 0:
                lines.append((f"{symbol:<4} {shares:>4} sh @ ${avg:>6.2f}  (${value:>7.2f})  P/L ${unreal:>7.2f}", unreal))
        if not lines:
            lines.append(("No holdings yet.", 0.0))
        return lines
