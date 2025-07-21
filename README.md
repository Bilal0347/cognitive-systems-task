# Sliding Puzzle Solver

A Python implementation that solves 8-puzzle (3x3 sliding block puzzle) using multiple search algorithms and compares their performance.

## Overview

This project implements and compares two different search algorithms for solving the classic 8-puzzle:
- **Depth-First Search (DFS)** with depth limiting
- **A* Search** with Manhattan distance heuristic

The solver provides detailed performance metrics and visualizes the optimal solution path.

## Features

- **Solvability Check**: Automatically verifies if a puzzle configuration is solvable
- **Multiple Algorithms**: Compare DFS and A* search performance
- **Performance Metrics**: Tracks nodes expanded, memory usage, and execution time
- **Solution Visualization**: Shows step-by-step solution path
- **Manhattan Heuristic**: Efficient A* implementation with admissible heuristic

## Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Running the Solver

```bash
python main.py
```

## How It Works

### Puzzle Representation
- 3x3 grid with numbers 1-8 and one empty space (represented as 0)
- Goal: Arrange numbers in ascending order with empty space in bottom-right

### Default Configuration
**Start State:**
```
8 7 6
5 4 3
2 1  
```

**Goal State:**
```
1 2 3
4 5 6
7 8  
```

### Algorithms

#### Depth-First Search (DFS)
- Explores paths deeply before backtracking
- Uses depth limiting (max 50 moves) to prevent infinite loops
- Memory efficient but not optimal

#### A* Search
- Uses Manhattan distance heuristic for informed search
- Guarantees optimal solution
- More memory intensive but finds shortest path

### Manhattan Distance Heuristic
Calculates the sum of distances each tile needs to move to reach its target position, ignoring obstacles. This is an admissible heuristic that never overestimates the actual cost.

## Sample Output

```
SLIDING BLOCK PUZZLE SOLVER
==================================================
Puzzle is solvable - proceeding with search algorithms...

==================================================
PUZZLE CONFIGURATION:
==================================================

Start configuration:
[8, 7, 6]
[5, 4, 3]
[2, 1, ' ']

Target configuration:
[1, 2, 3]
[4, 5, 6]
[7, 8, ' ']

==================================================
RUNNING: DEPTH-FIRST SEARCH
==================================================

SUCCESS! Solution found!

PERFORMANCE METRICS:
   Nodes expanded: 2847
   Maximum memory usage: 1523 nodes
   Moves in solution: 26
   Time taken: 0.0234 seconds

==================================================
RUNNING: A* SEARCH
==================================================

SUCCESS! Solution found!

PERFORMANCE METRICS:
   Nodes expanded: 456
   Maximum memory usage: 298 nodes
   Moves in solution: 26
   Time taken: 0.0156 seconds

============================================================
FINAL COMPARISON
============================================================

Algorithm            Nodes      Memory     Moves    Time      
-----------------------------------------------------------------
Depth-First Search   2847       1523       26       0.0234s
A* Search           456        298        26       0.0156s
```

## Customization

### Changing Initial Configuration
Modify the `start_board` in the `run_comparison()` function:

```python
start_board = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]  # 0 represents empty space
]
```

### Adjusting Depth Limit
Change the `max_depth` parameter in DFS:

```python
depth_first_search(start_state, target_board, max_depth=100)
```

## Code Structure

- `PuzzleState`: Represents a puzzle configuration with board state and metadata
- `manhattan_heuristic()`: Calculates Manhattan distance for A* search
- `depth_first_search()`: Implements DFS with depth limiting
- `a_star_search()`: Implements A* algorithm with priority queue
- `is_solvable()`: Checks puzzle solvability using inversion count
- `print_solution_path()`: Visualizes the solution sequence

## Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Optimality |
|-----------|----------------|------------------|------------|
| DFS | O(b^d) | O(bd) | No |
| A* | O(b^d) | O(b^d) | Yes* |

*Optimal when using admissible heuristic

## Contributing

Contributions are welcome! Here are some ideas for improvements:
- Add more heuristics (Linear Conflict, Pattern Database)
- Implement additional search algorithms (BFS, IDA*)
- Add GUI interface
- Support for larger puzzle sizes (4x4, 5x5)
- Performance optimizations

## License

This project is open source and available under the [MIT License](LICENSE).

## References

- [8-puzzle on Wikipedia](https://en.wikipedia.org/wiki/15_puzzle)
- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Manhattan Distance Heuristic](https://en.wikipedia.org/wiki/Taxicab_geometry)

---
If you find this project helpful, please give it a star!
