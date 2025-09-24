"""
Core game functions for the Tic-Tac-Toe game.

This module provides the basic game mechanics:
- Board creation and display
- Move validation and execution
- Win condition checking
- Player input handling

Supports customizable board sizes and win conditions, with colored
output for better visual distinction between players.

Constants:
    CENTER_WIDTH: Width for centering text output
    DIVIDER: Horizontal line for UI separation
    TO_WIN: Number of marks in a row needed to win
    INTRODUCTION: Welcome message and game mode selection text
    BOLD, RED, GREEN, RESET: ANSI color codes for terminal output
"""

import random

CENTER_WIDTH = 60
DIVIDER = '=' * CENTER_WIDTH
TO_WIN = 3
INTRODUCTION = (
    f'{DIVIDER}\n\n'
    f'{'TIC-TAC-TOE'.center(CENTER_WIDTH)}\n\n'
    f'{DIVIDER}\n\n'
    f'{'You win by lining up THREE of your marks.'.center(CENTER_WIDTH)}\n\n'
    f'{'Select mode:'.center(CENTER_WIDTH)}\n'
    f'1. Play against computer\n'
    f'2. Two players'
)
BOLD  = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def create_board(size: int) -> list[str]:
    """
    Create a new square board numbered from 1 to size*size.
    
    Args:
        size: The width/height of the board (size x size)
    
    Returns:
        List of strings representing board cells, numbered sequentially
        from 1 to size*size. Empty cells contain their position number.
    
    Example:
        >>> create_board(3)
        ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    """
    return [str(i + 1) for i in range(size * size)]


def print_board(board: list[str], size: int) -> None:
    """
    Print the Tic-Tac-Toe board with colored markers and grid.
    
    Args:
        board: List of strings representing the board state
        size: The width/height of the board (size x size)
    
    The function prints:
    - A grid with '+' and '-' for borders
    - Cell numbers or player marks ('X' in red, 'O' in green)
    - Proper spacing and alignment for all board sizes
    
    Example output for 3x3:
        +----+----+----+
        |  1 |  2 |  3 |
        +----+----+----+
        |  4 |  X |  6 |
        +----+----+----+
        |  7 |  8 |  O |
        +----+----+----+
    """
    print('\n')
    for row in range(0, size * size, size):
        row_cells = []
        for col in range(size):
            raw = board[row + col]
            cell = raw.rjust(2)
            if raw == 'X':
                cell = f'{BOLD}{RED}{cell}{RESET}'
            elif raw == 'O':
                cell = f'{BOLD}{GREEN}{cell}{RESET}'
            row_cells.append(cell)
        row_str = ' | '.join(row_cells)
        print('+----' * (size - 1) + '+----+')
        print(f'| {row_str} |')
        if row == size * (size - 1):
            print('+----' * (size - 1) + '+----+')
    print('\n')


def check_winner(board: list[str], player: str, size: int, to_win: int = 3
) -> bool:
    """
    Check if the specified player has won the game.
    
    Args:
        board: List of strings representing the board state
        player: The player mark to check for ('X' or 'O')
        size: The width/height of the board (size x size)
        to_win: Number of marks needed in a row to win (default: 3)
    
    Returns:
        True if the player has won, False otherwise
    """
    # Rows
    for r in range(size):
        for c in range(size - to_win + 1):
            if all(
                board[r * size + c + k] == player for k in range(to_win)
            ):
                return True
    # Columns
    for c in range(size):
        for r in range(size - to_win + 1):
            if all(
                board[(r + k) * size + c] == player for k in range(to_win)
            ):
                return True
    # Diagonals (\)
    for r in range(size - to_win + 1):
        for c in range(size - to_win + 1):
            if all(
                board[(r + k) * size + (c + k)] == player
                for k in range(to_win)
            ):
                return True
    # Anti-diagonals (/)
    for r in range(size - to_win + 1):
        for c in range(to_win - 1, size):
            if all(
                board[(r + k) * size + (c - k)] == player
                for k in range(to_win)
            ):
                return True
    return False


def get_player_move(board: list[str], player: str, size: int) -> int:
    """
    Get and validate a move from the player.
    
    Args:
        board: List of strings representing the board state
        player: The current player's mark ('X' or 'O')
        size: The width/height of the board (size x size)
    
    Returns:
        The validated index (0-based) where the player wants to move
    """
    max_num = size * size
    while True:
        move = input(
            f'It\'s your turn, player {player}! Select 1 - {max_num}: '
        )
        if not move.isdigit() or int(move) not in range(1, max_num + 1):
            print('Probably typo. Try again.')
            continue
        idx = int(move) - 1
        if board[idx] in ('X', 'O'):
            print('Spot already taken. Try again.')
            continue
        return idx


def get_computer_move(board: list[str]) -> int:
    """
    Get a random valid move for the computer player.
    
    Args:
        board: List of strings representing the board state
    
    Returns:
        A randomly chosen valid move index (0-based)
    """
    free_spots = [i for i, v in enumerate(board) if v not in ('X', 'O')]
    return random.choice(free_spots)


def ask_to_continue() -> bool:
    """
    Prompt the user to play another round.
    
    Continuously prompts until a valid 'y' or 'n' response is received.
    Input is case-insensitive and whitespace is stripped.
    
    Returns:
        bool: True if player wants to continue, False otherwise
    """
    while True:
        answer = input(
            f'\n{'Play again? (y/n):'.center(CENTER_WIDTH)}\n{' ':>29}'
        ).strip().lower()
        if answer in ('y', 'n'):
            return answer == 'y'
        print('\nPlease enter y or n: ')
