# 8-Queens Problem — A* Search Implementation

Two complete implementations of the classic 8-Queens constraint satisfaction problem using A* search algorithm with step-by-step visualization.

## Project Overview

The 8-Queens problem challenges you to place 8 queens on a chessboard such that no two queens can attack each other (no shared rows, columns, or diagonals). This repository contains two different implementations of an A* search solution with interactive visualizations.

## Demo Video
[![Video](https://img.youtube.com/vi/TYTDRmb7u0w/maxresdefault.jpg)](https://www.youtube.com/watch?v=TYTDRmb7u0w)

## Implementations

### 🐍 Python Version (`queen8_py/`)
- **Desktop GUI** built with Tkinter
- **Native performance** with Python algorithms
- **Dark theme interface** with red border highlighting
- **Immediate visual feedback** for each queen placement

### 🌐 Web Version (`queen8_web/`)
- **Browser-based interface** using HTML/CSS/JavaScript
- **Cross-platform compatibility** - runs anywhere
- **Responsive design** that works on mobile and desktop
- **Alpha-transparent highlighting** with modern UI

## Quick Start

### Python Version
```bash
cd queen8_py/
python queen8_gui.py
```

### Web Version
```bash
cd queen8_web/
# Open index.html in any web browser
```

## Features Comparison

| Feature | Python Version | Web Version |
|---------|---------------|-------------|
| **Platform** | Desktop (Windows/Mac/Linux) | Any browser |
| **Dependencies** | Python 3.7+ + Tkinter | None |
| **Performance** | Native Python speed | JavaScript engine |
| **UI Theme** | Dark with red highlights | Dark with orange highlights |
| **Transparency** | Limited (stipple patterns) | Full alpha transparency |
| **Responsiveness** | Fixed window size | Responsive design |
| **Installation** | Python required | No installation |

## Algorithm Details

Both implementations use the same core A* search algorithm:

### Search Strategy
1. **Constraint Satisfaction**: Only places queens in conflict-free positions
2. **Heuristic Guidance**: Uses `calculateFutureConflicts()` to choose optimal placements
3. **Intelligent Backtracking**: Systematically explores alternatives when stuck
4. **Step-by-Step Execution**: User controls algorithm progression

### Key Components
- **State Representation**: Array where `state[row] = column` (-1 if empty)
- **Conflict Detection**: Checks column and diagonal conflicts
- **Heuristic Function**: Counts blocked positions in future rows
- **Search Stack**: Maintains backtracking information

## Educational Value

This project demonstrates:
- **Search Algorithms**: A* heuristic search implementation
- **Constraint Satisfaction Problems**: Systematic constraint handling
- **Backtracking Techniques**: Intelligent exploration with undo
- **Algorithm Visualization**: Step-by-step problem solving
- **Cross-Platform Development**: Same algorithm, different interfaces

## File Structure

```
├── README.md                    # This overview file
├── queen8_py/                   # Python implementation
│   ├── queen8_algorithm.py      # Core A* search algorithm
│   ├── queen8_gui.py           # Tkinter GUI interface
│   └── README.md               # Python-specific documentation
└── queen8_web/                 # Web implementation
    ├── index.html              # HTML structure
    ├── styles.css              # CSS styling
    ├── script.js               # JavaScript algorithm & UI
    └── README.md               # Web-specific documentation
```

## Usage Instructions

### Common Controls (Both Versions)
- **Start**: Begin A* search (places first queen immediately)
- **Next Step**: Advance algorithm by one step
- **Restart**: Reset board and algorithm state

### Visual Elements
- **Chess Board**: 8x8 grid with alternating light/dark squares
- **Queens**: Crown symbols (♛) with background circles
- **Row Highlighting**: Colored overlay on current queen's row
- **Position Panel**: Shows "Row X: column Y" for each placed queen
- **Status Messages**: Algorithm progress and completion notifications
- **Progress Counter**: "Queens placed: X/8"

## Technical Implementation

### Algorithm Complexity
- **Time**: O(N!) worst case, significantly improved by heuristics
- **Space**: O(N) for state and search stack
- **Typical Performance**: Solves 8-Queens in 10-50 steps

### Customization Options
- Change `BOARD_SIZE` for different N-Queens problems
- Modify heuristic functions for alternative search strategies
- Adjust visual themes and colors
- Add animation effects (web version)

## Browser Compatibility (Web Version)

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Requires ES6 JavaScript support (classes, arrow functions, destructuring).

## Development Notes

### Python Version Advantages
- **Performance**: Native Python execution
- **Debugging**: Full IDE support and debugging tools
- **Libraries**: Access to Python ecosystem
- **Offline**: No internet connection required

### Web Version Advantages
- **Accessibility**: Runs on any device with a browser
- **Sharing**: Easy to share via URL or hosting
- **Modern UI**: CSS3 features like alpha transparency
- **No Installation**: Zero setup required

## Future Enhancements

Potential improvements for both versions:
- **Animation**: Smooth transitions between steps
- **Multiple Solutions**: Find and display all possible solutions
- **Performance Metrics**: Show search statistics and timing
- **Different Algorithms**: Compare A* with other search methods
- **Larger Boards**: Support for N > 8 queens
- **Solution Export**: Save/load board configurations

## License

Educational use - part of CS 4200 coursework demonstrating search algorithms and constraint satisfaction techniques.

---

**Course**: CS 4200 - Artificial Intelligence  
**Assignment**: A* Search Algorithm Implementation  
**Topic**: Constraint Satisfaction Problems (8-Queens)
