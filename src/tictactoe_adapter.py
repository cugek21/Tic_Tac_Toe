"""
Adapter class to use the minimax algorithm with Tic-Tac-Toe.
This module implements the game-specific logic.
It handles:
- Move generation
- Move application
- Board evaluation
- Terminal state detection
"""

from src.minimax_lib import minimax
from src.game_functions import check_winner


class TicTacToeAdapter:
    def __init__(self, size: int, to_win: int, human='X', computer='O'):
        """
        Initialize the TicTacToeAdapter.
        
        Args:
            size: Size of the board (size x size)
            to_win: Number of marks in a row needed to win
            human: Symbol for human player (default: 'X')
            computer: Symbol for computer player (default: 'O')
        """
        self.size = size
        self.to_win = to_win
        self.human = human
        self.computer = computer

    def get_moves(self, state: list[str], maximizing: bool) -> list[int]:
        """
        Get all valid moves from the current state.
        
        Args:
            state: Current board state
            maximizing: Whether it's maximizing player's turn (unused)
        
        Returns:
            List of indices where a move can be made
        """
        return [
            i for i, v in enumerate(
                state
            ) if v not in (
                self.human, self.computer
            )
        ]

    def apply_move(
            self,
            state: list[str],
            move: int,
            maximizing: bool
    ) -> list[str]:
        """
        Apply a move to the game state.
        
        Args:
            state: Current board state
            move: Index where to place the mark
            maximizing: True if it's computer's turn
            
        Returns:
            New board state after applying the move
        """
        new_state = state.copy()
        new_state[move] = self.computer if maximizing else self.human
        return new_state

    def evaluate(self, state: list[str]) -> int:
        """
        Evaluate the board state from computer's perspective.
        
        Args:
            state: Current board state
            
        Returns:
            Score for the position:
            - +100 for computer win
            - -100 for human win
            - Otherwise, difference between computer's
                and human's potential wins
        """
        if check_winner(state, self.computer, self.size, self.to_win):
            return 100
        if check_winner(state, self.human, self.size, self.to_win):
            return -100
        score = 0
        lines = self.generate_lines()
        for line in lines:
            ai_count = sum(1 for i in line if state[i] == self.computer)
            human_count = sum(1 for i in line if state[i] == self.human)
            if human_count == 0 and ai_count > 0:
                score += ai_count
            elif ai_count == 0 and human_count > 0:
                score -= human_count
        return score

    def is_terminal(self, state: list[str]) -> bool:
        """
        Check if the game has ended.
        
        Args:
            state: Current board state
            
        Returns:
            True if either player has won or the board is full
        """
        return (
            check_winner(state, self.human, self.size, self.to_win)
            or check_winner(state, self.computer, self.size, self.to_win)
            or all(v in (self.human, self.computer) for v in state)
        )

    def best_move(self, board: list[str], depth: int) -> int | None:
        """
        Find the best move for the computer using minimax algorithm.
        
        Args:
            board: Current board state
            depth: How many moves ahead to look
            
        Returns:
            The index of the best move, or None if no moves are available
        """
        _, move = minimax(
            state=board,
            depth=depth,
            maximizing_player=True,
            get_moves=self.get_moves,
            apply_move=self.apply_move,
            evaluate=self.evaluate,
            is_terminal=self.is_terminal
        )
        return move

    def generate_lines(self) -> list[list[int]]:
        """
        Generate all possible winning lines on the board.
        
        Returns:
            List of lists, where each inner list contains indices that form
            a potential winning line (horizontal, vertical, or diagonal)
        """
        lines = []
        N = self.size
        K = self.to_win

        # Rows
        for r in range(N):
            for c in range(N - K + 1):
                lines.append([r*N + c + i for i in range(K)])
        # Columns
        for c in range(N):
            for r in range(N - K + 1):
                lines.append([(r+i)*N + c for i in range(K)])
        # Diagonals (\)
        for r in range(N - K + 1):
            for c in range(N - K + 1):
                lines.append([(r+i)*N + (c+i) for i in range(K)])
        # Anti-diagonals (/)
        for r in range(N - K + 1):
            for c in range(K - 1, N):
                lines.append([(r+i)*N + (c-i) for i in range(K)])
        return lines
