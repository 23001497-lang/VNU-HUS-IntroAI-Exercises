from collections import deque
import heapq
import time
import math

# --- Utilities: factorials and Lehmer rank (permutation -> index) ---
FACT = [1]*10
for i in range(1,10):
    FACT[i] = FACT[i-1]*i

def perm_to_rank(perm):
    """Lehmer code: map permutation of 0..8 to a unique rank 0..9!-1"""
    # perm is a tuple/list length 9 with values 0..8
    rank = 0
    used = [False]*9
    for i in range(9):
        smaller = 0
        v = perm[i]
        for x in range(v):
            if not used[x]:
                smaller += 1
        rank += smaller * FACT[8-i]
        used[v] = True
    return rank

def rank_to_perm(rank):
    """Inverse of perm_to_rank"""
    seq = list(range(9))
    perm = [0]*9
    for i in range(9):
        f = FACT[8-i]
        idx = rank // f
        rank %= f
        perm[i] = seq.pop(idx)
    return tuple(perm)

# --- Board helpers ---
GOAL = (1,2,3,4,5,6,7,8,0)
GOAL_RANK = perm_to_rank(GOAL)

# precompute possible moves of the blank index (0..8)
NEIGH_IDX = {
    0: [1,3],
    1: [0,2,4],
    2: [1,5],
    3: [0,4,6],
    4: [1,3,5,7],
    5: [2,4,8],
    6: [3,7],
    7: [4,6,8],
    8: [5,7]
}

# precompute manhattan distances for tile value (1..8) at each position (0..8)
MANH = [[0]*9 for _ in range(9)]  # MANH[val][pos] (val 0..8, but we ignore val=0)
for val in range(1,9):
    goal_pos = GOAL.index(val)
    gx, gy = divmod(goal_pos, 3)
    for pos in range(9):
        x, y = divmod(pos, 3)
        MANH[val][pos] = abs(x-gx) + abs(y-gy)

def manhattan(perm):
    s = 0
    for pos, val in enumerate(perm):
        if val != 0:
            s += MANH[val][pos]
    return s

# neighbors generator using index swapping (faster than creating many lists)
def neighbors_states(state):
    z = state.index(0)
    for nidx in NEIGH_IDX[z]:
        lst = list(state)
        lst[z], lst[nidx] = lst[nidx], lst[z]
        yield tuple(lst), nidx  # return new state and new zero index (for potential use)

# --- Optimized BFS using boolean visited array indexed by permutation rank ---
def bfs_fast(start):
    start_time = time.time()
    if start == GOAL:
        return [], 0, 0, time.time()-start_time
    visited = bytearray(FACT[9])  # 362880 bytes, ~354 KB
    parents = dict()  # store parent rank and move as (parent_rank, action)
    q = deque()
    sr = perm_to_rank(start)
    q.append(sr)
    parents[sr] = (None, None)
    visited[sr] = 1
    nodes = 0
    max_frontier = 1
    while q:
        r = q.popleft()
        nodes += 1
        state = rank_to_perm(r)
        z = state.index(0)
        for nidx in NEIGH_IDX[z]:
            lst = list(state)
            lst[z], lst[nidx] = lst[nidx], lst[z]
            nr = perm_to_rank(lst)
            if not visited[nr]:
                visited[nr] = 1
                parents[nr] = (r, nidx)  # store where blank moved to (action = new blank index)
                if nr == GOAL_RANK:
                    # reconstruct
                    path = []
                    cur = nr
                    while parents[cur][0] is not None:
                        p, action = parents[cur]
                        # action is the index where blank moved to; we can derive move name
                        # derive move by comparing positions of zero in parent and cur
                        parent_state = rank_to_perm(p)
                        parent_z = parent_state.index(0)
                        if action == parent_z - 3:
                            move = 'Up'
                        elif action == parent_z + 3:
                            move = 'Down'
                        elif action == parent_z - 1:
                            move = 'Left'
                        else:
                            move = 'Right'
                        path.append(move)
                        cur = p
                    path.reverse()
                    return path, len(path), nodes, time.time()-start_time
                q.append(nr)
        if len(q) > max_frontier:
            max_frontier = len(q)
    return None, None, nodes, time.time()-start_time

