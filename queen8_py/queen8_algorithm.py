import heapq
from typing import List, Tuple, Dict, Set

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
        self.reset()
    
    def reset(self):
        """Reset the search to start from beginning"""
        self.current_state = tuple([-1] * BOARD_SIZE)
        self.search_stack = []  # Stack for backtracking: [(state, row, tried_columns)]
        self.current_row = 0
        self.solved = False
        self.stuck = False
    
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
        """Perform one step of the A* search. Returns (new_state, message, is_complete)"""
        if self.solved:
            return self.current_state, "Already solved!", True
        
        if self.stuck:
            return self.current_state, "Search failed - no solution found", True
        
        # If we've placed all queens, check if it's a valid solution
        if self.current_row >= BOARD_SIZE:
            h = attacking_pairs(self.current_state)
            if h == 0:
                self.solved = True
                return self.current_state, f"Solution found! h(n) = {h}", True
            else:
                # This shouldn't happen with our constraint checking, but just in case
                self.current_row -= 1
                return self.backtrack()
        
        # Get valid columns for current row
        valid_cols = self.get_valid_columns(self.current_state, self.current_row)
        
        if not valid_cols:
            # No valid moves, need to backtrack
            return self.backtrack()
        
        # Choose the best column using heuristic (A* approach)
        best_col = self.choose_best_column(valid_cols)
        
        # Save current state for potential backtracking
        tried_cols = {best_col}
        self.search_stack.append((self.current_state, self.current_row, tried_cols))
        
        # Place queen
        new_state = list(self.current_state)
        new_state[self.current_row] = best_col
        self.current_state = tuple(new_state)
        
        message = f"Placed queen at row {self.current_row}, col {best_col}. h(n) = {attacking_pairs(self.current_state)}"
        self.current_row += 1
        
        return self.current_state, message, False
    
    def choose_best_column(self, valid_cols: List[int]) -> int:
        """Choose the best column using A* heuristic (lowest h value)"""
        best_col = valid_cols[0]
        best_h = float('inf')
        
        for col in valid_cols:
            # Create temporary state
            temp_state = list(self.current_state)
            temp_state[self.current_row] = col
            
            # Calculate heuristic (future conflicts)
            h = self.calculate_future_conflicts(tuple(temp_state), self.current_row + 1)
            
            if h < best_h:
                best_h = h
                best_col = col
        
        return best_col
    
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
    
    def backtrack(self) -> Tuple[Tuple[int, ...], str, bool]:
        """Backtrack to previous state and try next option"""
        while self.search_stack:
            prev_state, prev_row, tried_cols = self.search_stack.pop()
            
            # Get valid columns for this row
            valid_cols = self.get_valid_columns(prev_state, prev_row)
            untried_cols = [c for c in valid_cols if c not in tried_cols]
            
            if untried_cols:
                # Found an untried option
                best_col = self.choose_best_column(untried_cols)
                tried_cols.add(best_col)
                self.search_stack.append((prev_state, prev_row, tried_cols))
                
                # Place queen
                new_state = list(prev_state)
                new_state[prev_row] = best_col
                self.current_state = tuple(new_state)
                self.current_row = prev_row + 1
                
                message = f"Backtracked to row {prev_row}, trying col {best_col}. h(n) = {attacking_pairs(self.current_state)}"
                return self.current_state, message, False
        
        # No more options to try
        self.stuck = True
        return self.current_state, "Search failed - no solution exists", True
