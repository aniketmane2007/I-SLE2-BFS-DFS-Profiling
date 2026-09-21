import time
from collections import deque

# Goal state for 8-puzzle (0 represents the empty tile)
GOAL = (1, 2, 3, 
        4, 5, 6, 
        7, 8, 0)

# A sample start state 
START = (1, 2, 3, 
         4, 0, 6, 
         7, 5, 8)

def print_board(state):
    """Helper function to print the puzzle state as a 3x3 grid"""
    for i in range(0, 9, 3):
        print(f"    {state[i]} {state[i+1]} {state[i+2]}")

def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)
    
    # Possible movements: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_zero_idx = nr * 3 + nc
            lst = list(state)
            lst[zero_idx], lst[new_zero_idx] = lst[new_zero_idx], lst[zero_idx]
            neighbors.append(tuple(lst))
            
    return neighbors

# --- 1. Breadth-First Search (BFS) ---
def solve_bfs(start):
    queue = deque([(start, [start])])
    visited = {start}
    nodes_expanded = 0
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        
        if current == GOAL:
            return nodes_expanded, len(path) - 1
            
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return nodes_expanded, -1

# --- 2. Depth-First Search (DFS) ---
def solve_dfs(start, max_depth=20):
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0
    
    while stack:
        current, path = stack.pop()
        
        if current == GOAL:
            return nodes_expanded, len(path) - 1
            
        if current in visited or len(path) > max_depth:
            continue
            
        visited.add(current)
        nodes_expanded += 1
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
                
    return nodes_expanded, -1

# --- Main Execution & Profiling ---
if __name__ == "__main__":
    print("=" * 55)
    print("       BFS vs DFS: 8-Puzzle Performance Analysis")
    print("=" * 55)
    print("\n[INFO] Problem Details:")
    print("  - Domain: 8-Puzzle Uninformed Search")
    print("  - Initial State:")
    print_board(START)
    print("\n  - Goal State:")
    print_board(GOAL)
    print("-" * 55)
    print("Running profiling experiments...\n")
    
    # Profile BFS
    start_time = time.perf_counter()
    bfs_nodes, bfs_steps = solve_bfs(START)
    end_time = time.perf_counter()
    bfs_time_ms = (end_time - start_time) * 1000
    
    # Profile DFS
    start_time = time.perf_counter()
    dfs_nodes, dfs_steps = solve_dfs(START)
    end_time = time.perf_counter()
    dfs_time_ms = (end_time - start_time) * 1000
    
    # Results Display
    print("=" * 55)
    print("                     RESULTS SUMMARY")
    print("=" * 55)
    print(f"{'Algorithm':<12} | {'Execution Time (ms)':<20} | {'Nodes Expanded'}")
    print("-" * 55)
    print(f"{'BFS':<12} | {bfs_time_ms:<20.4f} | {bfs_nodes}")
    print(f"{'DFS':<12} | {dfs_time_ms:<20.4f} | {dfs_nodes}")
    print("=" * 55)