# --- A* with Manhattan heuristic (optimized using rank-indexed arrays for g-scores) ---
def astar_manhattan(start):
    start_time = time.time()
    if start == GOAL:
        return [], 0, 0, time.time()-start_time
    start_rank = perm_to_rank(start)
    g_scores = [math.inf] * FACT[9]
    parent = [-1] * FACT[9]
    parent_action = [-1] * FACT[9]
    open_heap = []
    start_h = manhattan(start)
    g_scores[start_rank] = 0
    heapq.heappush(open_heap, (start_h, start_rank))
    nodes = 0
    max_open = 1
    closed = bytearray(FACT[9])
    while open_heap:
        f, r = heapq.heappop(open_heap)
        # lazy-deletion: skip if popped state already has a worse g or closed
        if closed[r]:
            continue
        nodes += 1
        current = rank_to_perm(r)
        if r == GOAL_RANK:
            # reconstruct path
            path = []
            cur = r
            while parent[cur] != -1:
                p = parent[cur]
                action = parent_action[cur]
                parent_state = rank_to_perm(p)
                parent_z = parent_state.index(0)
                if action == parent_z - 3:
                    move = 'Up'
                elif action == parent_z + 3:
                    move = 'Down'
                elif action == parent_z - 1:
                    move = 'Left'
                else:
                    move = 'Right'
                path.append(move)
                cur = p
            path.reverse()
            return path, len(path), nodes, time.time()-start_time
        closed[r] = 1
        z = current.index(0)
        for nidx in NEIGH_IDX[z]:
            lst = list(current)
            lst[z], lst[nidx] = lst[nidx], lst[z]
            nr = perm_to_rank(lst)
            if closed[nr]:
                continue
            tentative_g = g_scores[r] + 1
            if tentative_g < g_scores[nr]:
                g_scores[nr] = tentative_g
                parent[nr] = r
                parent_action[nr] = nidx
                h = manhattan(lst)
                heapq.heappush(open_heap, (tentative_g + h, nr))
        if len(open_heap) > max_open:
            max_open = len(open_heap)
    return None, None, nodes, time.time()-start_time

# --- IDA* (iterative deepening A*), often best for sliding puzzles for memory reasons ---
def ida_star(start):
    start_time = time.time()
    bound = manhattan(start)
    path = [start]
    nodes = 0
    max_search_nodes = 10_000_000  # safety cap

    def search(g, bound, zero_idx):
        nonlocal nodes
        nodes += 1
        if nodes > max_search_nodes:
            return None, math.inf  # exhausted
        current = path[-1]
        f = g + manhattan(current)
        if f > bound:
            return None, f
        if current == GOAL:
            return list(path), f
        min_thresh = math.inf
        z = zero_idx
        for nidx in NEIGH_IDX[z]:
            lst = list(current)
            lst[z], lst[nidx] = lst[nidx], lst[z]
            nxt = tuple(lst)
            if len(path) >= 2 and nxt == path[-2]:
                continue  # don't immediately backtrack to parent (prunes trivial cycles)
            path.append(nxt)
            res, t = search(g+1, bound, nidx)
            if res is not None:
                return res, t
            if t < min_thresh:
                min_thresh = t
            path.pop()
        return None, min_thresh

    zero_idx = start.index(0)
    while True:
        nodes = 0
        res, t = search(0, bound, zero_idx)
        if res is not None:
            # reconstruct moves from res
            moves = []
            for i in range(len(res)-1):
                p = res[i]
                q = res[i+1]
                pz = p.index(0)
                qz = q.index(0)
                if qz == pz - 3: moves.append('Up')
                elif qz == pz + 3: moves.append('Down')
                elif qz == pz - 1: moves.append('Left')
                else: moves.append('Right')
            return moves, len(moves), nodes, time.time()-start_time
        if t == math.inf:
            return None, None, nodes, time.time()-start_time
        bound = t

# --- Testcases and run ---
tests = {
    "easy": (1,2,3,4,5,6,0,7,8),      # 2 moves
    "medium": (1,2,3,5,0,6,4,7,8),    # ~4 moves
    "moderate": (1,3,6,5,0,2,4,7,8)   # moderate difficulty
}

print("Goal:\n", GOAL)
for name, start in tests.items():
    print("\n=== Test:", name)
    print("Start:\n", start)
    # BFS
    p, d, nodes, t = bfs_fast(start)
    if p is None:
        print("BFS failed or not found. nodes:", nodes)
    else:
        print(f"BFS: len={d}, nodes_expanded={nodes}, time={t:.4f}s, moves={p}")
    # A*
    p, d, nodes, t = astar_manhattan(start)
    if p is None:
        print("A* failed. nodes:", nodes)
    else:
        print(f"A*: len={d}, nodes_expanded={nodes}, time={t:.4f}s, moves={p}")
    # IDA*
    p, d, nodes, t = ida_star(start)
    if p is None:
        print("IDA* failed. nodes:", nodes)
    else:
        print(f"IDA*: len={d}, nodes_expanded={nodes}, time={t:.4f}s, moves={p}")

