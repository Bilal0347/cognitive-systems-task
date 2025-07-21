import heapq
import copy
import time


class PuzzleState:
    def __init__(self, board, empty_pos, moves=0, parent=None, move_description=""):
        self.board = board
        self.empty_pos = empty_pos
        self.moves = moves
        self.parent = parent
        self.move_description = move_description
        self.g_cost = moves
        self.h_cost = 0
        self.f_cost = 0

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __lt__(self, other):
        return self.f_cost < other.f_cost or (self.f_cost == other.f_cost and self.h_cost < other.h_cost)

    def get_neighbors(self):
        """Generate all possible next states by sliding blocks into empty space."""
        neighbors = []
        empty_row, empty_col = self.empty_pos

        directions = [
            (-1, 0, "Move block down"),
            (1, 0, "Move block up"),
            (0, -1, "Move block right"),
            (0, 1, "Move block left")
        ]

        for dr, dc, desc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc

            # Check bounds
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = copy.deepcopy(self.board)
                new_board[empty_row][empty_col] = new_board[new_row][new_col]
                new_board[new_row][new_col] = 0

                new_state = PuzzleState(
                    new_board,
                    (new_row, new_col),
                    self.moves + 1,
                    self,
                    f"{desc} ({new_board[empty_row][empty_col]})"
                )
                neighbors.append(new_state)

        return neighbors

    def is_goal(self, target_board):
        return self.board == target_board

    def print_board(self):
        for row in self.board:
            print([x if x != 0 else ' ' for x in row])
        print()


def manhattan_heuristic(board, target_board):
    """Calculate Manhattan distance heuristic."""
    distance = 0
    target_positions = {}

    # Map target positions
    for i in range(3):
        for j in range(3):
            if target_board[i][j] != 0:
                target_positions[target_board[i][j]] = (i, j)

    # Calculate Manhattan distance for each tile
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0:
                target_pos = target_positions[board[i][j]]
                distance += abs(i - target_pos[0]) + abs(j - target_pos[1])

    return distance


def depth_first_search(start_state, target_board, max_depth=50):
    stack = [start_state]
    visited = set()
    nodes_expanded = 0
    max_memory = 1

    while stack:
        current_state = stack.pop()

        # Skip if too deep or already visited
        if current_state.moves > max_depth or hash(current_state) in visited:
            continue

        visited.add(hash(current_state))
        nodes_expanded += 1

        # Check goal
        if current_state.is_goal(target_board):
            return current_state, nodes_expanded, max_memory, current_state.moves

        # Add unvisited neighbors
        for neighbor in current_state.get_neighbors():
            if hash(neighbor) not in visited:
                stack.append(neighbor)
                max_memory = max(max_memory, len(stack) + len(visited))

    return None, nodes_expanded, max_memory, -1


def a_star_search(start_state, target_board):
    start_state.h_cost = manhattan_heuristic(start_state.board, target_board)
    start_state.f_cost = start_state.g_cost + start_state.h_cost

    open_list = [start_state]
    closed_set = set()
    nodes_expanded = 0
    max_memory = 1
    g_costs = {hash(start_state): start_state.g_cost}

    while open_list:
        current_state = heapq.heappop(open_list)

        # Skip if already processed
        if current_state in closed_set:
            continue

        closed_set.add(current_state)
        nodes_expanded += 1

        # Check goal
        if current_state.is_goal(target_board):
            return current_state, nodes_expanded, max_memory, current_state.moves

        for neighbor in current_state.get_neighbors():
            # Skip if already processed
            if neighbor in closed_set:
                continue

            neighbor.g_cost = current_state.g_cost + 1
            neighbor.h_cost = manhattan_heuristic(neighbor.board, target_board)
            neighbor.f_cost = neighbor.g_cost + neighbor.h_cost

            neighbor_hash = hash(neighbor)
            # Skip if we found a better path before
            if neighbor_hash in g_costs and g_costs[neighbor_hash] <= neighbor.g_cost:
                continue

            g_costs[neighbor_hash] = neighbor.g_cost
            heapq.heappush(open_list, neighbor)
            max_memory = max(max_memory, len(open_list) + len(closed_set))

    return None, nodes_expanded, max_memory, -1


