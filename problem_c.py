#!/usr/bin/env python3
"""
Problem C: Top Digit
NCNA 2026 Regional Contest

Given positive integers L and R (1 <= L <= R <= 10^8), find the digit (0-9)
that occurs most frequently among the prime numbers in the range [L, R].
If there is a tie, report the smallest digit.
If there are no primes within the specified range, print 0.
"""

import sys


def solve(L: int, R: int) -> int:
    if R < 2 or L > R:
        return 0

    # For small ranges (<= 2,000,000 elements), a segmented sieve on [L, R]
    # is extremely fast (takes < 0.08s) and uses minimal memory.
    if R - L + 1 <= 2_000_000:
        limit = int(R**0.5)
        base = bytearray(b"\x01") * (limit + 1)
        if limit >= 0:
            base[0] = 0
        if limit >= 1:
            base[1] = 0

        for i in range(2, int(limit**0.5) + 1):
            if base[i]:
                start = i * i
                num = (limit - start) // i + 1
                base[start::i] = b"\x00" * num

        primes = [p for p in range(2, limit + 1) if base[p]]

        sz = R - L + 1
        seg = bytearray(b"\x01") * sz
        if L == 1:
            seg[0] = 0

        for p in primes:
            start = (L + p - 1) // p * p
            if start < p * p:
                start = p * p
            if start <= R:
                num = (R - start) // p + 1
                seg[start - L :: p] = b"\x00" * num

        counts = [0] * 10
        has_prime = False
        for i in range(sz):
            if seg[i]:
                has_prime = True
                p = L + i
                while p:
                    counts[p % 10] += 1
                    p //= 10

        if not has_prime:
            return 0
        return counts.index(max(counts))

    # For large ranges, we use an odd-only sieve up to R (at most 50M bytes for R = 10^8)
    # accelerated with C-level bytearray slice assignments, followed by block prefix
    # and suffix counting to avoid millions of individual digit extractions in Python.
    max_i = (R - 1) // 2
    if max_i < 0:
        return 0

    sieve = bytearray(b"\x01") * (max_i + 1)
    sieve[0] = 0  # 1 is not prime

    limit = int(R**0.5) // 2
    s_len = len(sieve)
    for i in range(1, limit + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = p * p // 2
            if start < s_len:
                num = (s_len - 1 - start) // p + 1
                sieve[start::p] = b"\x00" * num

    # Invalidate odd numbers less than L
    zero_until = L // 2
    if zero_until > 0:
        to_zero = min(zero_until, s_len)
        sieve[:to_zero] = b"\x00" * to_zero

    counts = [0] * 10

    # Account for the even prime 2
    if L <= 2 <= R:
        counts[2] += 1

    # For primes < 1000, count digits directly
    idx_1000 = min(500, s_len)
    for i in range(1, idx_1000):
        if sieve[i]:
            p = 2 * i + 1
            while p:
                counts[p % 10] += 1
                p //= 10

    # For primes >= 1000, each number is 1000*q + r where r in [0, 999].
    # 1. Suffixes: for each odd residue r = 2*rem + 1, all occurrences across
    #    all blocks q >= 1 contribute the 3 digits of r (with leading zeros).
    #    We can count all occurrences in one slice count: sieve[500 + rem :: 500].count(1).
    if s_len > 500:
        for rem in range(500):
            cnt = sieve[500 + rem :: 500].count(1)
            if cnt:
                r = 2 * rem + 1
                counts[r // 100] += cnt
                counts[(r // 10) % 10] += cnt
                counts[r % 10] += cnt

        # 2. Prefixes: for each block q >= 1 (numbers in [1000*q, 1000*q + 999]),
        #    every prime in this block contributes the digits of q.
        #    We count primes in each block using sieve slice count.
        max_q = (s_len - 1) // 500
        for q in range(1, max_q + 1):
            start = 500 * q
            end = min(s_len, 500 * (q + 1))
            cnt = sieve[start:end].count(1)
            if cnt:
                temp = q
                while temp:
                    counts[temp % 10] += cnt
                    temp //= 10

    max_c = max(counts)
    if max_c == 0:
        return 0
    return counts.index(max_c)


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    L = int(input_data[0])
    R = int(input_data[1])
    print(solve(L, R))


if __name__ == "__main__":
    main()
