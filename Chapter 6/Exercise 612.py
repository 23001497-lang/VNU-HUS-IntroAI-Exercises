from collections import deque
import heapq
import time

GOAL = (1,2,3,4,5,6,7,8,0)  # 0 is the blank
MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

def is_solvable(state):
    """For 3x3 8-puzzle: puzzle is solvable iff inversion count is even."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

def h_misplaced(state):
    """h1: number of misplaced tiles (excluding blank)"""
    return sum(1 for i, v in enumerate(state) if v != 0 and v != GOAL[i])

def h_manhattan(state):
    """h2: sum of Manhattan distances of tiles to goal positions"""
    dist = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        goal_index = v - 1
        r1, c1 = divmod(i, 3)
        r2, c2 = divmod(goal_index, 3)
        dist += abs(r1-r2) + abs(c1-c2)
    return dist

def neighbors(state):
    """Yields (neighbor_state, move_name)"""
    zero_idx = state.index(0)
    zr, zc = divmod(zero_idx, 3)
    for move, delta in MOVES.items():
        new_idx = zero_idx + delta
        if move == 'Up' and zr == 0: continue
        if move == 'Down' and zr == 2: continue
        if move == 'Left' and zc == 0: continue
        if move == 'Right' and zc == 2: continue
        new_state = list(state)
        new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
        yield tuple(new_state), move

def a_star(start, heuristic_func):
    """
    A* search.
    Returns: (moves_list, states_list, stats_dict)
      - moves_list: sequence of moves from start -> goal
      - states_list: sequence of states (tuples)
      - stats_dict: nodes_expanded, max_frontier, time_sec, path_cost
    If unsolvable: (None, None, {'solvable': False})
    """
    if not is_solvable(start):
        return None, None, {'solvable': False}

    open_heap = []
    counter = 0  # tie-breaker so heap entries are deterministic
    start_h = heuristic_func(start)
    heapq.heappush(open_heap, (start_h, counter, start))

    came_from = {start: (None, None)}  # state -> (parent_state, move)
    g_score = {start: 0}
    closed = set()

    nodes_expanded = 0
    max_frontier = 1
    start_time = time.perf_counter()

    while open_heap:
        f, _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == GOAL:
            time_taken = time.perf_counter() - start_time
            # Reconstruct path
            path_states = []
            path_moves = []
            s = current
            while s is not None:
                p, mv = came_from[s]
                path_states.append(s)
                if mv is not None:
                    path_moves.append(mv)
                s = p
            path_states.reverse()
            path_moves.reverse()
            stats = {
                'nodes_expanded': nodes_expanded,
                'max_frontier': max_frontier,
                'time_sec': time_taken,
                'path_cost': len(path_moves)
            }
            return path_moves, path_states, stats

        closed.add(current)
        nodes_expanded += 1
        g_curr = g_score[current]

        for nstate, move in neighbors(current):
            tentative_g = g_curr + 1
            if nstate in closed and tentative_g >= g_score.get(nstate, float('inf')):
                continue
            if tentative_g < g_score.get(nstate, float('inf')):
                came_from[nstate] = (current, move)
                g_score[nstate] = tentative_g
                fscore = tentative_g + heuristic_func(nstate)
                counter += 1
                heapq.heappush(open_heap, (fscore, counter, nstate))

        if len(open_heap) > max_frontier:
            max_frontier = len(open_heap)

    # No solution found (should not happen for solvable inputs)
    time_taken = time.perf_counter() - start_time
    return None, None, {'solvable': True, 'nodes_expanded': nodes_expanded,
                        'max_frontier': max_frontier, 'time_sec': time_taken}

# Utility printing
def print_state(state):
    s = list(state)
    lines = []
    for i in range(0, 9, 3):
        lines.append(' '.join(str(x) if x!=0 else '_' for x in s[i:i+3]))
    return '\n'.join(lines)

def summarize_solution(moves, states, stats, max_show=3):
    if moves is None:
        if not stats.get('solvable', True):
            return "Not solvable."
        return "No solution found."
    out = []
    out.append(f"Solution length: {stats['path_cost']}")
    out.append(f"Nodes expanded: {stats['nodes_expanded']}")
    out.append(f"Max frontier size: {stats['max_frontier']}")
    out.append(f"Time: {stats['time_sec']:.4f} sec")
    out.append("Moves: " + ' '.join(moves))
    out.append("Path states:")
    if len(states) <= max_show*2:
        for i, st in enumerate(states):
            out.append(f"Step {i}:\n{print_state(st)}\n---")
    else:
        for i in range(max_show):
            out.append(f"Step {i}:\n{print_state(states[i])}\n---")
        out.append("   ...")
        for i in range(len(states)-max_show, len(states)):
            out.append(f"Step {i}:\n{print_state(states[i])}\n---")
    return '\n'.join(out)

# Tests
tests = [
    ((1,2,3,4,5,6,7,8,0), "Already solved"),
    ((1,2,3,4,5,6,0,7,8), "Two-move example"),
    ((8,6,7,2,5,4,3,0,1), "Hard (known 31-move instance)")
]

if __name__ == "__main__":
    for st, name in tests:
        print("\n=== Test:", name, "===")
        print("Start state:")
        print(print_state(st))
        print("Solvable?", is_solvable(st))
        for hfunc, hname in [(h_misplaced, "h1: misplaced tiles"),
                             (h_manhattan, "h2: manhattan distance")]:
            print(f"\nRunning A* with {hname} ...")
            moves, states, stats = a_star(st, hfunc)
            print(summarize_solution(moves, states, stats))
