import json
from game_state import GameState, simulate
from move_generator import get_legal_moves, get_captures
from heuristics import get_heuristic

benchmark = []

def get_game_phase(turn):
    if turn < 20:
        return 'opening'
    elif turn < 50:
        return 'midgame'
    else:
        return 'endgame'

def exhaustive_optimal(state, depth=5):
    from alpha_beta import alpha_beta
    import alpha_beta as ab_module

    moves = get_legal_moves(state)
    if not moves:
        return None, None

    piece_count = get_heuristic('piece_count')
    score_before = state.scores[state.active]

    ab_module.nodes_expanded = 0
    _, best_mv = alpha_beta(
        state, depth,
        float('-inf'), float('inf'),
        True, state.active, piece_count
    )

    if best_mv is None:
        return None, None

    sim = simulate(state, best_mv)
    score_gained = sim.scores[state.active] - score_before

    best_mv_serialized = [list(sq) for sq in best_mv]

    return best_mv_serialized, round(score_gained, 4)

def serialize_board(state):
    out = []
    for r in range(8):
        row = []
        for c in range(8):
            p = state.board[r][c]
            row.append({
                'player': p.player,
                'value':  p.value,
                'dama':   p.is_dama
            } if p else None)
        out.append(row)
    return out

def generate_benchmark(num_games=20, sample_every=5):
    piece_count = get_heuristic('piece_count')
    from game_loop import select_move

    for game_num in range(num_games):
        state = GameState()
        turn  = 0
        print(f"Benchmark game {game_num + 1}/{num_games}...")
        while True:
            moves = get_legal_moves(state)
            if not moves or turn > 500:
                break
            if turn % sample_every == 0:
                opt_mv, opt_sc = exhaustive_optimal(state, depth=5)
                if opt_mv is not None:
                    benchmark.append({
                        'game':          game_num,
                        'turn':          turn,
                        'phase':         get_game_phase(turn),
                        'active':        state.active,
                        'board':         serialize_board(state),
                        'optimal_move':  opt_mv,
                        'optimal_score': opt_sc
                    })
            mv, _, _ = select_move(state, 3, piece_count)
            if mv is None:
                break
            state.apply_move(mv)
            turn += 1

def save_benchmark(path='benchmark.json'):
    with open(path, 'w') as f:
        json.dump(benchmark, f, indent=2)
    print(f"Benchmark saved: {len(benchmark)} states written to {path}")

def load_benchmark(path='benchmark.json'):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Benchmark file not found. Running without optimal comparisons.")
        return []