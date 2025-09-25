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

        # Horizontal row: board (left) and controls (right)
        row_frame = tk.Frame(self.right, bg="black")
        row_frame.grid(row=0, column=0, sticky="nw")
        
        # Board canvas
        self.canvas = tk.Canvas(row_frame, width=BOARD_W, height=BOARD_H)
        self.canvas.grid(row=0, column=0, padx=(0, 12), sticky="nw")

        # Controls column (stacked vertically) - to the right of the board
        ctrls = tk.Frame(row_frame, bg="black")
        ctrls.grid(row=0, column=1, sticky="nwe")

        # Mode selector
        tk.Label(ctrls, text="Mode:", font=("Arial", 10, "bold"), bg="black", fg="white").grid(row=0, column=0, sticky="we", pady=(0, 4))
        self.mode_var = tk.StringVar(value="deterministic")
        self.mode_menu = tk.OptionMenu(ctrls, self.mode_var, "deterministic", "astar", command=lambda _: self.on_mode_change())
        self.mode_menu.configure(font=("Arial", 10), highlightthickness=0)
        self.mode_menu.grid(row=1, column=0, sticky="we", pady=(0, 8))

        # Buttons
        self.start_btn = tk.Button(ctrls, text="Start", command=self.start_search, bd=0, font=("Arial", 10, "bold"), bg="white", fg="black")
        self.start_btn.grid(row=2, column=0, sticky="we", pady=(0, 6))

        self.run_btn = tk.Button(ctrls, text="Run simulation", command=self.run_simulation, bd=0, font=("Arial", 10, "bold"), bg="white", fg="black")
        self.run_btn.grid(row=3, column=0, sticky="we", pady=(0, 6))

        self.pause_btn = tk.Button(ctrls, text="Pause", command=self.toggle_pause_resume, state="disabled", bd=0, font=("Arial", 10, "bold"), bg="white", fg="black")
        self.pause_btn.grid(row=4, column=0, sticky="we", pady=(0, 6))

        self.next_btn = tk.Button(ctrls, text="Next Step", command=self.next_step, bd=0, font=("Arial", 10, "bold"), state="disabled", bg="white", fg="black")
        self.next_btn.grid(row=5, column=0, sticky="we", pady=(0, 6))

        tk.Label(ctrls, text="Speed:", font=("Arial", 10, "bold"), bg="black", fg="white").grid(row=6, column=0, sticky="we", pady=(6, 4))
        self.speed_var = tk.StringVar(value="150")
        self.speed_menu = tk.OptionMenu(ctrls, self.speed_var, "400", "150", "50", command=lambda _: self.on_speed_change())
        self.speed_menu.configure(font=("Arial", 10), highlightthickness=0)
        self.speed_menu.grid(row=7, column=0, sticky="we", pady=(0, 8))

        self.restart_btn = tk.Button(ctrls, text="Restart", command=self.restart, bd=0, font=("Arial", 10, "bold"), bg="white", fg="black")
        self.restart_btn.grid(row=8, column=0, sticky="we", pady=(0, 6))

        # Grouped Status Box
        status_box = tk.Frame(ctrls, bg="black")
        status_box.grid(row=9, column=0, sticky="we", pady=(8, 0))

        # Status message
        self.msg = tk.StringVar()
        self.msg_label = tk.Label(status_box, textvariable=self.msg, fg="white", bg=COL_MSG,
                                  font=("Georgia", 12, "bold"), padx=10, pady=6)
        self.msg_label.grid(row=0, column=0, pady=(0, 6), sticky="we")
        
        # Mode indicator
        self.mode_indicator = tk.StringVar()
        self.mode_label = tk.Label(status_box, textvariable=self.mode_indicator, fg="black", bg="#f0f0f0",
                                   font=("Arial", 11, "bold"), padx=10, pady=4)
        self.mode_label.grid(row=1, column=0, pady=(0, 6), sticky="we")

        # Queens placed
        self.placed_var = tk.StringVar()
        self.placed_label = tk.Label(status_box, textvariable=self.placed_var, fg="black", bg="#f0f0f0",
                                     font=("Arial", 11, "bold"), padx=10, pady=4)
        self.placed_label.grid(row=2, column=0, pady=(0, 6), sticky="we")

        # Step counter
        self.step_var = tk.StringVar()
        self.step_label = tk.Label(status_box, textvariable=self.step_var, fg="#2c5aa0", bg="#e8f4f8",
                                   font=("Arial", 11, "bold"), padx=10, pady=4, highlightbackground="#2c5aa0", highlightthickness=1)
        self.step_label.grid(row=3, column=0, pady=(0, 0), sticky="we")
        

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
        self.timer_id = None
        self.is_paused = False

        self.draw_board()
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.update_mode_indicator()
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
        # disable mode switching during run
        self.mode_menu.config(state="disabled")
        
        # Immediately perform the first step to place the first queen
        new_state, message, is_complete = self.astar_search.next_step()
        self.state = new_state
        
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.draw_board()
        self.update_message(message)
        
        if is_complete:
            if self.astar_search.solved:
                self.next_btn.config(state="disabled")
                self.update_message("Solution found! All queens placed without conflicts.")
            else:
                self.next_btn.config(state="disabled")
                self.update_message("Search failed - no solution found.")
            self.mode_menu.config(state="normal")
    
    def next_step(self):
        """Perform the next step of A* search"""
        new_state, message, is_complete = self.astar_search.next_step()
        self.state = new_state
        
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.draw_board()
        self.update_message(message)
        
        if is_complete:
            if self.astar_search.solved:
                self.next_btn.config(state="disabled")
                self.update_message("Solution found! All queens placed without conflicts.")
            else:
                self.next_btn.config(state="disabled")
                self.update_message("Search failed - no solution found.")
            self.mode_menu.config(state="normal")

    def restart(self):
        """Reset the search to start over"""
        self.stop_timer()
        self.astar_search.reset()
        self.state = self.astar_search.current_state
        self.search_started = False
        self.start_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.run_btn.config(state="normal", text="Run simulation")
        self.pause_btn.config(state="disabled", text="Pause")
        self.mode_menu.config(state="normal")
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.update_mode_indicator()
        self.draw_board()
        self.update_message("Search reset. Click 'Start' to begin the A* algorithm.")

    # ---------------- Simulation helpers ---------------- #
    def get_delay_ms(self) -> int:
        try:
            return int(self.speed_var.get())
        except Exception:
            return 150

    def on_speed_change(self):
        if self.timer_id is not None and not self.is_paused:
            self.stop_timer()
            self.start_timer()

    def start_timer(self):
        delay = self.get_delay_ms()
        self.timer_id = self.root.after(delay, self.tick_sim)

    def stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def tick_sim(self):
        new_state, message, is_complete = self.astar_search.next_step()
        self.state = new_state
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.draw_board()
        self.update_message(message)

        if is_complete:
            self.stop_timer()
            self.next_btn.config(state="disabled")
            self.run_btn.config(state="normal", text="Run simulation")
            self.mode_menu.config(state="normal")
            self.pause_btn.config(state="disabled", text="Pause")
            # finalize message clarity
            if self.astar_search.solved:
                self.update_message("Solution found! All queens placed without conflicts.")
            else:
                self.update_message("Search failed - no solution found.")
        else:
            # schedule next tick if not paused
            if not self.is_paused:
                self.start_timer()

    def run_simulation(self):
        # ensure A* frontier mode
        if self.mode_var.get() != "astar":
            self.mode_var.set("astar")
            self.on_mode_change()
        else:
            if not self.search_started:
                self.astar_search.set_mode("astar")
                self.state = self.astar_search.current_state

        self.search_started = True
        self.start_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.run_btn.config(state="disabled", text="Running...")
        self.mode_menu.config(state="disabled")
        self.pause_btn.config(state="normal", text="Pause")
        self.is_paused = False
        self.stop_timer()
        self.start_timer()

    def toggle_pause_resume(self):
        if self.pause_btn["state"] == "disabled":
            return
        if self.is_paused:
            # resume
            self.is_paused = False
            self.pause_btn.config(text="Pause")
            self.start_timer()
        else:
            # pause
            self.is_paused = True
            self.pause_btn.config(text="Resume")
            self.stop_timer()

    # ---------------- UI updates ---------------- #
    def on_mode_change(self):
        mode = self.mode_var.get()
        self.astar_search.set_mode(mode)
        self.state = self.astar_search.current_state
        self.search_started = False
        self.start_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.run_btn.config(state="normal", text="Run simulation")
        self.pause_btn.config(state="disabled", text="Pause")
        self.update_side_panel()
        self.update_placed_display()
        self.update_step_display()
        self.update_mode_indicator()
        self.draw_board()
        label = "Deterministic (8 steps)" if mode == "deterministic" else "A* Frontier (no backtracking)"
        self.update_message(f"Mode changed to {label}. Click 'Start' to begin.")

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
    
    def update_placed_display(self):
        placed_queens = sum(1 for c in self.state if c != -1)
        self.placed_var.set(f"Queens placed: {placed_queens}/{BOARD_SIZE}")

    def update_step_display(self):
        self.step_var.set(f"Algorithm steps: {self.astar_search.step_count}")

    def update_mode_indicator(self):
        mode = self.astar_search.mode
        label = "Deterministic (8 steps)" if mode == "deterministic" else "A* Frontier (no backtracking)"
        self.mode_indicator.set(f"Mode: {label}")

    def update_message(self, text: str):
        self.msg.set(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensGUI(root)
    root.mainloop()
