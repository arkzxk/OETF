import tkinter as tk
import os
from board import OPERATOR_MAP

class DaMathGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OETF - DaMath AI Simulation")
        self.cell_size = 70
        
        self.info_frame = tk.Frame(self.root, bg="#333333", pady=10)
        self.info_frame.pack(fill=tk.X)
        self.info_label = tk.Label(self.info_frame, text="Initializing OETF...", 
                                   font=("Consolas", 14, "bold"), bg="#333333", fg="white")
        self.info_label.pack()

        self.canvas = tk.Canvas(self.root, width=8 * self.cell_size, height=8 * self.cell_size, bg="white")
        self.canvas.pack(padx=20, pady=20)
        
        self.end_button = tk.Button(self.root, text="End Simulation", command=self.stop_code, 
                                    bg="#d9534f", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.end_button.pack(pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.stop_code)
        
        self.root.update()

    def stop_code(self):
        self.root.destroy()
        os._exit(0)

    def update_board(self, state, move_num, nodes, time_ms, p1_name, p2_name):
        self.canvas.delete("all")
        
        player_names = [f"RED ({p1_name})", f"BLUE ({p2_name})"]
        active_player = player_names[state.active]
        
        status = (f"Turn: {state.turn} | Move: {move_num} | Active: {active_player}\n"
                  f"P1 (RED - {p1_name}): {state.scores[0]:.2f}  |  P2 (BLUE - {p2_name}): {state.scores[1]:.2f}\n"
                  f"Compute: {nodes} nodes in {time_ms}ms")
        self.info_label.config(text=status)

        for r in range(8):
            for c in range(8):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                is_white = (r + c) % 2 == 1
                bg_color = "#F0E6D2" if is_white else "#7D5A44"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#555555")
                
                if is_white and (r, c) in OPERATOR_MAP:
                    op = OPERATOR_MAP[(r, c)]
                    self.canvas.create_text(x1 + 12, y1 + 12, text=op, font=("Arial", 12, "bold"), fill="#888888")

                pc = state.board[r][c]
                if pc:
                    pc_color = "#A83232" if pc.player == 0 else "#325CA8"
                    outline_color = "gold" if pc.is_dama else "black"
                    outline_width = 3 if pc.is_dama else 1
                    
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, 
                                            fill=pc_color, outline=outline_color, width=outline_width)
                    
                    val_str = f"[{pc.value}]" if pc.is_dama else str(pc.value)
                    self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, 
                                            text=val_str, font=("Arial", 14, "bold"), fill="white")
        
        self.root.update()