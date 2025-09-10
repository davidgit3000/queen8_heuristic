// Constants
const BOARD_SIZE = 8;

// A* Search Algorithm Class
class StepByStepAStar {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.currentState = new Array(BOARD_SIZE).fill(-1);
        this.searchStack = []; // Stack for backtracking: [{state, row, triedColumns}]
        this.currentRow = 0;
        this.solved = false;
        this.stuck = false;
    }
    
    getValidColumns(state, row) {
        const validCols = [];
        for (let col = 0; col < BOARD_SIZE; col++) {
            const tempState = [...state];
            tempState[row] = col;
            
            let conflicts = false;
            for (let r = 0; r < row; r++) {
                if (tempState[r] === -1) continue;
                const c = tempState[r];
                
                // Check column conflict
                if (c === col) {
                    conflicts = true;
                    break;
                }
                
                // Check diagonal conflicts
                if (Math.abs(r - row) === Math.abs(c - col)) {
                    conflicts = true;
                    break;
                }
            }
            
            if (!conflicts) {
                validCols.push(col);
            }
        }
        return validCols;
    }
    
    nextStep() {
        if (this.solved) {
            return [this.currentState, "Already solved!", true];
        }
        
        if (this.stuck) {
            return [this.currentState, "Search failed - no solution found", true];
        }
        
        // If we've placed all queens, check if it's a valid solution
        if (this.currentRow >= BOARD_SIZE) {
            const h = this.attackingPairs(this.currentState);
            if (h === 0) {
                this.solved = true;
                return [this.currentState, `Solution found!`, true];
            } else {
                this.currentRow -= 1;
                return this.backtrack();
            }
        }
        
        // Get valid columns for current row
        const validCols = this.getValidColumns(this.currentState, this.currentRow);
        
        if (validCols.length === 0) {
            return this.backtrack();
        }
        
        // Choose the best column using heuristic
        const bestCol = this.chooseBestColumn(validCols);
        
        // Save current state for potential backtracking
        const triedCols = new Set([bestCol]);
        this.searchStack.push({
            state: [...this.currentState],
            row: this.currentRow,
            triedColumns: triedCols
        });
        
        // Place queen
        this.currentState[this.currentRow] = bestCol;
        
        const message = `Placed queen at row ${this.currentRow}, col ${bestCol}.`;
        this.currentRow += 1;
        
        return [this.currentState, message, false];
    }
    
    chooseBestColumn(validCols) {
        let bestCol = validCols[0];
        let bestH = Infinity;
        
        for (const col of validCols) {
            const tempState = [...this.currentState];
            tempState[this.currentRow] = col;
            
            const h = this.calculateFutureConflicts(tempState, this.currentRow + 1);
            
            if (h < bestH) {
                bestH = h;
                bestCol = col;
            }
        }
        
        return bestCol;
    }
    
    calculateFutureConflicts(state, fromRow) {
        let conflicts = 0;
        const placedQueens = [];
        
        for (let r = 0; r < fromRow; r++) {
            if (state[r] !== -1) {
                placedQueens.push([r, state[r]]);
            }
        }
        
        // For each remaining row, count how many columns are blocked
        for (let row = fromRow; row < BOARD_SIZE; row++) {
            const blockedCols = new Set();
            
            for (const [r, c] of placedQueens) {
                // Column conflict
                blockedCols.add(c);
                
                // Diagonal conflicts
                const diagOffset = row - r;
                if (c - diagOffset >= 0 && c - diagOffset < BOARD_SIZE) {
                    blockedCols.add(c - diagOffset);
                }
                if (c + diagOffset >= 0 && c + diagOffset < BOARD_SIZE) {
                    blockedCols.add(c + diagOffset);
                }
            }
            
            const available = BOARD_SIZE - blockedCols.size;
            if (available === 0) {
                conflicts += 10; // Heavy penalty for impossible rows
            } else {
                conflicts += Math.max(0, 1 - available); // Prefer rows with more options
            }
        }
        
        return conflicts;
    }
    
    backtrack() {
        while (this.searchStack.length > 0) {
            const {state: prevState, row: prevRow, triedColumns: triedCols} = this.searchStack.pop();
            
            const validCols = this.getValidColumns(prevState, prevRow);
            const untriedCols = validCols.filter(c => !triedCols.has(c));
            
            if (untriedCols.length > 0) {
                const bestCol = this.chooseBestColumn(untriedCols);
                triedCols.add(bestCol);
                this.searchStack.push({
                    state: prevState,
                    row: prevRow,
                    triedColumns: triedCols
                });
                
                // Place queen
                this.currentState = [...prevState];
                this.currentState[prevRow] = bestCol;
                this.currentRow = prevRow + 1;
                
                const message = `Backtracked to row ${prevRow}, trying col ${bestCol}.`;
                return [this.currentState, message, false];
            }
        }
        
        // No more options to try
        this.stuck = true;
        return [this.currentState, "Search failed - no solution exists", true];
    }
    
    attackingPairs(state) {
        const rows = [];
        const cols = [];
        
        for (let i = 0; i < state.length; i++) {
            if (state[i] !== -1) {
                rows.push(i);
                cols.push(state[i]);
            }
        }
        
        let pairs = 0;
        for (let i = 0; i < rows.length; i++) {
            const r1 = rows[i];
            const c1 = cols[i];
            
            for (let j = i + 1; j < rows.length; j++) {
                const r2 = rows[j];
                const c2 = cols[j];
                
                const sameCol = (c1 === c2);
                const sameDiag = Math.abs(r1 - r2) === Math.abs(c1 - c2);
                
                if (sameCol || sameDiag) {
                    pairs++;
                }
            }
        }
        
        return pairs;
    }
}

