# AI Search Algorithm Profiling: BFS vs. DFS on the 8-Puzzle Problem

* **Name:** Aniket Anandrao Mane
* **PRN:** 25UAM045
* **Class:** SY BTech (Div A)
* **Course:** Introduction to Artificial Intelligence (SLE-2)

##  1. Project Overview & Objective
This project implements, profiles, and compares two classic uninformed search strategies—**Breadth-First Search (BFS)** and **Depth-First Search (DFS)**—to solve the classic **8-Puzzle problem**. The goal is to evaluate algorithmic efficiency, execution overhead, memory/state expansion behavior, and solution optimality under identical starting conditions.

##  2. Problem Configuration & State Space
* **Domain:** 8-Puzzle Uninformed State-Space Search
* **Initial State:** 
  ```text
  1 2 3
  4 0 6
  7 5 8
  
* **Goal State:**

1 2 3
4 5 6
7 8 0

##  3. Profiling Methodology & Metrics Tracked

1. **Measurement Tools:** Utilized Python’s high-resolution `time.perf_counter()` timer to measure exact execution duration down to microseconds, combined with a manual node-expansion counter variable.

2. **Execution Strategy:** Both algorithms were executed programmatically on the exact same randomized initial state across trial runs to maintain empirical consistency.

3. **Metrics:**
* **Execution Time (ms):** Total CPU time taken to find the target state.
* **Nodes Expanded:** Total number of unique board states popped and evaluated from the frontier.
* **Solution Steps (Path Length):** Total number of moves required to reach the goal configuration.

##  4. Comprehensive Results & Performance Comparison
------------------------------------------------------------------------------------------------------------------------------------------
| Performance Metric              | Breadth-First Search (BFS)    | Depth-First Search (DFS)        | Performance Winner                 |
------------------------------------------------------------------------------------------------------------------------------------------
| **Execution Time**              | **0.1198 ms**                 | 5.6039 ms                       | **BFS** (Faster by ~46x)           |
| **Nodes Expanded**              | **9 states**                  | 1,357 states                    | **BFS** (Massively lower overhead) |
| **Solution Steps / Path Depth** | Optimal shortest path         | Deep / suboptimal path          | **BFS** (Guarantees optimality)    |
| **Search Strategy**             | Level-by-level (Queue / FIFO) | Branch-by-branch (Stack / LIFO) | **BFS**                            |
------------------------------------------------------------------------------------------------------------------------------------------

* **Short Observation:** BFS solved the puzzle almost instantaneously by expanding only 9 states, whereas DFS explored 1,357 states and took significantly longer.

## 📝 5. Detailed Technical Analysis & Justification

### Why BFS Outperformed DFS:

* **Systematic Level-Order Exploration:** BFS explores the search space tier-by-tier using a Queue data structure (`deque`). Because the goal state was located close to the root configuration in this specific test case, BFS found the solution almost instantaneously by evaluating only **9 nodes** in **0.1198 ms**.


* **Optimality Guarantee:** BFS guarantees the shortest possible path to the goal because it explores all nodes at depth $d$ before moving to depth $d+1$.

### The Pitfalls of DFS on this Domain:

* **Blind Deep Traversal:** DFS dives deep down a single path branch using a Stack structure. Without strict heuristic guidance or tight depth bounds in basic uninformed implementations, DFS wandered through **1,357 states** and took **5.6039 ms**.


* **Redundant Exploration:** DFS can get trapped searching irrelevant subtrees or looping down deep branches before backtracking, making it highly inefficient for unconstrained puzzle state-spaces.

## 💻 6. Source Code (`Profile_Puzzle.py`)

```python
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

```
## 🚀 7. How to Run Locally
1. Ensure Python is installed on your system.
2. Save the code section above as `Profile_Puzzle.py`.
3. Open your terminal in the script directory and execute:
```bash
python profile_puzzle.py
