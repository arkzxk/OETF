from heuristics import get_heuristic
from game_loop import run_game

class ConsoleLogger:
    def __init__(self):
        self.move_num = 0

    def log_move(self, state, move, nodes, t):
        self.move_num += 1
        print(f"Move {self.move_num:>3} | "
              f"Player {state.active} | "
              f"Move: {move} | "
              f"Nodes: {nodes} | "
              f"Time: {t*1000:.2f}ms | "
              f"Scores -> P0: {state.scores[0]:.2f}, "
              f"P1: {state.scores[1]:.2f}")

    def log_result(self, state):
        print("\n--- GAME OVER ---")
        print(f"Final Score -> P0: {state.scores[0]:.2f} | "
              f"P1: {state.scores[1]:.2f}")
        if state.scores[0] > state.scores[1]:
            print("Winner: Player 0")
        elif state.scores[1] > state.scores[0]:
            print("Winner: Player 1")
        else:
            print("Result: Draw")

heuristic_fn = get_heuristic('piece_count')
logger = ConsoleLogger()
run_game(depth=2, heuristic_fn=heuristic_fn, logger=logger)