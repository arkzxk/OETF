from move_generator import get_legal_moves
from game_state import simulate

nodes_expanded = 0

def alpha_beta(state, depth, a, b, maximizing, player, heuristic):
    global nodes_expanded
    nodes_expanded += 1
    moves = get_legal_moves(state)
    if depth == 0 or not moves:
        return heuristic(state, player), None
    best_mv = None
    if maximizing:
        val = float('-inf')
        for mv in moves:
            sim  = simulate(state, mv)
            sc,_ = alpha_beta(sim, depth-1, a, b, False, player, heuristic)
            if sc > val:
                val, best_mv = sc, mv
            a = max(a, val)
            if b <= a:
                break
        return val, best_mv
    else:
        val = float('inf')
        for mv in moves:
            sim  = simulate(state, mv)
            sc,_ = alpha_beta(sim, depth-1, a, b, True, player, heuristic)
            if sc < val:
                val, best_mv = sc, mv
            b = min(b, val)
            if b <= a:
                break
        return val, best_mv