import random
from collections import defaultdict
from typing import Dict, Tuple

from economy import Economy


class StockMarket:
    """
    Lightweight stock market simulator for the GUI economy tab.
    Prices move a bit each tick; buy/sell adjusts the shared Economy balance.
    Includes occasional crashes and surges to keep risk meaningful.
    """

    def __init__(self, economy: Economy, seed: int = None):
        self.economy = economy
        self.prices: Dict[str, float] = {
            "PAW": 50.0,
            "MEOW": 35.0,
            "BONE": 20.0,
            "NUT": 15.0,
        }
        self.holdings = defaultdict(int)
        self.day = 0
        # Momentum lets symbols drift; crashes can push them into long slumps
        self.momentum: Dict[str, float] = {symbol: random.uniform(-0.02, 0.03) for symbol in self.prices}
        if seed is not None:
            random.seed(seed)

    def tick(self) -> Dict[str, float]:
        """Advance market one step and slightly move prices."""
        self.day += 1
        for symbol, price in self.prices.items():
            swing = random.uniform(-0.1, 0.1)  # wider range to allow dips
            swing += self.momentum.get(symbol, 0.0)

            # Occasional surge
            if random.random() < 0.06:
                swing += random.uniform(0.15, 0.4)

            # Occasional crash
            if random.random() < 0.05:
                crash_factor = random.uniform(0.2, 0.7)
                price = max(0.5, price * crash_factor)
                # Post-crash malaise: push momentum negative so some never recover
                self.momentum[symbol] = random.uniform(-0.08, -0.01)

            new_price = max(0.5, round(price * (1 + swing), 2))
            # Slowly mean-revert momentum so it doesn't explode upwards forever
            self.momentum[symbol] = max(-0.1, min(0.08, self.momentum.get(symbol, 0.0) * 0.9 + random.uniform(-0.01, 0.02)))
            self.prices[symbol] = new_price
        return self.prices

    def buy(self, symbol: str, shares: int) -> Tuple[bool, str]:
        symbol = symbol.upper()
        if shares <= 0:
            return False, "Enter a positive share count."
        price = self.prices.get(symbol)
        if price is None:
            return False, "Unknown symbol."

        cost = int(round(price * shares))
        if not self.economy.spend("investments", cost):
            return False, "Not enough balance."

        self.holdings[symbol] += shares
        return True, f"Bought {shares} {symbol} for ${cost}"

    def sell(self, symbol: str, shares: int) -> Tuple[bool, str]:
        symbol = symbol.upper()
        if shares <= 0:
            return False, "Enter a positive share count."
        owned = self.holdings.get(symbol, 0)
        if shares > owned:
            return False, "Not enough shares to sell."

        price = self.prices.get(symbol)
        if price is None:
            return False, "Unknown symbol."

        proceeds = int(round(price * shares))
        self.holdings[symbol] -= shares
        self.economy.earn(proceeds)
        return True, f"Sold {shares} {symbol} for ${proceeds}"

    def portfolio_value(self) -> float:
        return round(sum(self.prices[symbol] * shares for symbol, shares in self.holdings.items()), 2)

    def holdings_lines(self):
        lines = []
        for symbol, shares in sorted(self.holdings.items()):
            value = self.prices.get(symbol, 0) * shares
            lines.append(f"{symbol:<4} {shares:>4} sh @ ${self.prices.get(symbol, 0):>6.2f}  (${value:>7.2f})")
        if not lines:
            lines.append("No holdings yet.")
        return lines
