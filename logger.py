import csv
import os

class Logger:
    def __init__(self, h_name, depth):
        self.h_name    = h_name
        self.depth     = depth
        self.game_num  = 0
        self.rows      = []

    def get_game_phase(self, turn):
        if turn < 20:
            return 'opening'
        elif turn < 50:
            return 'midgame'
        else:
            return 'endgame'

    def log_move(self, state, move, nodes, t,
                 optimal_move=None, optimal_score=None,
                 pruning_ratio=0.0):
        chosen_score = state.scores[state.active]
        is_suboptimal = False
        score_deviation = 0.0
        score_loss = 0.0
        operator_blind = False

        if optimal_move is not None:
            is_suboptimal   = (move != optimal_move)
            score_deviation = abs(chosen_score - (optimal_score or 0))
            score_loss      = max(0, (optimal_score or 0) - chosen_score)

        # Determine landing square of the move
        land_square = move[-1] if move else None

        self.rows.append({
            'game':           self.game_num,
            'turn':           state.turn,
            'player':         state.active,
            'move':           str(move),
            'land_square':    str(land_square),
            'nodes':          nodes,
            'time_ms':        round(t * 1000, 4),
            'pruning_ratio':  round(pruning_ratio, 4),
            'score_p0':       state.scores[0],
            'score_p1':       state.scores[1],
            'heuristic':      self.h_name,
            'depth':          self.depth,
            'game_phase':     self.get_game_phase(state.turn),
            'suboptimal':     is_suboptimal,
            'score_deviation':round(score_deviation, 4),
            'score_loss':     round(score_loss, 4),
            'operator_blind': operator_blind
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