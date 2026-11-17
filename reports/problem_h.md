# Problem H: Greedy Miner

**Contest:** ICPC 2026 North Central North America Regional Contest (NCNA 2026)  
**Kattis Problem ID:** `greedyminer`  
**Solution File:** [`problem_h.py`](../problem_h.py)

---

## 1. Problem Statement & Background

Miners have discovered an $L \times 4$ seam of valuable ore. Each square cell $(r, c)$ has an assayed integer ore value. To safely extract the ore without installing artificial bracing posts, miners must leave some ore behind as natural ceiling support pillars:
1. **Ceiling Support Rule:** At each corner of the grid squares, at least one square must be left unmined. Equivalently, **no $2 \times 2$ block of ore may be entirely dug out**.
2. **Access & Connectivity Rule:** Access to the mine is made via a single tunnel or shaft. Therefore, **all mined squares must form a single 4-connected (rectilinearly connected) component**.

The goal is to maximize the total value of mined ore, which is equivalent to minimizing the total value of ore left behind as supports.

### Input Format
* First line: length of the seam $L$ ($L \ge 1$, width is fixed at 4).
* Following $L$ lines: 4 space-separated integers representing the values of each row of 4 squares.

### Output Format
```
Retrievable: <maximum total value of mined ore>
Remaining: <minimum total value of ore left as supports>
```

---

## 2. Mathematical & Algorithmic Analysis

### Why Greedy Approaches Fail
A greedy approach (such as selecting the smallest square in each $2 \times 2$ window) fails because:
1. **Overlapping Coverage:** A single square can simultaneously cover up to four $2 \times 2$ blocks. Picking local minima independently misses the multi-block coverage opportunities and forces extra supports later.
2. **Non-local Connectivity:** Support squares can inadvertently create bottlenecks or sever the mine into disconnected components, leaving mined ore unreachable.

### Profile Dynamic Programming ($W = 4$)
Because the width is strictly fixed at $W = 4$, the problem can be solved using **Profile DP**:
* **Row Masks:** There are $2^4 = 16$ binary masks per row (where bit $c = 1$ if mined, $0$ if support).
* **$2 \times 2$ Constraint:** A transition between row $r-1$ and row $r$ is valid if and only if no column pair $c, c+1$ has all four cells mined.
* **Connectivity Tracking:** Across the frontier of 4 cells, we maintain connected component equivalence classes using Disjoint Set Union (DSU). When a component terminates without merging into surviving components, the state is pruned.

At the final row, all mined cells must belong to at most one connected component.

---

## 3. Complexity Analysis

* **Number of States:** Only $\approx 22$ valid canonical connectivity profiles exist for $W = 4$.
* **Transitions per State:** At most 16 row masks.
* **Time Complexity:** $O(L \times 22 \times 16) \approx O(350 L)$ operations. For $L = 1000$, execution takes $\approx 0.05$ seconds.
* **Space Complexity:** $O(\text{number of states}) \approx O(1)$ space between row transitions.

---

## 4. Implementation Highlights

The core transition in [`problem_h.py`](../problem_h.py) maintains `dp[profile] = min_support_cost`:
* DSU tracks horizontal connections within the current row and vertical connections to the previous row.
* Prevents isolated components from being left behind.
* Relabels components into canonical order $(1, 2, \dots)$.

---

## 5. Verification & Sample Test

### Sample 1
```
Input:
11
5  10  6  5
12  8  3  4
8  7  11  8
9  10  8  3
2  12  5  13
4  9  7  5
6  4  2  4
5  1  5  7
6  7  8  4
8  7  3  4
5  6  2  5

Output:
Retrievable: 228
Remaining: 45
```
Both values match the official judge output.