// GUI Class
class EightQueensGUI {
    constructor() {
        this.astarSearch = new StepByStepAStar();
        this.state = [...this.astarSearch.currentState];
        this.searchStarted = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.drawBoard();
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateMessage("Click 'Start' to begin the A* search algorithm.");
    }
    
    initializeElements() {
        this.startBtn = document.getElementById('start-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.restartBtn = document.getElementById('restart-btn');
        this.statusMessage = document.getElementById('status-message');
        this.heuristicDisplay = document.getElementById('heuristic-display');
        this.chessBoard = document.getElementById('chess-board');
        this.queenPositions = document.getElementById('queen-positions');
    }
    
    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.startSearch());
        this.nextBtn.addEventListener('click', () => this.nextStep());
        this.restartBtn.addEventListener('click', () => this.restart());
    }
    
    drawBoard() {
        this.chessBoard.innerHTML = '';
        
        // Create chess board cells
        for (let r = 0; r < BOARD_SIZE; r++) {
            for (let c = 0; c < BOARD_SIZE; c++) {
                const cell = document.createElement('div');
                cell.className = `chess-cell ${(r + c) % 2 === 0 ? 'light' : 'dark'}`;
                cell.dataset.row = r;
                cell.dataset.col = c;
                this.chessBoard.appendChild(cell);
            }
        }
        
        // Draw queens
        for (let r = 0; r < BOARD_SIZE; r++) {
            const c = this.state[r];
            if (c !== -1) {
                this.drawQueen(r, c);
            }
        }
        
        // Highlight current row (most recently placed queen)
        if (this.searchStarted && !this.astarSearch.solved) {
            let lastPlacedRow = -1;
            for (let r = 0; r < BOARD_SIZE; r++) {
                if (this.state[r] !== -1) {
                    lastPlacedRow = r;
                }
            }
            
            if (lastPlacedRow >= 0) {
                this.addOrangeHighlight(lastPlacedRow);
                // this.highlightRow(lastPlacedRow);
            }
        }
    }
    
    drawQueen(row, col) {
        const cells = this.chessBoard.children;
        const cellIndex = row * BOARD_SIZE + col;
        const cell = cells[cellIndex];
        
        const queen = document.createElement('div');
        queen.className = 'queen';
        queen.textContent = '♛';
        cell.appendChild(queen);
    }
    
    // highlightRow(row) {
    //     const highlight = document.createElement('div');
    //     highlight.className = 'row-highlight';
    //     highlight.style.top = `${row * 60 + 2}px`;
    //     highlight.style.height = '56px';
    //     this.chessBoard.appendChild(highlight);
    // }
    
    addOrangeHighlight(row) {
        const highlight = document.createElement('div');
        highlight.className = 'orange-highlight';
        highlight.style.top = `${row * 60}px`;
        this.chessBoard.appendChild(highlight);
    }
    
    startSearch() {
        this.searchStarted = true;
        this.startBtn.disabled = true;
        this.nextBtn.disabled = false;
        
        // Immediately perform the first step
        const [newState, message, isComplete] = this.astarSearch.nextStep();
        this.state = [...newState];
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.drawBoard();
        this.updateMessage(message);
        
        if (isComplete) {
            if (this.astarSearch.solved) {
                this.nextBtn.disabled = true;
                this.updateMessage("Solution found! All queens placed without conflicts.");
            } else {
                this.nextBtn.disabled = true;
                this.updateMessage("Search failed - no solution found.");
            }
        }
    }
    
    nextStep() {
        const [newState, message, isComplete] = this.astarSearch.nextStep();
        this.state = [...newState];
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.drawBoard();
        this.updateMessage(message);
        
        if (isComplete) {
            if (this.astarSearch.solved) {
                this.nextBtn.disabled = true;
                this.updateMessage("Solution found! All queens placed without conflicts.");
            } else {
                this.nextBtn.disabled = true;
                this.updateMessage("Search failed - no solution found.");
            }
        }
    }
    
    restart() {
        this.astarSearch.reset();
        this.state = [...this.astarSearch.currentState];
        this.searchStarted = false;
        this.startBtn.disabled = false;
        this.nextBtn.disabled = true;
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.drawBoard();
        this.updateMessage("Search reset. Click 'Start' to begin the A* algorithm.");
    }
    
    updateSidePanel() {
        this.queenPositions.innerHTML = '';
        
        for (let r = 0; r < BOARD_SIZE; r++) {
            const val = this.state[r];
            const text = val === -1 ? `Row ${r}: not placed` : `Row ${r}: column ${val}`;
            
            const div = document.createElement('div');
            div.className = 'queen-position';
            div.textContent = text;
            
            // Highlight current row
            let isHighlighted = false;
            if (this.searchStarted && !this.astarSearch.solved) {
                let lastPlacedRow = -1;
                for (let row = 0; row < BOARD_SIZE; row++) {
                    if (this.state[row] !== -1) {
                        lastPlacedRow = row;
                    }
                }
                isHighlighted = (r === lastPlacedRow && lastPlacedRow >= 0);
            }
            
            if (isHighlighted) {
                div.classList.add('highlighted');
            }
            
            this.queenPositions.appendChild(div);
        }
    }
    
    updateHeuristicDisplay() {
        const placedQueens = this.state.filter(c => c !== -1).length;
        this.heuristicDisplay.textContent = `Queens placed: ${placedQueens}/${BOARD_SIZE}`;
    }
    
    updateMessage(text) {
        this.statusMessage.textContent = text;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new EightQueensGUI();
});
