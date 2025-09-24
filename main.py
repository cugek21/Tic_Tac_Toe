"""
Main module for the Tic-Tac-Toe game.

This module contains the main game logic and entry points for both
single-player and multiplayer modes. It handles game initialization,
player input, and game flow control.

The game supports boards from 3x3 to 9x9 and includes various
difficulty levels for the AI opponent in single-player mode.
"""

import sys
from src.game_functions import (
    create_board, print_board, get_player_move,
    check_winner, get_computer_move, ask_to_continue,
    INTRODUCTION, DIVIDER, CENTER_WIDTH, TO_WIN
)
from src.tictactoe_adapter import TicTacToeAdapter


def check_python_version(required=(3, 10)):
    """
    Raises an error if the Python version is below the required.
    
    Args:
        required (tuple): Required Python version as (major, minor).

    Raises:
        RuntimeError: If current version is lower than required.
    """
    current = sys.version_info
    if current[:2] < required:
        raise RuntimeError(
        f'Requires Python {required[0]}.{required[1]}+, '
        f'but found {current.major}.{current.minor}'
        )


def singleplayer(size: int, depth: int) -> None:
    """
    The function handles the game loop for single player mode.
    
    Args:
        size: The size of the game board (size x size)
        depth: The depth of the minimax search tree (difficulty)
              0 = random moves
              size*size = perfect play
    """
    board = create_board(size)
    human, computer = 'X', 'O'

    if size <= 3:
        depth = size*size
    elif size <= 5:
        depth = 4
    elif size <= 7:
        depth = 3
    else:
        depth = 2
    ai = TicTacToeAdapter(size, TO_WIN, human, computer)

    for turn in range(size * size):
        print_board(board, size)
        if turn % 2 == 0:
            idx = get_player_move(board, human, size)
            board[idx] = human
            if check_winner(board, human, size, TO_WIN):
                print_board(board, size)
                print('🎉 You win! 🎉')
                return
        else:
            if depth == 0:
                idx = get_computer_move(board)
            else:
                print('Let me think... please wait.')
                idx = ai.best_move(board, depth)
                if idx is None:
                    idx = get_computer_move(board)
            board[idx] = ai.computer
            print(f'AI selected {idx + 1}')
            if check_winner(board, computer, size, TO_WIN):
                print_board(board, size)
                print('🎉 AI wins! 🎉')
                return
    print_board(board, size)
    print('It\'s a draw!')


def multiplayer(size: int) -> None:
    """
    The function handles the game loop for two-player mode.
    
    Args:
        size: The size of the game board (size x size)
    """
    board = create_board(size)
    current_player = 'X'

    for _ in range(size * size):
        print_board(board, size)
        idx = get_player_move(board, current_player, size)
        board[idx] = current_player
        if check_winner(board, current_player, size, TO_WIN):
            print_board(board, size)
            print(f'🎉 Player {current_player} wins! 🎉')
            return
        current_player = 'O' if current_player == 'X' else 'X'
    print_board(board, size)
    print('It\'s a draw!')


def play_game() -> None:
    """
    Main game loop that handles game setup and replay functionality.
    
    This function:
    1. Shows the introduction and game options
    2. Gets user input for:
       - Game mode (single/multiplayer)
       - Difficulty level (in single player mode)
       - Board size (3x3 to 9x9)
    3. Runs the selected game mode
    4. Offers to play another game
    """
    first_game = True
    while True:
        if first_game:
            print(INTRODUCTION)
        else:
            print(f'\n{DIVIDER}')
        while True:
            mode = input('\nSelect 1 or 2: ').strip()
            if mode not in ('1', '2'):
                print('Probably typo. Try again.')
            else:
                break

        if mode == '1':
            print(
                f'\n'
                f"{'Select difficulty:'.center(CENTER_WIDTH)}\n"
                f'1. Easy\n'
                f'2. Medium\n'
                f'3. Hard\n'
                f'4. Impossible'
            )
            while True:
                difficulty = input('\nSelect 1 - 4: ').strip()
                if difficulty not in ('1', '2', '3', '4'):
                    print('Probably typo. Try again.')
                else:
                    break

        while True:
            size_input = input(
                '\nSelect board size (min. 3, max. 9 for 9x9 board): '
            ).strip()
            if size_input.isdigit() and int(size_input) in range(3,10):
                size = int(size_input)
                break
            print('Size must be between 3 and 9.')

        if mode == '1':
            if difficulty == '1':
                depth = 0
            elif difficulty == '2':
                depth = int((size * size) * 0.4)
            elif difficulty == '3':
                depth = int((size * size) * 0.8)
            else:
                depth = size * size
            singleplayer(size, depth)
        else:
            multiplayer(size)
        if not ask_to_continue():
            break


if __name__ == '__main__':
    check_python_version((3,10))
    play_game()
