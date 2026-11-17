#!/usr/bin/env python3
"""
Problem G: Loose Change (NCNA 2026)

Problem Summary:
Given N (<= 12) coins at specified 2D coordinates (in mils) that are initially
non-overlapping (possibly touching). We can replace any coin with any available
US coin type (Penny, Nickel, Dime, Quarter, Half), keeping the center coordinates.
Find the maximum total dollar value of the resulting non-overlapping set of coins.

Coin Types:
- Penny:   1 cent,  diameter 750 mils
- Nickel:  5 cents, diameter 835 mils
- Dime:   10 cents, diameter 705 mils
- Quarter: 25 cents, diameter 955 mils
- Half:   50 cents, diameter 1205 mils

Dominance Principle:
A Dime (10c, diameter 705) strictly dominates both a Penny (1c, diameter 750)
and a Nickel (5c, diameter 835) because it has higher value and smaller diameter.
Thus, any valid coin configuration using Pennies or Nickels can be replaced with
Dimes to strictly increase or maintain value without causing any overlap.
Therefore, we only ever need to consider:
1. Half dollar (50 cents, diameter 1205)
2. Quarter (25 cents, diameter 955)
3. Dime (10 cents, diameter 705)

Non-overlapping condition:
Two coins at centers (x1, y1) and (x2, y2) with diameters d1, d2 do not overlap iff:
Distance >= (d1 + d2) / 2 <=> 4 * ((x1 - x2)^2 + (y1 - y2)^2) >= (d1 + d2)^2.
"""

import sys

# Candidate replacement coins in descending order of value
CANDIDATES = [
    (50, 1205),  # Half dollar
    (25, 955),   # Quarter
    (10, 705)    # Dime
]

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    if n == 0:
        print("$0.00")
        return

    # Read coins: each has initial_value, x, y
    coords = []
    idx = 1
    for _ in range(n):
        _val = int(input_data[idx])
        x = int(input_data[idx + 1])
        y = int(input_data[idx + 2])
        coords.append((x, y))
        idx += 3

    # Precompute pairwise squared distances
    dist_sq = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i + 1, n):
            xj, yj = coords[j]
            d2 = (xi - xj) ** 2 + (yi - yj) ** 2
            dist_sq[i][j] = d2
            dist_sq[j][i] = d2

    # For each coin i, determine the maximum candidate it could theoretically be,
    # assuming all other coins j take their smallest possible diameter (Dime, 705).
    max_possible = [10] * n
    for i in range(n):
        for val, d in CANDIDATES:
            # Check if coin i with diameter d can coexist with all other coins having diameter 705
            can_fit = True
            for j in range(n):
                if i != j and 4 * dist_sq[i][j] < (d + 705) ** 2:
                    can_fit = False
                    break
            if can_fit:
                max_possible[i] = val
                break

    # Suffix maximum sum for branch and bound upper bound
    suffix_max = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_max[i] = suffix_max[i + 1] + max_possible[i]

    # Precompute pairwise compatibility between candidates
    # compat[i][j][c_i][c_j] is True if coin i choice c_i is compatible with coin j choice c_j
    compat = [[[[True] * 3 for _ in range(3)] for _ in range(n)] for _ in range(n)]
    req_dist_sq = [[(CANDIDATES[c1][1] + CANDIDATES[c2][1]) ** 2 for c2 in range(3)] for c1 in range(3)]

    for i in range(n):
        for j in range(i + 1, n):
            d4 = 4 * dist_sq[i][j]
            for c1 in range(3):
                for c2 in range(3):
                    ok = (d4 >= req_dist_sq[c1][c2])
                    compat[i][j][c1][c2] = ok
                    compat[j][i][c2][c1] = ok

    # All Dimes is always valid because the original arrangement had non-overlapping coins,
    # and Dime has diameter 705, which is <= all original coin diameters.
    best_val = 10 * n
    assignment = []

    def dfs(coin_idx, current_val):
        nonlocal best_val

        # Branch & Bound pruning: even if all remaining coins take their theoretical upper bound
        if current_val + suffix_max[coin_idx] <= best_val:
            return

        if coin_idx == n:
            if current_val > best_val:
                best_val = current_val
            return

        for c, (val, d) in enumerate(CANDIDATES):
            if val > max_possible[coin_idx]:
                continue

            # Check compatibility against previously assigned coins
            possible = True
            for prev_idx, prev_c in enumerate(assignment):
                if not compat[coin_idx][prev_idx][c][prev_c]:
                    possible = False
                    break

            if possible:
                assignment.append(c)
                dfs(coin_idx + 1, current_val + val)
                assignment.pop()

    dfs(0, 0)

    dollars = best_val // 100
    cents = best_val % 100
    print(f"${dollars}.{cents:02d}")

if __name__ == "__main__":
    solve()
