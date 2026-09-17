from collections import deque
import time

# 8-Puzzle Solver with BFS and DFS Profiling

class PuzzleState:
    def __init__(self, grid, moves=0, path=[]):
        self.grid = tuple(tuple(row) for row in grid)
        self.moves = moves
        self.path = path
    
    def __eq__(self, other):
        return self.grid == other.grid
    
    def __hash__(self):
        return hash(self.grid)
    
    def is_goal(self, goal):
        return self.grid == goal.grid
    
    def get_neighbors(self):
        grid = [list(row) for row in self.grid]
        neighbors = []
        
        # Find empty space (0)
        empty_row, empty_col = None, None
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    empty_row, empty_col = i, j
                    break
        
        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_grid = [row[:] for row in grid]
                new_grid[empty_row][empty_col], new_grid[new_row][new_col] = \
                    new_grid[new_row][new_col], new_grid[empty_row][empty_col]
                
                new_path = self.path + [new_grid]
                neighbors.append(PuzzleState(new_grid, self.moves + 1, new_path))
        
        return neighbors
    
    def print_grid(self):
        for row in self.grid:
            print(row)
        print()


def bfs_solve(start_grid, goal_grid):
    """BFS: Explores level by level"""
    start = PuzzleState(start_grid)
    goal = PuzzleState(goal_grid)
    
    queue = deque([start])
    visited = {start}
    nodes_expanded = 0
    
    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        
        if current.is_goal(goal):
            return current.moves, nodes_expanded, current.path
        
        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return -1, nodes_expanded, []  # No solution found


def dfs_solve(start_grid, goal_grid):
    """DFS: Explores depth first"""
    start = PuzzleState(start_grid)
    goal = PuzzleState(goal_grid)
    
    stack = [start]
    visited = {start}
    nodes_expanded = 0
    
    while stack:
        current = stack.pop()
        nodes_expanded += 1
        
        if current.is_goal(goal):
            return current.moves, nodes_expanded, current.path
        
        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return -1, nodes_expanded, []  # No solution found


# Starting and Goal States
start_grid = [
    [2, 1, 6],
    [4, 0, 3],
    [7, 8, 5]
]

goal_grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

print("=" * 50)
print("8-PUZZLE PROFILING: BFS vs DFS")
print("=" * 50)

print("\nStarting State:")
PuzzleState(start_grid).print_grid()

print("Goal State:")
PuzzleState(goal_grid).print_grid()

# Run each algorithm multiple times
num_runs = 3
bfs_times = []
dfs_times = []
bfs_nodes_list = []
dfs_nodes_list = []

print("\n" + "=" * 50)
print("RUNNING PROFILING (3 runs each)")
print("=" * 50)

for run in range(1, num_runs + 1):
    print(f"\n--- Run {run} ---")
    
    # BFS
    start_time = time.time()
    bfs_moves, bfs_nodes, bfs_path = bfs_solve(start_grid, goal_grid)
    bfs_time = (time.time() - start_time) * 1000  # Convert to ms
    bfs_times.append(bfs_time)
    bfs_nodes_list.append(bfs_nodes)
    
    print(f"BFS: Time = {bfs_time:.2f}ms | Nodes Expanded = {bfs_nodes} | Moves = {bfs_moves}")
    
    # DFS
    start_time = time.time()
    dfs_moves, dfs_nodes, dfs_path = dfs_solve(start_grid, goal_grid)
    dfs_time = (time.time() - start_time) * 1000  # Convert to ms
    dfs_times.append(dfs_time)
    dfs_nodes_list.append(dfs_nodes)
    
    print(f"DFS: Time = {dfs_time:.2f}ms | Nodes Expanded = {dfs_nodes} | Moves = {dfs_moves}")

# Calculate averages
print("\n" + "=" * 50)
print("RESULTS (AVERAGES)")
print("=" * 50)

avg_bfs_time = sum(bfs_times) / len(bfs_times)
avg_dfs_time = sum(dfs_times) / len(dfs_times)
avg_bfs_nodes = sum(bfs_nodes_list) / len(bfs_nodes_list)
avg_dfs_nodes = sum(dfs_nodes_list) / len(dfs_nodes_list)

print(f"\nBFS Average:")
print(f"  Time: {avg_bfs_time:.2f} ms")
print(f"  Nodes Expanded: {avg_bfs_nodes:.0f}")
print(f"  Moves to Goal: {bfs_moves}")

print(f"\nDFS Average:")
print(f"  Time: {avg_dfs_time:.2f} ms")
print(f"  Nodes Expanded: {avg_dfs_nodes:.0f}")
print(f"  Moves to Goal: {dfs_moves}")

print(f"\n{'Better Algorithm':<20} | {'Difference'}")
print("-" * 40)
if avg_bfs_time < avg_dfs_time:
    print(f"{'BFS (by time)':<20} | {avg_dfs_time - avg_bfs_time:.2f} ms faster")
else:
    print(f"{'DFS (by time)':<20} | {avg_bfs_time - avg_dfs_time:.2f} ms faster")

if avg_bfs_nodes < avg_dfs_nodes:
    print(f"{'BFS (by nodes)':<20} | {avg_dfs_nodes - avg_bfs_nodes:.0f} fewer nodes")
else:
    print(f"{'DFS (by nodes)':<20} | {avg_bfs_nodes - avg_dfs_nodes:.0f} fewer nodes")
