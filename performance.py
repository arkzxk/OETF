import time
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
    AVG_BRANCH = 8
    if depth == 1:
        theoretical = moves_count
    else:
        theoretical = moves_count * (AVG_BRANCH ** (depth - 1))
    if theoretical == 0:
        return 0.0
    pruned = max(0, theoretical - nodes_expanded)
    return round(min(pruned / theoretical, 1.0), 4)

def find_benchmark_entry(benchmark, game_num, turn):
    for entry in benchmark:
        if entry['game'] == game_num and entry['turn'] == turn:
            return entry
    return None

def run_measured_game(depth, heuristic_fn, h_name, logger, game_num, benchmark):
    state = GameState()
    turn  = 0

    while turn < MAX_TURNS:
        moves = get_legal_moves(state)
        if not moves:
            break

        ab_module.nodes_expanded = 0

        t0    = time.time()
        _, mv = alpha_beta(state, depth, float('-inf'), float('inf'), True, state.active, heuristic_fn)
        elapsed = time.time() - t0

        if mv is None:
            break

        nodes         = ab_module.nodes_expanded
        pruning_ratio = compute_pruning_ratio(nodes, len(moves), depth)

        bench_entry   = find_benchmark_entry(benchmark, game_num, turn)
        optimal_move  = bench_entry['optimal_move']  if bench_entry else None
        optimal_score = bench_entry['optimal_score'] if bench_entry else None

        logger.log_move(
            state, mv, nodes, elapsed,
            optimal_move=optimal_move,
            optimal_score=optimal_score,
            pruning_ratio=pruning_ratio,
            all_moves=moves
        )
        state.apply_move(mv)
        turn += 1

    logger.log_result(state)