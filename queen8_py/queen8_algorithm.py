from typing import List, Tuple

# ---------------------------- Board constants ---------------------------- #
BOARD_SIZE = 8

# ---------------------------- Heuristic ---------------------------- #

def attacking_pairs(state: Tuple[int, ...]) -> int:
    """Number of attacking queen pairs (rows implied unique, but function
    works regardless). state[r] = column of queen in row r or -1 if empty."""
    rows = [i for i, c in enumerate(state) if c != -1]
    cols = [state[r] for r in rows]
    pairs = 0
    # row conflicts (only if multiple per row allowed; here one per row, so 0)
    # column & diagonal conflicts across placed rows
    for i in range(len(rows)):
        r1, c1 = rows[i], cols[i]
        for j in range(i + 1, len(rows)):
            r2, c2 = rows[j], cols[j]
            same_col = (c1 == c2)
            same_diag = abs(r1 - r2) == abs(c1 - c2)
            if same_col or same_diag:
                pairs += 1
    return pairs

# ---------------------------- Step-by-step A* Search ---------------------------- #

class StepByStepAStar:
    def __init__(self):
        self.mode = 'deterministic'  # 'deterministic' | 'astar'
        self.reset()

    def set_mode(self, mode: str):
        if mode not in ('deterministic', 'astar'):
            return
        self.mode = mode
        self.reset()

    def reset(self):
        """Reset the search to start from beginning"""
        self.current_state = tuple([-1] * BOARD_SIZE)
        self.current_row = 0
        self.solved = False
        self.stuck = False
        self.step_count = 0
        if self.mode == 'astar':
            # Open list frontier: each node is (f, g, state, row)
            h0 = self.calculate_future_conflicts(self.current_state, 0)
            self.open_list: List[Tuple[int, int, Tuple[int, ...], int]] = [(h0, 0, self.current_state, 0)]
        else:
            # Known valid solution: one queen per row
            self.fixed_solution: List[int] = [0, 4, 7, 5, 2, 6, 1, 3]
    
    def get_valid_columns(self, state: Tuple[int, ...], row: int) -> List[int]:
        """Get all valid columns for placing a queen in the given row"""
        valid_cols = []
        for col in range(BOARD_SIZE):
            # Create temporary state with queen at (row, col)
            temp_state = list(state)
            temp_state[row] = col
            
            # Check if this placement conflicts with existing queens
            conflicts = False
            for r in range(row):
                if temp_state[r] == -1:
                    continue
                c = temp_state[r]
                # Check column conflict
                if c == col:
                    conflicts = True
                    break
                # Check diagonal conflicts
                if abs(r - row) == abs(c - col):
                    conflicts = True
                    break
            
            if not conflicts:
                valid_cols.append(col)
        
        return valid_cols
    
    def next_step(self) -> Tuple[Tuple[int, ...], str, bool]:
        """Perform one step of the search based on mode. Returns (new_state, message, is_complete)"""
        if self.solved:
            return self.current_state, "Already solved!", True
        if self.stuck:
            return self.current_state, "Search failed - no solution found", True

        self.step_count += 1

        if self.mode == 'deterministic':
            # If all rows placed, validate and finish
            if self.current_row >= BOARD_SIZE:
                h = attacking_pairs(self.current_state)
                if h == 0:
                    self.solved = True
                    return self.current_state, f"Step {self.step_count}: Solution found!", True
                else:
                    self.stuck = True
                    return self.current_state, "Unexpected conflict at full placement.", True

            col = self.fixed_solution[self.current_row]
            new_state = list(self.current_state)
            new_state[self.current_row] = col
            self.current_state = tuple(new_state)
            msg = f"Step {self.step_count}: Placed queen at row {self.current_row}, col {col}."
            self.current_row += 1
            if self.current_row == BOARD_SIZE:
                h = attacking_pairs(self.current_state)
                if h == 0:
                    self.solved = True
                    return self.current_state, f"Step {self.step_count}: Solution found!", True
                else:
                    self.stuck = True
                    return self.current_state, "Unexpected conflict at full placement.", True
            return self.current_state, msg, False

        # A* frontier (no backtracking)
        if not self.open_list:
            self.stuck = True
            return self.current_state, "Frontier exhausted. No solution found (no backtracking).", True

        # pop node with smallest f
        self.open_list.sort(key=lambda x: x[0])
        f, g, state, row = self.open_list.pop(0)
        self.current_state = state
        self.current_row = row

        if row >= BOARD_SIZE and attacking_pairs(state) == 0:
            self.solved = True
            return self.current_state, f"Step {self.step_count}: Solution found!", True

        valid_cols = self.get_valid_columns(state, row)
        if not valid_cols:
            return self.current_state, f"Step {self.step_count}: Dead end at row {row}. Exploring other candidates...", False

        children: List[Tuple[int, int, Tuple[int, ...], int]] = []
        for col in valid_cols:
            child_state = list(state)
            child_state[row] = col
            child_state_t = tuple(child_state)
            g_child = row + 1
            h_child = self.calculate_future_conflicts(child_state_t, row + 1)
            f_child = g_child + h_child
            node = (f_child, g_child, child_state_t, row + 1)
            children.append(node)
            self.open_list.append(node)

        # For visualization choose best child to display now
        children.sort(key=lambda x: x[0])
        best = children[0]
        _, _, best_state, best_row = best
        placed_col = [c for c in range(BOARD_SIZE) if best_state[best_row - 1] == c][0]
        self.current_state = best_state
        self.current_row = best_row
        msg = f"Step {self.step_count}: Expanded row {row}, placed queen at col {placed_col}. Open list size: {len(self.open_list)}"
        return self.current_state, msg, False
    
    # Note: choose_best_column/backtrack removed in new modes. Kept get_valid_columns for constraint filtering.
    
    def calculate_future_conflicts(self, state: Tuple[int, ...], from_row: int) -> int:
        """Calculate potential future conflicts for remaining rows"""
        conflicts = 0
        placed_queens = [(r, state[r]) for r in range(from_row) if state[r] != -1]
        
        # For each remaining row, count how many columns are blocked
        for row in range(from_row, BOARD_SIZE):
            blocked_cols = set()
            for r, c in placed_queens:
                # Column conflict
                blocked_cols.add(c)
                # Diagonal conflicts
                diag_offset = row - r
                if 0 <= c - diag_offset < BOARD_SIZE:
                    blocked_cols.add(c - diag_offset)
                if 0 <= c + diag_offset < BOARD_SIZE:
                    blocked_cols.add(c + diag_offset)
            
            available = BOARD_SIZE - len(blocked_cols)
            if available == 0:
                conflicts += 10  # Heavy penalty for impossible rows
            else:
                conflicts += max(0, 1 - available)  # Prefer rows with more options
        
        return conflicts
    
    # backtrack removed (no backtracking in either mode)
