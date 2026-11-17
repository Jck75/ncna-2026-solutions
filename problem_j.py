#!/usr/bin/env python3
"""
Problem J: The Ants Go Marching
North Central North America Regional Contest (NCNA) 2026

Solution approach:
When the leader crosses her own path, she creates a loop of length L (integral seconds).
For any ant with offset tau:
- If tau < L: The ant arrives before the crossing is created, entering the loop.
              Upon exiting, its new offset relative to the leader is tau' = tau.
- If tau >= L: The ant arrives at or after the crossing, sensing the newer pheromone trail,
               bypassing the loop. Its new offset relative to the leader is tau' = tau - L.
- Ants arriving simultaneously at the intersection merge into a single row abreast,
  sorted in numerical order from left to right.

If we index the ants by their ID rank (rank 0 is the smallest ID, rank N-1 is the largest),
the ants are in total numeric order (including those marching abreast) if and only if
their offsets are non-decreasing:
    arr[0] <= arr[1] <= arr[2] <= ... <= arr[N-1]

At each step, 1 <= L <= max(tau).
Since initial max(tau) <= 30 < 32 = 2^5, repeated halving (or binary bit clearing:
L = 16, 8, 4, 2, 1) guarantees all offsets become 0 in at most 5 steps.
At offset 0, all ants merge into a single row, sorted left to right, which is valid.
Thus, the minimum number of crossings is always between 0 and 5.
We use Breadth-First Search (BFS) to find the exact minimum number of crossings.
"""

import sys


def solve(arr):
    n = len(arr)
    # Check if already in total numeric order (monotonic non-decreasing)
    is_sorted = True
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            is_sorted = False
            break
    if is_sorted:
        return 0

    visited = {arr}
    curr_level = [arr]

    # Search depths 1, 2, 3
    for depth in range(3):
        next_level = []
        for a in curr_level:
            max_t = max(a)
            for L in range(1, max_t + 1):
                nxt = tuple(t if t < L else t - L for t in a)
                # Check if monotonic non-decreasing
                ok = True
                for i in range(n - 1):
                    if nxt[i] > nxt[i + 1]:
                        ok = False
                        break
                if ok:
                    return depth + 1
                if nxt not in visited:
                    visited.add(nxt)
                    next_level.append(nxt)
        curr_level = next_level
        if not curr_level:
            return 5

    # Check depth 4 directly without storing next_level or visited
    for a in curr_level:
        max_t = max(a)
        for L in range(1, max_t + 1):
            prev = a[0] if a[0] < L else a[0] - L
            ok = True
            for i in range(1, n):
                val = a[i] if a[i] < L else a[i] - L
                if prev > val:
                    ok = False
                    break
                prev = val
            if ok:
                return 4

    # Any configuration with max(tau) <= 30 can be reduced to all 0s in at most 5 crossings
    return 5


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    pairs = []
    idx = 1
    for _ in range(n):
        aid = int(input_data[idx])
        tau = int(input_data[idx + 1])
        pairs.append((aid, tau))
        idx += 2

    # Map each ant ID to its 0-indexed rank among all ant IDs
    sorted_ids = sorted(aid for aid, tau in pairs)
    id_to_rank = {aid: r for r, aid in enumerate(sorted_ids)}

    # arr[r] is the emergence time (offset) of the ant with rank r
    arr = [0] * n
    for aid, tau in pairs:
        arr[id_to_rank[aid]] = tau

    result = solve(tuple(arr))
    print(result)


if __name__ == "__main__":
    main()
