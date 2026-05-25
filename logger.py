import csv
import os
from game_state import simulate
from move_generator import get_legal_moves
from board import OPERATOR_MAP

def normalize_move(move):
    return [list(sq) for sq in move]

def compute_score_gained(state, move):
    score_before = state.scores[state.active]
    sim = simulate(state, move)
    return sim.scores[state.active] - score_before

def detect_operator_blind(state, chosen_move, all_moves):
    if not all_moves or len(all_moves) < 2:
        return False

    chosen_gain  = compute_score_gained(state, chosen_move)
    chosen_land  = tuple(chosen_move[-1])
    chosen_op    = OPERATOR_MAP.get(chosen_land, '+')

    for mv in all_moves:
        if normalize_move(mv) == normalize_move(chosen_move):
            continue
        alt_gain = compute_score_gained(state, mv)
        alt_land = tuple(mv[-1])
        alt_op   = OPERATOR_MAP.get(alt_land, '+')
        if alt_gain > chosen_gain and alt_op != chosen_op:
            return True
    return False


class Logger:
    def __init__(self, h_name, depth):
        self.h_name   = h_name
        self.depth    = depth
        self.game_num = 0
        self.rows     = []

    def get_game_phase(self, turn):
        if turn < 20:
            return 'opening'
        elif turn < 50:
            return 'midgame'
        else:
            return 'endgame'

    def log_move(self, state, move, nodes, t,
                optimal_move=None, optimal_score=None,
                pruning_ratio=0.0, all_moves=None):
        chosen_gain = compute_score_gained(state, move)

        is_suboptimal   = False
        score_deviation = 0.0
        score_loss      = 0.0

        if optimal_move is not None:
            norm_chosen  = normalize_move(move)
            norm_optimal = normalize_move(optimal_move)
            is_suboptimal    = (norm_chosen != norm_optimal)
            score_deviation  = abs(chosen_gain - (optimal_score or 0))
            score_loss       = max(0.0, (optimal_score or 0) - chosen_gain)

        operator_blind = False
        if all_moves is not None:
            operator_blind = detect_operator_blind(state, move, all_moves)

        land_square = move[-1] if move else None

        self.rows.append({
            'game':            self.game_num,
            'turn':            state.turn,
            'player':          state.active,
            'move':            str(normalize_move(move)),
            'land_square':     str(list(land_square) if land_square else None),
            'nodes':           nodes,
            'time_ms':         round(t * 1000, 4),
            'pruning_ratio':   round(pruning_ratio, 4),
            'score_p0':        state.scores[0],
            'score_p1':        state.scores[1],
            'heuristic':       self.h_name,
            'depth':           self.depth,
            'game_phase':      self.get_game_phase(state.turn),
            'suboptimal':      is_suboptimal,
            'score_deviation': round(score_deviation, 4),
            'score_loss':      round(score_loss, 4),
            'operator_blind':  operator_blind
        })

    def log_result(self, state):
        self.game_num += 1

    def save(self, path='results'):
        os.makedirs(path, exist_ok=True)
        if not self.rows:
            print(f"No data to save for {self.h_name} depth {self.depth}.")
            return
        fn = f"{path}/{self.h_name}_d{self.depth}.csv"
        with open(fn, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            w.writeheader()
            w.writerows(self.rows)
        print(f"Saved: {fn}")