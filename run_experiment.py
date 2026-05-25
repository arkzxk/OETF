import os
from benchmark import generate_benchmark, save_benchmark, load_benchmark
from heuristics import get_heuristic
from logger import Logger
from performance import run_measured_game
from visualizer import load_results, generate_dashboard

HEURISTICS = {
    'piece_count': get_heuristic('piece_count'),
    'greedy':      get_heuristic('greedy')
}
DEPTHS    = [1, 2, 3, 4, 5]
NUM_GAMES = 50

BENCHMARK_GAMES = 20

os.makedirs('charts',  exist_ok=True)
os.makedirs('results', exist_ok=True)

# Step 1 — Generate and save benchmark dataset
print("=== Step 1: Generating Benchmark Dataset ===")
generate_benchmark(num_games=BENCHMARK_GAMES, sample_every=5)
save_benchmark()

# Step 2 — Load benchmark for use during measurement
benchmark = load_benchmark()

# Step 3 — Run all experiment configurations
# Total: 2 heuristics x 5 depths x 50 games = 500 simulated games
print("\n=== Step 2: Running Experiment Configurations ===")
for h_name, h_fn in HEURISTICS.items():
    for d in DEPTHS:
        logger = Logger(h_name, d)
        print(f"Running: {h_name} | depth {d} | {NUM_GAMES} games...")
        for game_num in range(NUM_GAMES):
            benchmark_game_num = game_num % BENCHMARK_GAMES

            run_measured_game(
                depth=d,
                heuristic_fn=h_fn,
                h_name=h_name,
                logger=logger,
                game_num=benchmark_game_num,
                benchmark=benchmark
            )
        logger.save()
        print(f"Completed: {h_name} | depth {d}")

# Step 4 — Generate Visual Representation Dashboard
print("\n=== Step 3: Generating Visual Representation Dashboard ===")
df = load_results()
if not df.empty:
    generate_dashboard(df)
else:
    print("No results data found. Dashboard generation skipped.")

print("\n=== All outputs complete ===")
print("Deliverables:")
print("  - benchmark.json         -> Benchmark Dataset")
print("  - results/*.csv          -> Computational Behavior Profile")
print("  - results/*.csv          -> Heuristic Sufficiency Evidence Report")
print("  - charts/*.png           -> Visual Representation Dashboard")
print("  - Full OETF framework    -> All .py modules combined")