from move_generator import get_captures
from game_state import simulate

def piece_count(state, player):
    score = 0
    for r in range(8):
        for c in range(8):
            p = state.board[r][c]
            if p:
                v = p.value * (2 if p.is_dama else 1)
                score += v if p.player == player else -v
    return score

def greedy(state, player):
    caps = get_captures(state)
    if not caps:
        return piece_count(state, player)
    best = float('-inf')
    for mv in caps:
        sim = simulate(state, mv)
        val = sim.scores[player] - state.scores[player]
        if val > best:
            best = val
    return best

def get_heuristic(name):
    return {'piece_count': piece_count,
            'greedy':      greedy}[name]