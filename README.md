# Tic-Tac-Toe

A customizable Tic-Tac-Toe game implemented in Python.
Supports single-player (with AI) and two-player modes, variable board sizes,
and multiple AI difficulty levels.

## Features
- Play against the computer or another player
- Board sizes from 3x3 up to 9x9
- AI opponent with adjustable difficulty (easy, medium, hard, impossible)
- Colored terminal output for better visibility
- Replay option after each game

## Project Structure
```
Tic_Tac_Toe/
├── main.py                # Main entry point and game loop
├── src/
│   ├── game_functions.py  # Core game logic and UI functions
│   ├── minimax_lib.py     # Generic minimax algorithm for AI
│   ├── tictactoe_adapter.py # Adapter for using minimax with Tic-Tac-Toe
│   └── __init__.py        # Package marker
└── README.md              # Project documentation
```

## How to Run
1. Make sure you have Python 3.10+ installed.
2. Run the game from the terminal:
   ```sh
   python main.py
   ```
3. Follow the prompts to select game mode, difficulty, and board size.

## How the AI Works
- The AI uses the minimax algorithm for decision making.
- Difficulty levels control the search depth:
  - Easy: random moves
  - Medium/Hard: limited lookahead
  - Impossible: perfect play

## Author
Radek Jíša
