import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def load_results(path='results'):
    frames = []
    for fn in os.listdir(path):
        if fn.endswith('.csv'):
            frames.append(pd.read_csv(f"{path}/{fn}"))
    if not frames:
        print("No CSV files found in results/")
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)

# --- Computational Behavior Charts ---

def plot_nodes_per_depth(df):
    fig, ax = plt.subplots()
    for h in df['heuristic'].unique():
        d   = df[df['heuristic'] == h]
        avg = d.groupby('depth')['nodes'].mean()
        ax.plot(avg.index, avg.values, marker='o', label=h)
    ax.set_title('Avg Nodes Expanded per Search Depth')
    ax.set_xlabel('Search Depth')
    ax.set_ylabel('Avg Nodes Expanded')
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/nodes_per_depth.png')
    plt.close()

def plot_exec_time_per_depth(df):
    fig, ax = plt.subplots()
    for h in df['heuristic'].unique():
        d   = df[df['heuristic'] == h]
        avg = d.groupby('depth')['time_ms'].mean()
        ax.plot(avg.index, avg.values, marker='s', label=h)
    ax.set_title('Avg Execution Time per Depth (ms)')
    ax.set_xlabel('Search Depth')
    ax.set_ylabel('Avg Time (ms)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/time_per_depth.png')
    plt.close()

def plot_pruning_ratio(df):
    fig, ax  = plt.subplots()
    heurs    = df['heuristic'].unique()
    depths   = sorted(df['depth'].unique())
    x        = np.arange(len(depths))
    width    = 0.35
    for i, h in enumerate(heurs):
        d    = df[df['heuristic'] == h]
        vals = [d[d['depth'] == dep]['pruning_ratio'].mean()
                for dep in depths]
        ax.bar(x + i * width, vals, width, label=h)
    ax.set_title('Pruning Ratio per Depth')
    ax.set_xlabel('Search Depth')
    ax.set_ylabel('Pruning Ratio')
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(depths)
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/pruning_ratio.png')
    plt.close()

# --- Scoring Performance Charts ---

def plot_score_yield_per_depth(df):
    fig, ax = plt.subplots()
    for h in df['heuristic'].unique():
        d   = df[df['heuristic'] == h]
        avg = d.groupby('depth')['score_p0'].mean()
        ax.plot(avg.index, avg.values, marker='o', label=h)
    ax.set_title('Avg Arithmetic Score Yield per Depth')
    ax.set_xlabel('Search Depth')
    ax.set_ylabel('Avg Cumulative Score')
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/score_yield_per_depth.png')
    plt.close()

def plot_score_distribution(df):
    fig, ax = plt.subplots()
    data    = [df[df['heuristic'] == h]['score_p0'].values
               for h in df['heuristic'].unique()]
    labels  = df['heuristic'].unique().tolist()
    ax.boxplot(data, labels=labels)
    ax.set_title('Score Distribution per Heuristic')
    ax.set_ylabel('Cumulative Score')
    plt.tight_layout()
    plt.savefig('charts/score_distribution.png')
    plt.close()

def plot_score_deviation(df):
    fig, ax = plt.subplots()
    heurs   = df['heuristic'].unique()
    depths  = sorted(df['depth'].unique())
    x       = np.arange(len(depths))
    width   = 0.35
    for i, h in enumerate(heurs):
        d    = df[df['heuristic'] == h]
        vals = [d[d['depth'] == dep]['score_deviation'].mean()
                for dep in depths]
        ax.bar(x + i * width, vals, width, label=h)
    ax.set_title('Avg Score Deviation from Optimal')
    ax.set_xlabel('Search Depth')
    ax.set_ylabel('Avg Deviation')
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(depths)
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/score_deviation.png')
    plt.close()

# --- Heuristic Sufficiency Charts ---

def plot_suboptimal_rate(df):
    fig, ax = plt.subplots()
    heurs   = df['heuristic'].unique()
    rates   = [df[df['heuristic'] == h]['suboptimal'].mean() * 100
               for h in heurs]
    ax.bar(heurs, rates, color=['steelblue', 'coral'])
    ax.set_title('Suboptimal Move Rate per Heuristic')
    ax.set_ylabel('Suboptimal Rate (%)')
    plt.tight_layout()
    plt.savefig('charts/suboptimal_rate.png')
    plt.close()

def plot_failure_by_phase(df):
    phases  = ['opening', 'midgame', 'endgame']
    heurs   = df['heuristic'].unique()
    fig, ax = plt.subplots()
    bottoms = np.zeros(len(heurs))
    colors  = ['#4e79a7', '#f28e2b', '#e15759']
    for i, phase in enumerate(phases):
        vals = [
            df[(df['heuristic'] == h) &
               (df['game_phase'] == phase)
               ]['suboptimal'].mean() * 100
            for h in heurs
        ]
        ax.bar(heurs, vals, bottom=bottoms,
               label=phase, color=colors[i])
        bottoms += np.array(vals)
    ax.set_title('Failure Frequency by Game Phase')
    ax.set_ylabel('Suboptimal Rate (%)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/failure_by_phase.png')
    plt.close()

def plot_operator_heatmap(df):
    board = np.zeros((8, 8))
    fails = df[df['operator_blind'] == True]
    for _, row in fails.iterrows():
        try:
            r, c = eval(row['land_square'])
            board[r][c] += 1
        except Exception:
            continue
    fig, ax = plt.subplots()
    im      = ax.imshow(board, cmap='Reds')
    ax.set_title('Operator-Unaware Selection Heatmap')
    plt.colorbar(im, ax=ax, label='Failure Count')
    plt.tight_layout()
    plt.savefig('charts/operator_heatmap.png')
    plt.close()

def plot_score_loss_histogram(df):
    fig, ax = plt.subplots()
    for h in df['heuristic'].unique():
        d = df[(df['heuristic'] == h) &
               (df['suboptimal'] == True)]
        if not d.empty:
            ax.hist(d['score_loss'].values,
                    bins=20, alpha=0.6, label=h)
    ax.set_title('Score Loss Distribution per Failure')
    ax.set_xlabel('Arithmetic Score Lost')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig('charts/score_loss_histogram.png')
    plt.close()

def generate_dashboard(df):
    os.makedirs('charts', exist_ok=True)
    print("Generating Computational Behavior charts...")
    plot_nodes_per_depth(df)
    plot_exec_time_per_depth(df)
    plot_pruning_ratio(df)
    print("Generating Scoring Performance charts...")
    plot_score_yield_per_depth(df)
    plot_score_distribution(df)
    plot_score_deviation(df)
    print("Generating Heuristic Sufficiency charts...")
    plot_suboptimal_rate(df)
    plot_failure_by_phase(df)
    plot_operator_heatmap(df)
    plot_score_loss_histogram(df)
    print("Visual Representation Dashboard complete. Charts saved to /charts.")