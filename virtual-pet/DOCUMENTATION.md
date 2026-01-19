# Virtual Pet Simulator Documentation

## Overview
This project is a real-time virtual pet game built with Python and Tkinter.
You name a pet, keep its stats healthy, and manage a simple in-game economy
with a lightweight stock market.

## Features
- Real-time pet care loop (stats change automatically over time)
- Feeding, playing, sleeping, and bathing actions
- Economy system with spending categories
- Stock market simulator with buy/sell and charts
- PNG-based pet skins by mood and species

## Requirements
- Python 3.x
- Tkinter (included with most Python installs on Windows)

## Project Structure
- `virtual-pet/src/ui_gui.py` - Main GUI application
- `virtual-pet/src/pet.py` - Pet model and stat logic
- `virtual-pet/src/economy.py` - Money and spending logic
- `virtual-pet/src/stock_market.py` - Market simulator
- `virtual-pet/assets/` - PNG skins and background music

## Running the Game
From the repository root:
```
python virtual-pet/src/ui_gui.py
```

## How to Play
- Name your pet and select a species.
- Use the Care tab to keep stats above zero.
- Time advances automatically; the market also updates automatically.
- Use the Economy tab to buy/sell shares and grow your balance.
- Watch the Charts tab for price history.

## Pet States and Skins
Pet images are loaded from `virtual-pet/assets` using this naming pattern:
```
<state>-<species>.png
```
Examples:
- `happy-dog.png`
- `hungry-cat.png`
- `neutral-guinea-pig.png`

Supported states:
- happy
- neutral
- hungry
- tired
- dirty
- sick
- sad

Supported species:
- dog
- cat
- guinea pig

## Controls
- Feed: costs $10, reduces hunger
- Play: costs $5, increases happiness
- Sleep: restores energy
- Bathe/Shower: costs $8, improves cleanliness

## Notes
- If any stat reaches zero (or sadness persists), the game ends.
- Market prices fluctuate on each time tick.

