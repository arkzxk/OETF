import time
from move_generator import get_legal_moves
from alpha_beta import alpha_beta, nodes_expanded as _ne
import alpha_beta as ab_module

MAX_TURNS = 500  # FIX: guard against infinite no-capture games

def select_move(state, depth, heuristic):
    ab_module.nodes_expanded = 0
    t0   = time.time()
    _, mv = alpha_beta(state, depth, float('-inf'), float('inf'), True, state.active, heuristic)
    return mv, ab_module.nodes_expanded, time.time() - t0

def run_game(depth, heuristic_fn, logger):
    from game_state import GameState
    state = GameState()
    while state.turn < MAX_TURNS:
        moves = get_legal_moves(state)
        if not moves:
            break
        mv, nodes, t = select_move(state, depth, heuristic_fn)
        if mv is None:
            break
        logger.log_move(state, mv, nodes, t)
        state.apply_move(mv)
    logger.log_result(state)