#!/usr/bin/env python3
"""
Problem F: Out of Order
ICPC 2026 North Central North America Regional Contest (NCNA 2026)

Determine whether a given list of integers is "totally out of order".
A list is "totally out of order" if no two values adjacent in the list
would be adjacent if the list were sorted (increasing or decreasing).
Duplicates are indistinct, meaning consecutive duplicates in the original list
are adjacent in the sorted list.
"""

import sys


def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    it = iter(tokens)
    while True:
        try:
            n_str = next(it)
        except StopIteration:
            break
        n = int(n_str)
        arr = [int(next(it)) for _ in range(n)]

        if n <= 1:
            print("Totally out of order")
            continue

        sorted_arr = sorted(arr)
        # Set of all unordered pairs that are adjacent in sorted order
        sorted_adjacent = {
            (min(sorted_arr[i], sorted_arr[i + 1]), max(sorted_arr[i], sorted_arr[i + 1]))
            for i in range(n - 1)
        }

        # Check if any adjacent pair in the input list would be adjacent when sorted
        is_partial = False
        for i in range(n - 1):
            pair = (min(arr[i], arr[i + 1]), max(arr[i], arr[i + 1]))
            if pair in sorted_adjacent:
                is_partial = True
                break

        if is_partial:
            print("In at least partial order")
        else:
            print("Totally out of order")


if __name__ == "__main__":
    solve()
