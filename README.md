# AI_UCS_Astar

## Overview
AI_UCS_Astar is a Python-based N-Puzzle solver implementing **Uniform Cost Search (UCS)** and **A Search Algorithm (A\*)** to find the optimal solution. The project includes a graphical user interface (GUI) using `tkinter` for user-friendly interaction.

## Features
- **Graphical User Interface (GUI)**: Users can input their puzzle configuration through an intuitive GUI.
- **Uniform Cost Search (UCS)**: Explores the shortest path by expanding the least-cost node.
- **A Search (A\*)**: Uses the inversion distance heuristic to find the optimal solution efficiently.
- **Memory Usage Tracking**: Monitors memory consumption during execution.
- **Execution Time Measurement**: Displays the time taken for solving the puzzle.
- **Step-by-Step Visualization**: Animates the solution process.

## Installation

### Prerequisites
Ensure you have Python installed (version 3.6+ recommended). Install dependencies:
```bash
pip install psutil
```

## How to Use
1. Run the program:
```bash
python main.py
```

2. Enter the size of the puzzle (e.g., 3 for a 3x3 puzzle).

3. Input the board configuration using comma-separated values (e.g., `1,2,3,4,5,6,7,8,0`).

4. Choose the algorithm:
  - **Uniform Cost Search (UCS)**
  - **A Search (A\*)**

5. View the solution, including execution time, memory usage, and step-by-step moves.

## Algorithms Used
### Uniform Cost Search (UCS)
- Expands the least-cost node first.
- Guarantees optimal solution if all actions have non-negative costs.

### A Search (A\*)
- Uses `f(n) = g(n) + h(n)` where:
  - `g(n)`: Cost from the initial state to node `n`
  - `h(n)`: Inversion distance heuristic estimating the cost to the goal.
- Efficiently finds the shortest path.

## Example
**Input**

```makefile
Size: 3
Board: 1,2,3,4,5,6,7,0,8
```

**Output**
```yaml
Solution Found!
Number of moves: X
Time taken: Y ms
Memory usage: Z MB
```

## License
This project is licensed under the `MIT License`.
