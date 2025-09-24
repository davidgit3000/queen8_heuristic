// Constants
const BOARD_SIZE = 8;

// A* Search Algorithm Class
class StepByStepAStar {
    constructor() {
        this.mode = 'deterministic'; // 'deterministic' | 'astar'
        this.reset();
    }
    
    reset() {
        this.currentState = new Array(BOARD_SIZE).fill(-1);
        if (this.mode === 'astar') {
            // Open list for A*: frontier of partial boards (no backtracking)
            // Each node: { state, row, g, h, f }
            const h0 = this.calculateFutureConflicts(this.currentState, 0);
            this.openList = [{ state: [...this.currentState], row: 0, g: 0, h: h0, f: h0 }];
        } else {
            // Deterministic minimal-steps solution for 8-Queens (one queen per row)
            // 0-indexed columns for rows 0..7; this is a known valid solution
            this.fixedSolution = [0, 4, 7, 5, 2, 6, 1, 3];
        }
        this.currentRow = 0; // for UI highlighting and placement
        this.solved = false;
        this.stuck = false;
        this.stepCount = 0;
    }
    
    setMode(mode) {
        if (mode !== 'deterministic' && mode !== 'astar') return;
        this.mode = mode;
        this.reset();
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

        // Increment step counter
        this.stepCount++;
        if (this.mode === 'deterministic') {
            // If all rows placed, validate and finish
            if (this.currentRow >= BOARD_SIZE) {
                const h = this.attackingPairs(this.currentState);
                if (h === 0) {
                    this.solved = true;
                    return [this.currentState, `Step ${this.stepCount}: Solution found!`, true];
                } else {
                    this.stuck = true;
                    return [this.currentState, "Unexpected conflict at full placement.", true];
                }
            }

            // Deterministic placement from a known valid solution
            const col = this.fixedSolution[this.currentRow];
            this.currentState[this.currentRow] = col;
            const message = `Step ${this.stepCount}: Placed queen at row ${this.currentRow}, col ${col}.`;
            this.currentRow += 1;
            
            // If this was the last placement, validate immediately and finish
            const done = (this.currentRow === BOARD_SIZE);
            if (done) {
                const h = this.attackingPairs(this.currentState);
                if (h === 0) {
                    this.solved = true;
                    return [this.currentState, `Step ${this.stepCount}: Solution found!`, true];
                } else {
                    this.stuck = true;
                    return [this.currentState, "Unexpected conflict at full placement.", true];
                }
            }

            return [this.currentState, message, false];
        } else {
            // A* frontier (no backtracking)
            if (this.openList.length === 0) {
                this.stuck = true;
                return [this.currentState, "Frontier exhausted. No solution found (no backtracking).", true];
            }

            // Select node with smallest f from open list
            this.openList.sort((a, b) => a.f - b.f);
            const node = this.openList.shift();

            // Update current state for visualization
            this.currentState = [...node.state];
            this.currentRow = node.row;

            // Goal test
            if (node.row >= BOARD_SIZE) {
                if (this.attackingPairs(node.state) === 0) {
                    this.solved = true;
                    return [this.currentState, `Step ${this.stepCount}: Solution found!`, true];
                }
            }

            // Expand children
            const validCols = this.getValidColumns(node.state, node.row);
            if (validCols.length === 0) {
                return [this.currentState, `Step ${this.stepCount}: Dead end at row ${node.row}. Exploring other candidates...`, false];
            }

            const children = [];
            for (const col of validCols) {
                const childState = [...node.state];
                childState[node.row] = col;
                const g = node.row + 1;
                const h = this.calculateFutureConflicts(childState, node.row + 1);
                const f = g + h;
                const child = { state: childState, row: node.row + 1, g, h, f };
                children.push(child);
                this.openList.push(child);
            }

            children.sort((a, b) => a.f - b.f);
            const bestChild = children[0];
            this.currentState = [...bestChild.state];
            this.currentRow = bestChild.row;
            const placedCol = bestChild.state[bestChild.row - 1];
            const message = `Step ${this.stepCount}: Expanded row ${node.row}, placed queen at col ${placedCol}. Open list size: ${this.openList.length}`;
            return [this.currentState, message, false];
        }
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
    
    // Heuristic function to count attacking pairs
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
        this.simulationTimer = null;
        this.isPaused = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.drawBoard();
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateStepCounter();
        this.updateModeIndicator();
        this.updateMessage("Click 'Start' to begin the A* search algorithm.");
    }
    