def print_solution_path(solution_state):
    """Print the sequence of moves to reach the solution."""
    path = []
    current = solution_state

    while current:
        path.append(current)
        current = current.parent

    path.reverse()

    print("\n📋 Solution path:")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        if i > 0:
            print(f"Move: {state.move_description}")
        state.print_board()

    return len(path) - 1


def is_solvable(board):
    """Check if puzzle is solvable using inversion count."""
    # Flatten board and remove empty space
    tiles = [tile for row in board for tile in row if tile != 0]

    # Count inversions
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    return inversions % 2 == 0


def run_algorithm(name, algorithm_func):
    """Run a single algorithm and return results."""
    print(f"\n{'=' * 50}")
    print(f"RUNNING: {name.upper()}")
    print("=" * 50)

    start_time = time.time()
    solution, nodes_expanded, max_memory, moves = algorithm_func()
    end_time = time.time()

    result = {
        'algorithm': name,
        'nodes_expanded': nodes_expanded,
        'max_memory': max_memory,
        'moves': moves,
        'time': end_time - start_time,
        'solution': solution
    }

    if solution:
        print(f"\n✅ SUCCESS! Solution found!")
        print(f"\n📊 PERFORMANCE METRICS:")
        print(f"   🔢 Nodes expanded: {nodes_expanded}")
        print(f"   🧠 Maximum memory usage: {max_memory} nodes")
        print(f"   🎯 Moves in solution: {moves}")
        print(f"   ⏱️  Time taken: {end_time - start_time:.4f} seconds")
    else:
        print(f"\n❌ No solution found within depth limit")
        print(f"📊 Search Statistics:")
        print(f"   🔢 Nodes expanded: {nodes_expanded}")
        print(f"   🧠 Maximum memory usage: {max_memory} nodes")
        print(f"   ⏱️  Time taken: {end_time - start_time:.4f} seconds")

    return result


def print_comparison(results):
    """Print final comparison of algorithms."""
    print(f"\n{'=' * 60}")
    print("🏆 FINAL COMPARISON")
    print(f"{'=' * 60}")

    print(f"\n{'Algorithm':<20} {'Nodes':<10} {'Memory':<10} {'Moves':<8} {'Time':<10}")
    print("-" * 65)

    for result in results:
        print(f"{result['algorithm']:<20} {result['nodes_expanded']:<10} "
              f"{result['max_memory']:<10} {result['moves']:<8} "
              f"{result['time']:.4f}s")

    # Show optimal solution path
    optimal_result = min(results, key=lambda x: x['moves'] if x['moves'] > 0 else float('inf'))
    if optimal_result['solution']:
        print(f"\n🛤️  OPTIMAL SOLUTION PATH ({optimal_result['algorithm']}):")
        print_solution_path(optimal_result['solution'])


def run_comparison():
    """Run both algorithms and compare their performance."""
    start_board = [
        [8, 7, 6],
        [5, 4, 3],
        [2, 1, 0]
    ]

    target_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    start_state = PuzzleState(start_board, (2, 2))

    print("🧩 SLIDING BLOCK PUZZLE SOLVER")
    print("=" * 50)

    # Check solvability
    if not is_solvable(start_board):
        print("❌ ERROR: This puzzle configuration is not solvable!")
        return

    print("✅ Puzzle is solvable - proceeding with search algorithms...")

    # Print puzzle configuration
    print(f"\n{'=' * 50}")
    print("PUZZLE CONFIGURATION:")
    print("=" * 50)
    print("\n📍 Start configuration:")
    start_state.print_board()
    print("🎯 Target configuration:")
    PuzzleState(target_board, (2, 2)).print_board()

    # Run algorithms
    algorithms = [
        ("Depth-First Search", lambda: depth_first_search(start_state, target_board)),
        ("A* Search", lambda: a_star_search(start_state, target_board))
    ]

    results = []
    for name, algorithm in algorithms:
        result = run_algorithm(name, algorithm)
        if result['solution']:
            results.append(result)

    # Print comparison
    if results:
        print_comparison(results)


if __name__ == "__main__":
    run_comparison()

