# 8-Queens — Step-by-Step A* Search (Python Version)

A Python implementation of the classic 8-Queens problem using A* search algorithm with Tkinter GUI visualization.

## Overview

This is the original Python implementation of the 8-Queens constraint satisfaction problem. It uses the A* search algorithm with backtracking and provides a step-by-step visual interface built with Tkinter.

## Features

- **Tkinter GUI Interface**: Native desktop application with dark theme
- **Step-by-Step Visualization**: Watch each queen placement in real-time
- **A* Search Algorithm**: Heuristic-guided search with intelligent backtracking
- **Row Highlighting**: Red border highlights the current queen being placed
- **Queen Position Panel**: Left sidebar shows placement status for each row
- **Interactive Controls**: Start, Next Step, and Restart buttons

## Files

- `queen8_algorithm.py` - Core A* search algorithm implementation
- `queen8_gui.py` - Tkinter GUI interface and visualization
- `README.md` - This documentation file

## Requirements

- Python 3.7+
- Tkinter (usually included with Python)
- No additional dependencies required

## How to Run

1. **Ensure Python is installed** on your system
2. **Navigate to the queen8_py directory**
3. **Run the GUI application**:
   ```bash
   python queen8_gui.py
   ```
4. **Use the interface**:
   - Click "Start" to begin the search
   - Click "Next Step" to advance through each placement
   - Click "Restart" to reset and try again

## Algorithm Details

### Core Components

**`StepByStepAStar` Class** (`queen8_algorithm.py`):
- `next_step()`: Performs one iteration of the search
- `get_valid_columns()`: Finds conflict-free positions for current row
- `choose_best_column()`: Uses heuristic to select optimal placement
- `calculate_future_conflicts()`: Heuristic function for A* guidance
- `backtrack()`: Handles dead-end situations with intelligent backtracking
- `attacking_pairs()`: Counts conflicts between placed queens

**`EightQueensGUI` Class** (`queen8_gui.py`):
- `draw_board()`: Renders 8x8 chessboard with queens
- `draw_queen()`: Places queen symbols with white background circles
- `update_side_panel()`: Updates position display with highlighting
- `start_search()`: Initiates algorithm and places first queen immediately
- `next_step()`: Advances algorithm by one step
- `restart()`: Resets board and algorithm state

### Visual Elements

- **Chess Board**: 480x480 pixel canvas with alternating colored squares
- **Queens**: Crown symbols (♛) with white circular backgrounds
- **Row Highlighting**: Red border around current queen's row
- **Status Messages**: Algorithm progress and completion notifications
- **Position Display**: "Row X: column Y" format with orange highlighting for current row

## Technical Implementation

### Constants
```python
BOARD_SIZE = 8          # 8x8 chessboard
CELL = 60              # 60px per square
COL_LIGHT = "#d4b896"  # Light brown squares
COL_DARK = "#2f6f62"   # Teal squares
```

### Key Features
- **Constraint Satisfaction**: Only allows valid queen placements
- **Heuristic Search**: Chooses placements that minimize future conflicts
- **Immediate Feedback**: Queens appear instantly when placed
- **Synchronized Highlighting**: Board and text panel highlight same row

## Customization Options

- **Board Size**: Change `BOARD_SIZE` for different N-Queens problems
- **Colors**: Modify color constants for different themes
- **Cell Size**: Adjust `CELL` constant for larger/smaller board
- **Heuristic Function**: Modify `calculate_future_conflicts()` for different strategies

## Educational Value

Demonstrates key computer science concepts:
- **Search Algorithms**: A* heuristic search implementation
- **Constraint Satisfaction Problems**: Valid move generation
- **Backtracking**: Systematic exploration with undo capability
- **GUI Programming**: Event-driven interface design
- **Algorithm Visualization**: Step-by-step problem solving

## Performance

- **Time Complexity**: O(N!) worst case, but heuristic guidance significantly improves average performance
- **Space Complexity**: O(N) for state representation and search stack
- **Typical Solution Time**: Finds solution in 10-50 steps for 8-Queens

## Troubleshooting

**Common Issues**:
- **Tkinter not found**: Install Python with Tkinter support
- **Font issues**: Queen symbol may not display on some systems
- **Performance**: Large board sizes (N > 12) may be slow

**Solutions**:
- Use Python from python.org (includes Tkinter)
- Install system fonts that support Unicode symbols
- Consider web version for better performance on large boards

---

*Part of CS 4200 coursework demonstrating A* search algorithm applied to constraint satisfaction problems.*