    initializeElements() {
        this.startBtn = document.getElementById('start-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.restartBtn = document.getElementById('restart-btn');
        this.runSimBtn = document.getElementById('run-sim-btn');
        this.modeSelect = document.getElementById('mode-select');
        this.pauseResumeBtn = document.getElementById('pause-resume-btn');
        this.speedSelect = document.getElementById('speed-select');
        this.statusMessage = document.getElementById('status-message');
        this.modeIndicator = document.getElementById('mode-indicator');
        this.heuristicDisplay = document.getElementById('heuristic-display');
        this.stepCounter = document.getElementById('step-counter');
        this.chessBoard = document.getElementById('chess-board');
        this.queenPositions = document.getElementById('queen-positions');
    }
    
    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.startSearch());
        this.nextBtn.addEventListener('click', () => this.nextStep());
        this.restartBtn.addEventListener('click', () => this.restart());
        if (this.runSimBtn) {
            this.runSimBtn.addEventListener('click', () => this.runSimulation());
        }
        if (this.pauseResumeBtn) {
            this.pauseResumeBtn.addEventListener('click', () => this.togglePauseResume());
        }
        if (this.modeSelect) {
            this.modeSelect.addEventListener('change', () => this.onModeChange());
        }
        if (this.speedSelect) {
            this.speedSelect.addEventListener('change', () => this.onSpeedChange());
        }
    }

    onModeChange() {
        const mode = this.modeSelect.value === 'astar' ? 'astar' : 'deterministic';
        // Apply mode to algorithm (this will reset internal state)
        this.astarSearch.setMode(mode);
        // Sync local state and UI
        this.state = [...this.astarSearch.currentState];
        this.searchStarted = false;
        this.startBtn.disabled = false;
        this.nextBtn.disabled = true;
        if (this.pauseResumeBtn) {
            this.pauseResumeBtn.disabled = true;
            this.pauseResumeBtn.textContent = 'Pause';
        }
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateStepCounter();
        this.drawBoard();
        const modeLabel = mode === 'deterministic' ? 'Deterministic (8 steps)' : 'A* Frontier (no backtracking)';
        this.updateMessage(`Mode changed to ${modeLabel}. Click 'Start' to begin.`);
        this.updateModeIndicator();
    }

    updateModeIndicator() {
        if (!this.modeIndicator) return;
        const mode = this.astarSearch.mode;
        const modeLabel = mode === 'deterministic' ? 'Deterministic (8 steps)' : 'A* Frontier (no backtracking)';
        this.modeIndicator.textContent = `Mode: ${modeLabel}`;
    }

    getSimulationDelay() {
        if (!this.speedSelect) return 150;
        const v = parseInt(this.speedSelect.value, 10);
        return Number.isFinite(v) ? v : 150;
    }

    onSpeedChange() {
        // If simulation is running and not paused, restart the interval with new speed
        if (this.simulationTimer && !this.isPaused) {
            this.stopSimulationTimer();
            this.startSimulationTimer();
        }
    }

    startSimulationTimer() {
        const delay = this.getSimulationDelay();
        this.simulationTimer = setInterval(() => {
            const [newState, message, isComplete] = this.astarSearch.nextStep();
            this.state = [...newState];
            this.updateSidePanel();
            this.updateHeuristicDisplay();
            this.updateStepCounter();
            this.drawBoard();
            this.updateMessage(message);

            if (isComplete) {
                this.stopSimulationTimer();
                this.nextBtn.disabled = true;
                if (this.runSimBtn) {
                    this.runSimBtn.disabled = false;
                    this.runSimBtn.textContent = 'Run simulation';
                }
                if (this.modeSelect) {
                    this.modeSelect.disabled = false;
                }
                if (this.pauseResumeBtn) {
                    this.pauseResumeBtn.disabled = true;
                    this.pauseResumeBtn.textContent = 'Pause';
                }
                // Ensure final message clarity
                if (this.astarSearch.solved) {
                    this.updateMessage('Solution found! All queens placed without conflicts.');
                } else {
                    this.updateMessage('Search failed - no solution found.');
                }
            }
        }, delay);
    }

    stopSimulationTimer() {
        if (this.simulationTimer) {
            clearInterval(this.simulationTimer);
            this.simulationTimer = null;
        }
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
        if (this.modeSelect) {
            this.modeSelect.disabled = true; // disable mode switching during manual run
        }
        
        // Immediately perform the first step
        const [newState, message, isComplete] = this.astarSearch.nextStep();
        this.state = [...newState];
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateStepCounter();
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
            if (this.modeSelect) {
                this.modeSelect.disabled = false;
            }
        }
    }
    
    nextStep() {
        const [newState, message, isComplete] = this.astarSearch.nextStep();
        this.state = [...newState];
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateStepCounter();
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
            if (this.modeSelect) {
                this.modeSelect.disabled = false;
            }
        }
    }
    
    restart() {
        this.astarSearch.reset();
        this.state = [...this.astarSearch.currentState];
        this.searchStarted = false;
        this.startBtn.disabled = false;
        this.nextBtn.disabled = true;
        this.stopSimulationTimer();
        this.isPaused = false;
        if (this.runSimBtn) {
            this.runSimBtn.disabled = false;
            this.runSimBtn.textContent = 'Run simulation';
        }
        if (this.modeSelect) {
            this.modeSelect.disabled = false;
        }
        if (this.pauseResumeBtn) {
            this.pauseResumeBtn.disabled = true;
            this.pauseResumeBtn.textContent = 'Pause';
        }
        
        this.updateSidePanel();
        this.updateHeuristicDisplay();
        this.updateStepCounter();
        this.drawBoard();
        this.updateModeIndicator();
        this.updateMessage("Search reset. Click 'Start' to begin the A* algorithm.");
    }

    runSimulation() {
        // Ensure mode is A* frontier
        if (this.modeSelect && this.modeSelect.value !== 'astar') {
            this.modeSelect.value = 'astar';
            this.onModeChange();
        } else {
            // If already in astar mode, reset to fresh state if not started
            if (!this.searchStarted) {
                this.astarSearch.setMode('astar');
                this.state = [...this.astarSearch.currentState];
            }
        }

        this.searchStarted = true;
        this.startBtn.disabled = true;
        this.nextBtn.disabled = true;
        if (this.runSimBtn) {
            this.runSimBtn.disabled = true;
            this.runSimBtn.textContent = 'Running...';
        }
        if (this.modeSelect) {
            this.modeSelect.disabled = true;
        }
        if (this.pauseResumeBtn) {
            this.pauseResumeBtn.disabled = false;
            this.pauseResumeBtn.textContent = 'Pause';
        }
        this.isPaused = false;
        this.stopSimulationTimer();
        this.startSimulationTimer();
    }

    togglePauseResume() {
        if (!this.pauseResumeBtn) return;
        if (!this.simulationTimer && !this.isPaused) return; // nothing to pause
        if (this.isPaused) {
            // Resume
            this.isPaused = false;
            this.pauseResumeBtn.textContent = 'Pause';
            this.startSimulationTimer();
        } else {
            // Pause
            this.isPaused = true;
            this.pauseResumeBtn.textContent = 'Resume';
            this.stopSimulationTimer();
        }
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
    
    updateStepCounter() {
        this.stepCounter.textContent = `Algorithm steps: ${this.astarSearch.stepCount}`;
    }
    
    updateMessage(text) {
        this.statusMessage.textContent = text;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new EightQueensGUI();
});
