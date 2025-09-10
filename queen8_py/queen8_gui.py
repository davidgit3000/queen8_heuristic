import tkinter as tk
from typing import Tuple
from queen8_algorithm import StepByStepAStar, attacking_pairs, BOARD_SIZE

# ---------------------------- GUI constants ---------------------------- #
CELL = 60
BOARD_W = BOARD_SIZE * CELL
BOARD_H = BOARD_SIZE * CELL
PADDING = 16

COL_LIGHT = "#d4b896"  # light brown/tan
COL_DARK = "#2f6f62"   # teal
COL_MSG = "#a24e21"

# ---------------------------- GUI ---------------------------- #

class EightQueensGUI:
    def __init__(self, root):
        self.root = root
        root.title("8-Queens — Step-by-Step A* Search")
        root.configure(bg="black")  # Light gray background

        # Layout frames
        self.left = tk.Frame(root, bg="black")
        self.left.grid(row=0, column=0, padx=8, pady=8, sticky="nsw")
        self.right = tk.Frame(root, bg="black")
        self.right.grid(row=0, column=1, padx=8, pady=8, sticky="nse")

        # Board canvas
        self.canvas = tk.Canvas(self.right, width=BOARD_W, height=BOARD_H)
        self.canvas.grid(row=0, column=0)

        # Buttons row
        btns = tk.Frame(self.right, bg="black")
        btns.grid(row=1, column=0, pady=(10, 0))
        self.start_btn = tk.Button(btns, text="Start", command=self.start_search, bd=0, font=("Arial", 10, "bold"), bg="white", fg="black", activebackground="#333333", activeforeground="black")
        self.start_btn.grid(row=0, column=0, padx=0, pady=0)
        self.next_btn = tk.Button(btns, text="Next Step", command=self.next_step, bd=0, font=("Arial", 10, "bold"), state="disabled", bg="white", fg="black", disabledforeground="black")
        self.next_btn.grid(row=0, column=1, padx=0, pady=0)
        self.restart_btn = tk.Button(btns, text="Restart", command=self.restart, bd=0, font=("Arial", 10, "bold"), bg="white", fg="black", activebackground="#333333", activeforeground="black")
        self.restart_btn.grid(row=0, column=2, padx=0, pady=0)

        # Status message
        self.msg = tk.StringVar()
        self.msg_label = tk.Label(self.right, textvariable=self.msg, fg="white", bg=COL_MSG,
                                  font=("Georgia", 12, "bold"), padx=10, pady=6)
        self.msg_label.grid(row=2, column=0, pady=(10, 0), sticky="we")
        
        # Heuristic display
        self.heuristic_var = tk.StringVar()
        self.heuristic_label = tk.Label(self.right, textvariable=self.heuristic_var, fg="black", bg="#f0f0f0",
                                       font=("Arial", 11, "bold"), padx=10, pady=4)
        self.heuristic_label.grid(row=3, column=0, pady=(5, 0), sticky="we")

        # Queens array panel
        tk.Label(self.left, text="Queen positions:", font=("Georgia", 12, "bold"), bg="black", fg="white").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.qvars = [tk.StringVar() for _ in range(BOARD_SIZE)]
        self.qlabels = []
        for r in range(BOARD_SIZE):
            sv = self.qvars[r]
            lbl = tk.Label(self.left, textvariable=sv, font=("Courier New", 12), bg="black", fg="white")
            lbl.grid(row=r + 1, column=0, sticky="w")
            self.qlabels.append(lbl)

        # Initialize A* search
        self.astar_search = StepByStepAStar()
        self.state = self.astar_search.current_state
        self.search_started = False

        self.draw_board()
        self.update_side_panel()
        self.update_heuristic_display()
        self.update_message("Click 'Start' to begin the A* search algorithm.")

    # ---------------- Drawing ---------------- #
    def draw_board(self):
        self.canvas.delete("all")
        # squares
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0, y0 = c * CELL, r * CELL
                x1, y1 = x0 + CELL, y0 + CELL
                fill = COL_LIGHT if (r + c) % 2 == 0 else COL_DARK
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=0)
        
        # queens (draw first)
        for r in range(BOARD_SIZE):
            c = self.state[r]
            if c == -1:
                continue
            self.draw_queen(r, c)
        
        # Highlight the row where the most recent queen was placed - draw after queens
        if (self.search_started and not self.astar_search.solved):
            # Find the highest row with a placed queen (most recently placed)
            last_placed_row = -1
            for r in range(BOARD_SIZE):
                if self.state[r] != -1:
                    last_placed_row = r
            
            # Highlight the row with the most recent queen placement
            if last_placed_row >= 0:
                y0 = last_placed_row * CELL
                # Create border highlight with padding to prevent clipping
                border_width = 4
                padding = border_width // 2
                self.canvas.create_rectangle(padding, y0 + padding, BOARD_W - padding, y0 + CELL - padding, fill="", outline="red", width=border_width, tags="highlight")
                

    def draw_queen(self, r: int, c: int):
        x = c * CELL + CELL // 2
        y = r * CELL + CELL // 2
        # Add white background circle for better visibility on highlights
        self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="white", outline="#8B4513", width=2)
        # Draw queen crown symbol
        self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", int(CELL * 0.7)), fill="#8B4513")

    # ---------------- Interaction ---------------- #
    def start_search(self):
        """Start the A* search algorithm"""
        self.search_started = True
        self.start_btn.config(state="disabled")
        self.next_btn.config(state="normal")
        
        # Immediately perform the first step to place the first queen
        new_state, message, is_complete = self.astar_search.next_step()
        self.state = new_state
        
        self.update_side_panel()
        self.update_heuristic_display()
        self.draw_board()
        self.update_message(message)
        
        if is_complete:
            if self.astar_search.solved:
                self.next_btn.config(state="disabled")
                self.update_message("Solution found! All queens placed without conflicts.")
            else:
                self.next_btn.config(state="disabled")
                self.update_message("Search failed - no solution found.")
    
    def next_step(self):
        """Perform the next step of A* search"""
        new_state, message, is_complete = self.astar_search.next_step()
        self.state = new_state
        
        self.update_side_panel()
        self.update_heuristic_display()
        self.draw_board()
        self.update_message(message)
        
        if is_complete:
            if self.astar_search.solved:
                self.next_btn.config(state="disabled")
                self.update_message("Solution found! All queens placed without conflicts.")
            else:
                self.next_btn.config(state="disabled")
                self.update_message("Search failed - no solution found.")

    def restart(self):
        """Reset the search to start over"""
        self.astar_search.reset()
        self.state = self.astar_search.current_state
        self.search_started = False
        self.start_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.update_side_panel()
        self.update_heuristic_display()
        self.draw_board()
        self.update_message("Search reset. Click 'Start' to begin the A* algorithm.")

    def update_side_panel(self):
        for r in range(BOARD_SIZE):
            val = self.state[r]
            if val == -1:
                txt = f"Row {r}: not placed"
            else:
                txt = f"Row {r}: column {val}"
            self.qvars[r].set(txt)
            
            # Highlight the row where the most recent queen was placed
            is_current = False
            if self.search_started and not self.astar_search.solved:
                # Find the highest row with a placed queen (most recently placed)
                last_placed_row = -1
                for row in range(BOARD_SIZE):
                    if self.state[row] != -1:
                        last_placed_row = row
                is_current = (r == last_placed_row and last_placed_row >= 0)
            
            self.qlabels[r].configure(fg="#cc6a00" if is_current else "white")
    
    def update_heuristic_display(self):
        """Update the heuristic function display"""
        h_value = attacking_pairs(self.state)
        placed_queens = sum(1 for c in self.state if c != -1)
        self.heuristic_var.set(f"Heuristic h(n) = {h_value} | Queens placed: {placed_queens}/{BOARD_SIZE}")

    def update_message(self, text: str):
        self.msg.set(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensGUI(root)
    root.mainloop()
