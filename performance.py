import json
from game_state import GameState, simulate
from move_generator import get_legal_moves
from logger import Logger
import alpha_beta as ab_module
from alpha_beta import alpha_beta
from benchmark import load_benchmark

MAX_TURNS = 500

def compute_pruning_ratio(nodes_expanded, moves_count, depth):
    if depth == 0 or moves_count == 0:
        return 0.0
    max_nodes = moves_count ** depth
    if max_nodes == 0:
        return 0.0
    pruned = max(0, max_nodes - nodes_expanded)
    return round(pruned / max_nodes, 4)

def find_benchmark_entry(benchmark, game_num, turn):
    for entry in benchmark:
        if entry['game'] == game_num and entry['turn'] == turn:
            return entry
    return None

def run_measured_game(depth, heuristic_fn, h_name,
                      logger, game_num, benchmark):
    state    = GameState()
    turn     = 0

    while turn < MAX_TURNS:
        moves = get_legal_moves(state)
        if not moves:
            break

        # Reset node counter before each move
        ab_module.nodes_expanded = 0

        import time
        t0     = time.time()
        _, mv  = alpha_beta(state, depth,
                            float('-inf'), float('inf'),
                            True, state.active, heuristic_fn)
        elapsed = time.time() - t0

        if mv is None:
            break

        nodes         = ab_module.nodes_expanded
        pruning_ratio = compute_pruning_ratio(
            nodes, len(moves), depth
        )

        # Look up benchmark entry for this state if available
        bench_entry   = find_benchmark_entry(benchmark, game_num, turn)
        optimal_move  = bench_entry['optimal_move']  if bench_entry else None
        optimal_score = bench_entry['optimal_score'] if bench_entry else None

        logger.log_move(
            state, mv, nodes, elapsed,
            optimal_move=optimal_move,
            optimal_score=optimal_score,
            pruning_ratio=pruning_ratio
        )
        state.apply_move(mv)
        turn += 1

    logger.log_result(state)