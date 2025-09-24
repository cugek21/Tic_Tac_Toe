"""
Generic implementation of the Minimax algorithm for game AI.
Provides algorithm that can be used with two-player,
zero-sum game with perfect information.

Evaluates all possible moves to a certain depth and chooses the move
that leads to the best possible outcome.
"""

from typing import Any, Callable


def minimax(
    state: Any,
    depth: int,
    maximizing_player: bool,
    get_moves: Callable[[Any, bool], list[Any]],
    apply_move: Callable[[Any, Any, bool], Any],
    evaluate: Callable[[Any], int],
    is_terminal: Callable[[Any], bool]
) -> tuple[float, Any | None]:
    """
    Execute the minimax algorithm to find the best move in game state.
    
    Args:
        state: The current game state
        depth: How many moves ahead to look
        maximizing_player: True if it's maximizing player's turn
        get_moves: Returns list of possible moves
        apply_move: Returns new state after applying a move
        evaluate: Returns numeric score for a state
        is_terminal: Checks if state is terminal
    
    Returns:
        tuple[float, Any | None]: A tuple containing:
            - The best score achievable from this state
            - The move that achieves this score
    """

    if depth == 0 or is_terminal(state):
        return evaluate(state), None

    if maximizing_player:
        best_score = float("-inf")
        best_move = None
        for move in get_moves(state, True):
            # pass maximizing_player to apply_move
            new_state = apply_move(state, move, True)
            score, _ = minimax(
                new_state, depth - 1, False,
                get_moves, apply_move, evaluate, is_terminal
            )
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    else:  # minimizing player
        best_score = float("inf")
        best_move = None
        for move in get_moves(state, False):
            # pass maximizing_player to apply_move
            new_state = apply_move(state, move, False)
            score, _ = minimax(
                new_state, depth - 1, True,
                get_moves, apply_move, evaluate, is_terminal
            )
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move
