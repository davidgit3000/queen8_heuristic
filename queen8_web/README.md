# 8-Queens — Step-by-Step A* Search (Web Version)

A web-based implementation of the classic 8-Queens problem using A* search algorithm with step-by-step visualization.

## Overview

The 8-Queens problem is a classic constraint satisfaction problem where you must place 8 queens on a chessboard such that no two queens attack each other. This implementation uses the A* search algorithm with backtracking to find a solution while providing visual feedback for each step.

## Features

- **Interactive Step-by-Step Visualization**: Watch the algorithm place queens one by one
- **A* Search Algorithm**: Uses heuristic-guided search with backtracking
- **Real-time Highlighting**: Current queen placement highlighted with transparent overlay
- **Queen Position Tracking**: Left panel shows the position of each queen
- **Responsive Design**: Works on desktop and mobile devices
- **Clean Modern UI**: Dark theme with intuitive controls

## Files Structure

```
queen8_web/
├── index.html      # Main HTML structure
├── styles.css      # CSS styling and layout
├── script.js       # JavaScript A* algorithm and UI logic
└── README.md       # This file
```

## How to Run

1. **Clone or download** the files to your local machine
2. **Open `index.html`** in any modern web browser
3. **Click "Start"** to begin the search algorithm
4. **Click "Next Step"** to advance through each placement
5. **Click "Restart"** to reset and try again

No server setup required - runs entirely in the browser!

## How It Works

### Algorithm Details

1. **Constraint Satisfaction**: Only places queens in positions that don't conflict with existing queens
2. **Heuristic Guidance**: Uses `calculateFutureConflicts()` to choose the best column for each row
3. **Backtracking**: When no valid moves exist, backtracks to try alternative placements
4. **Step-by-Step Execution**: Each button click advances the algorithm by one step

### Visual Elements

- **Chess Board**: 8x8 grid with alternating light and dark squares
- **Queens**: Represented by crown symbols (♛) with white background circles
- **Row Highlighting**: Orange transparent overlay on the row with the most recent queen
- **Position Display**: Left panel shows "Row X: column Y" for each placed queen
- **Status Messages**: Bottom panel shows current algorithm action
- **Progress Counter**: Shows "Queens placed: X/8"

## Controls

- **Start**: Begin the A* search algorithm (places first queen immediately)
- **Next Step**: Advance to the next step in the search
- **Restart**: Reset the board and algorithm to start over

## Technical Implementation

### JavaScript Classes

- **`StepByStepAStar`**: Core algorithm implementation
  - `nextStep()`: Performs one step of the search
  - `getValidColumns()`: Finds valid positions for current row
  - `chooseBestColumn()`: Uses heuristic to select best option
  - `calculateFutureConflicts()`: Heuristic function for A* guidance
  - `backtrack()`: Handles backtracking when stuck

- **`EightQueensGUI`**: User interface management
  - `drawBoard()`: Renders the chess board and queens
  - `updateSidePanel()`: Updates position display
  - `addOrangeHighlight()`: Adds row highlighting

### CSS Features

- **Flexbox Layout**: Responsive design that centers content
- **CSS Grid**: Chess board implemented as 8x8 grid
- **Alpha Transparency**: `rgba()` colors for smooth highlighting effects
- **Responsive Design**: Adapts to different screen sizes

## Browser Compatibility

Works in all modern browsers that support:
- ES6 JavaScript (classes, arrow functions, destructuring)
- CSS Grid and Flexbox
- HTML5

Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Educational Value

This implementation demonstrates:
- **Search Algorithms**: A* search with heuristics
- **Constraint Satisfaction**: Only allowing valid moves
- **Backtracking**: Undoing choices when stuck
- **Web Development**: HTML/CSS/JavaScript integration
- **Algorithm Visualization**: Step-by-step problem solving

## Customization

Easy to modify:
- Change `BOARD_SIZE` constant for different N-Queens problems
- Adjust colors in CSS for different themes
- Modify heuristic function for different search strategies
- Add animation effects for smoother transitions

## License

Educational use - feel free to modify and learn from the code!

---

*Created as part of CS 4200 coursework - demonstrates A* search algorithm applied to the classic 8-Queens constraint satisfaction problem.*
