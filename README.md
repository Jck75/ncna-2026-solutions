# ICPC North Central North America Regional Contest (NCNA 2026) Solutions

This repository contains complete, verified Python 3 solutions and detailed technical analysis reports for all 10 problems from the **2026 ICPC North Central North America Regional Contest (NCNA 2026)** hosted on [Kattis](https://ncna26.kattis.com/contests/ncna26).

---

## Contest Overview & Problem Matrix

| # | Problem Title | Kattis ID | Algorithm / Technique | Complexity | Solution File | Technical Report |
|---|---|---|---|---|:---:|:---:|
| **A** | **Wheelchair Maze** | `wheelchairmaze` | State-Space BFS (Kinematics DAG) | $O(R \cdot C \cdot D_L \cdot D_R)$ | [`problem_a.py`](problem_a.py) | [`reports/problem_a.md`](reports/problem_a.md) |
| **B** | **Total Eclipse** | `totaleclipse` | Circular Interval Union & Coverage | $O(N^2 \log N)$ worst, $O(N)$ typ. | [`problem_b.py`](problem_b.py) | [`reports/problem_b.md`](reports/problem_b.md) |
| **C** | **Top Digit** | `topdigit` | Segmented Sieve & Slice Counting | $O(B + \frac{R}{\ln R})$ | [`problem_c.py`](problem_c.py) | [`reports/problem_c.md`](reports/problem_c.md) |
| **D** | **Swat that Fly** | `swatthatfly` | Configuration Space $L_1$ Shortest Path | $O(1)$ | [`problem_d.py`](problem_d.py) | [`reports/problem_d.md`](reports/problem_d.md) |
| **E** | **Rubik's Towers of Hanoi** | `rubikstowersofhanoi` | Bounded State-Space BFS | $O(3^N \cdot N)$ | [`problem_e.py`](problem_e.py) | [`reports/problem_e.md`](reports/problem_e.md) |
| **F** | **Out of Order** | `outoforder` | Hash Set Adjacency Verification | $O(N \log N)$ | [`problem_f.py`](problem_f.py) | [`reports/problem_f.md`](reports/problem_f.md) |
| **G** | **Loose Change** | `loosechange` | Dominance Pruning & Branch-and-Bound | $O(3^N)$ worst, $< 3000$ nodes | [`problem_g.py`](problem_g.py) | [`reports/problem_g.md`](reports/problem_g.md) |
| **H** | **Greedy Miner** | `greedyminer` | Profile Dynamic Programming ($W = 4$) | $O(L \cdot 22 \cdot 16)$ | [`problem_h.py`](problem_h.py) | [`reports/problem_h.md`](reports/problem_h.md) |
| **I** | **Common Descent** | `commondescent` | Dual-Tree Poset & Dual Segment Tree | $O(N \log N)$ | [`problem_i.py`](problem_i.py) | [`reports/problem_i.md`](reports/problem_i.md) |
| **J** | **The Ants Go Marching** | `antsort` | Loop Dynamics & Level-Synchronous BFS | $O(N \cdot B^{\text{depth}})$, $\le 5$ steps | [`problem_j.py`](problem_j.py) | [`reports/problem_j.md`](reports/problem_j.md) |

---

## Detailed Summary of Each Problem

### Problem A: Wheelchair Maze
* **Kattis ID:** `wheelchairmaze`
* **Summary:** A wheelchair navigates hallways where large wheels follow distinct odometer rules: straight moves advance both wheels by 1m, while 90° turns pivot on the inner wheel (0m) and advance the outer wheel by 1m. Determine if a collision-free path exists from entrance to exit achieving exact target odometer readings $(D_L, D_R) \le 10$.
* **Approach:** Modeled the wheelchair state on the grid as `(segment_type, r, c, direction, d_L, d_R)`. Because odometer readings strictly increase with every movement, the state transition graph is a Directed Acyclic Graph (DAG). Solved using Breadth-First Search (BFS) with distance-pruning.
* **Full Report:** [Problem A Technical Report](reports/problem_a.md)

---

### Problem B: Total Eclipse
* **Kattis ID:** `totaleclipse`
* **Summary:** A point-source neutron star illuminates $N \le 2000$ circular planetary cross-sections in a 2D plane. Determine how many planets are completely eclipsed from direct starlight by intervening planets closer to the star.
* **Approach:** Converted each planet into an angular coverage interval $[\phi - \theta/2, \phi + \theta/2]$ centered at angle $\phi$ with angular width $\theta$. Solved circular wrap-around at $2\pi$ by local linearization centered at the target planet. Checked if the target planet's angular span is completely covered by the union of angular intervals of closer planets.
* **Full Report:** [Problem B Technical Report](reports/problem_b.md)

---

### Problem C: Top Digit
* **Kattis ID:** `topdigit`
* **Summary:** Given a range $[L, R]$ with $1 \le L \le R \le 10^8$, find the base-10 digit occurring most frequently among primes in $[L, R]$. Ties broken in favor of the smaller digit; output 0 if no primes exist.
* **Approach:** Implemented a two-regime engine: for small intervals ($R - L + 1 \le 2 \times 10^6$), a fast segmented sieve is used; for large intervals, an odd-only bitset sieve up to $10^8$ using `bytearray` slice assignment is paired with $O(B)$ block prefix and residue-suffix slice counts, completing in $< 0.49$ seconds in pure Python.
* **Full Report:** [Problem C Technical Report](reports/problem_c.md)

---

### Problem D: Swat that Fly
* **Kattis ID:** `swatthatfly`
* **Summary:** A fly of size $4 \times 2$ sits at $(0, 0)$. Two hands of dimensions $12 \times 2$ must move from initial coordinates to opposite sides of the fly outside a forbidden strike zone $[-D, D] \times [-D, D]$ to perform a final horizontal clap. Find the minimum total Manhattan movement distance.
* **Approach:** Formulated the forbidden zone in configuration space as the Minkowski sum of the strike zone and hand dimensions. Derived closed-form piecewise $L_1$ geodesics around the rectangular obstacle, evaluating both hand assignment permutations in $O(1)$ time.
* **Full Report:** [Problem D Technical Report](reports/problem_d.md)

---

### Problem E: Rubik's Towers of Hanoi
* **Kattis ID:** `rubikstowersofhanoi`
* **Summary:** Up to 8 disks are scrambled across 3 pegs in an arbitrary (possibly illegal) configuration. Using standard Hanoi moves (top disk moves to an empty peg or onto a larger disk), find the minimum moves to stack all disks in decreasing size order on any single peg, or return -1.
* **Approach:** Because disk placements must respect the larger-over-smaller invariant for all moves, reachable configurations are strictly bounded by $3^8 = 6,561$ states. Solved via BFS with state hashing, running in $\approx 0.01$ seconds.
* **Full Report:** [Problem E Technical Report](reports/problem_e.md)

---

### Problem F: Out of Order
* **Kattis ID:** `outoforder`
* **Summary:** Given a list of integers, verify if it is "totally out of order" (no two adjacent elements in the input would be adjacent if the list were sorted in increasing or decreasing order).
* **Approach:** Constructed the set of valid adjacent pairs in the sorted array $\mathcal{P}_{\text{sorted}}$ in $O(N \log N)$ time, treating duplicates as indistinct. Checked all consecutive input pairs against this set in $O(N)$ time.
* **Full Report:** [Problem F Technical Report](reports/problem_f.md)

---

### Problem G: Loose Change
* **Kattis ID:** `loosechange`
* **Summary:** Given up to 12 non-overlapping coins in the 2D plane, replace them with higher-value coins (Penny, Nickel, Dime, Quarter, Half Dollar) centered at the same coordinates such that no two coins overlap. Maximize total dollar value.
* **Approach:** Proved the **Dime Dominance Property**: a Dime (10¢, $d=705$) strictly dominates Penny (1¢, $d=750$) and Nickel (5¢, $d=835$) in both value and size, reducing choices per coin to 3 (Dime, Quarter, Half). Solved with branch-and-bound and pairwise integer distance checks $4((x_1-x_2)^2 + (y_1-y_2)^2) \ge (d_1+d_2)^2$.
* **Full Report:** [Problem G Technical Report](reports/problem_g.md)

---

### Problem H: Greedy Miner
* **Kattis ID:** `greedyminer`
* **Summary:** In an $L \times 4$ ore seam, select squares to mine vs. leave as supports to maximize mined value. Must satisfy: (1) no $2 \times 2$ block is completely mined (ceiling safety), and (2) all mined squares form a single 4-connected component (accessible from one entrance).
* **Approach:** Since width is fixed at $W = 4$, used **Profile Dynamic Programming**. Maintained canonical connected component profiles using DSU across row transitions, pruning abandoned components to guarantee global connectivity.
* **Full Report:** [Problem H Technical Report](reports/problem_h.md)

---

### Problem I: Common Descent
* **Kattis ID:** `commondescent`
* **Summary:** Given two genealogies (rooted trees $T_1$ and $T_2$ on $N \le 200{,}000$ vertices) sharing root 1, find the maximum weight of a sequence of people where each person is a strict ancestor of the next in both trees, and count the number of such maximum lines modulo $1{,}000{,}000{,}007$.
* **Approach:** Formulated as finding the longest weighted chain in the common ancestor poset. Used an Euler tour on $T_2$ to map subtrees to intervals, and traversed $T_1$ with an iterative Dual Segment Tree supporting range updates and point queries in $O(N \log N)$ time.
* **Full Report:** [Problem I Technical Report](reports/problem_i.md)

---

### Problem J: The Ants Go Marching
* **Kattis ID:** `antsort`
* **Summary:** $N \le 31$ ants emerge from an anthill at times $e_i \le 30$. When the leader crosses her own trail, later ants take the newer shortcut, while earlier ants traverse the loop. Ants converging simultaneously march abreast in numerical order. Find the minimum self-crossings for the leader to sort all ants numerically.
* **Approach:** Proved that a loop of length $L$ maps relative offsets $\tau \ge L$ to $\tau - L$. Established the **5-Crossing Theorem** (repeated powers-of-two loops merge all ants in $\le 5$ steps). Solved via level-synchronous BFS with state pruning in $< 0.04$ seconds.
* **Full Report:** [Problem J Technical Report](reports/problem_j.md)

---

## Repository Structure

```
icpc_2026_questions/
├── README.md               # Master competition report and index
├── .gitignore
├── problem_a.py            # Solution for Problem A (Wheelchair Maze)
├── problem_b.py            # Solution for Problem B (Total Eclipse)
├── problem_c.py            # Solution for Problem C (Top Digit)
├── problem_d.py            # Solution for Problem D (Swat that Fly)
├── problem_e.py            # Solution for Problem E (Rubik's Towers of Hanoi)
├── problem_f.py            # Solution for Problem F (Out of Order)
├── problem_g.py            # Solution for Problem G (Loose Change)
├── problem_h.py            # Solution for Problem H (Greedy Miner)
├── problem_i.py            # Solution for Problem I (Common Descent)
├── problem_j.py            # Solution for Problem J (The Ants Go Marching)
├── reports/
│   ├── problem_a.md        # Technical analysis report for Problem A
│   ├── problem_b.md        # Technical analysis report for Problem B
│   ├── problem_c.md        # Technical analysis report for Problem C
│   ├── problem_d.md        # Technical analysis report for Problem D
│   ├── problem_e.md        # Technical analysis report for Problem E
│   ├── problem_f.md        # Technical analysis report for Problem F
│   ├── problem_g.md        # Technical analysis report for Problem G
│   ├── problem_h.md        # Technical analysis report for Problem H
│   ├── problem_i.md        # Technical analysis report for Problem I
│   └── problem_j.md        # Technical analysis report for Problem J
└── raw_problems/           # Extracted markdown problem statements and assets
```
