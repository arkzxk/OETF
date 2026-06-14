import time
import tkinter as tk
from tkinter import ttk
from heuristics import get_heuristic
from game_loop import run_game
from gui import DaMathGUI

class GUILogger:
    def __init__(self, gui, p1_name, p2_name):
        self.gui = gui
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.move_num = 0

    def log_move(self, state, move, nodes, t):
        self.move_num += 1
        time_ms = t * 1000
        
        self.gui.update_board(state, self.move_num, nodes, time_ms, self.p1_name, self.p2_name)
        
        active_name = self.p1_name if state.active == 0 else self.p2_name
        print(f"Move {self.move_num} | {active_name} played {move}")
        
        time.sleep(1.5)

    def log_result(self, state):
        print("\n--- GAME OVER ---")
        print(f"Final Score -> {self.p1_name}: {state.scores[0]:.2f} | {self.p2_name}: {state.scores[1]:.2f}")
        
        winner_text = "Result: Draw"
        if state.scores[0] > state.scores[1]:
            winner_text = f"Winner: {self.p1_name}"
        elif state.scores[1] > state.scores[0]:
            winner_text = f"Winner: {self.p2_name}"
            
        self.gui.info_label.config(text=f"GAME OVER\n{winner_text}\nP1: {state.scores[0]:.2f} | P2: {state.scores[1]:.2f}", fg="gold")
        
        # Enable the End Simulation button
        if hasattr(self.gui, 'end_button'):
            self.gui.end_button.config(state=tk.NORMAL)
            
        self.gui.root.update()

def confirm_setup():
    # Stop the setup window's loop first instead of destroying it immediately
    setup_window.quit()

if __name__ == "__main__":
    # --- PHASE 1: SETUP WINDOW ---
    setup_window = tk.Tk()
    setup_window.title("OETF - Setup Menu")
    setup_window.geometry("400x250")
    setup_window.configure(bg="#f0f0f0")
    
    tk.Label(setup_window, text="OETF Simulation Setup", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)
    
    tk.Label(setup_window, text="Select Matchup:", bg="#f0f0f0", font=("Arial", 10)).pack()
    sim_var = tk.StringVar(value="Piece-Count vs Piece-Count")
    sim_dropdown = ttk.Combobox(setup_window, textvariable=sim_var, state="readonly", width=35)
    sim_dropdown['values'] = ("Piece-Count vs Piece-Count", "Greedy vs Greedy")
    sim_dropdown.pack(pady=5)
    
    tk.Label(setup_window, text="Select Search Depth (Alpha-Beta):", bg="#f0f0f0", font=("Arial", 10)).pack()
    depth_var = tk.StringVar(value="2")
    depth_dropdown = ttk.Combobox(setup_window, textvariable=depth_var, state="readonly", width=10)
    depth_dropdown['values'] = ("1", "2", "3", "4", "5")
    depth_dropdown.pack(pady=5)
    
    tk.Button(setup_window, text="Run Simulation", command=confirm_setup, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=15).pack(pady=20)
    
    setup_window.mainloop()
    
    # Capture the values BEFORE destroying the window completely
    selected_sim = sim_var.get()
    selected_depth = int(depth_var.get())
    setup_window.destroy()

    # --- PHASE 2: MAIN SIMULATION ---
    if selected_sim == "Piece-Count vs Piece-Count":
        h_name = 'piece_count'
        p1_name = "Piece-Count AI"
        p2_name = "Piece-Count AI"
    else:
        h_name = 'greedy'
        p1_name = "Greedy AI"
        p2_name = "Greedy AI"
        
    app = DaMathGUI()
    heuristic_fn = get_heuristic(h_name)
    logger = GUILogger(app, p1_name, p2_name)
    
    run_game(depth=selected_depth, heuristic_fn=heuristic_fn, logger=logger)
    
    app.root.mainloop()