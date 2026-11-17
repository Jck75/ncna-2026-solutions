# Problem H: Greedy Miner

**Contest:** ICPC 2026 North Central North America Regional Contest (NCNA 2026)  
**Kattis Problem ID:** `greedyminer`  
**Solution File:** [`problem_h.py`](../problem_h.py)  
**Problem Statement:** [`H_greedyminer.md`](../raw_problems/H_greedyminer.md)  
**Visual Diagram:** [`problem_h_profile_dp_visual.svg`](../problem_h_profile_dp_visual.svg)

---

## 1. Problem Statement & Constraints

Miners have discovered an $L \times 4$ seam of valuable ore. Each square cell $(r, c)$ has an assayed integer ore value. To safely extract the ore without installing artificial ceiling bracing posts, miners must leave some ore behind as natural ceiling support pillars:

1. **Ceiling Support Rule:** At each corner of the grid squares, at least one square must be left unmined. Equivalently, **no $2 \times 2$ block of ore may be entirely dug out**.
2. **Access & Connectivity Rule:** Access to the mine is made via a single entrance point (shaft or tunnel). Therefore, **all mined squares must form a single 4-connected (rectilinearly connected) component**.

**Goal:** Maximize the total value of mined ore, which is equivalent to minimizing the total value of ore left behind as supports:
$$\text{Max Mined Value} = \text{Total Ore Value} - \min(\text{Total Support Value})$$

### Input Format
* First line: length of the seam $L$ ($1 \le L \le 10{,}000$, width fixed at $W = 4$).
* Following $L$ lines: 4 space-separated integers representing the assayed values $v$ ($1 \le v \le 1{,}000{,}000$) for each row.

---

## 2. Why Greedy Approaches Fail

A greedy algorithm makes a sequence of locally optimal choices, committing permanently to each decision without reconsidering. In this problem, greedy heuristics fail due to two coupled constraints:

### 1. Overlapping $2 \times 2$ Coverage
A single support cell at $(r, c)$ can simultaneously support up to **four** overlapping $2 \times 2$ blocks:
```
  [2x2 Block 1]   [2x2 Block 2]
         \             /
          (r, c) Support
         /             \
  [2x2 Block 3]   [2x2 Block 4]
```
Picking the locally smallest cell in one $2 \times 2$ block misses multi-block synergies, forcing redundant support pillars in neighboring blocks later.

### 2. Global Connectivity Bottlenecks
Support pillars sever transit paths. Consider this example:
```
  1    1    1    1
  1  100  100    1
  1    1    1    1
```
A greedy rule picking the smallest cells to satisfy the $2 \times 2$ constraint might turn surrounding $1$-value cells into supports, permanently isolating the two high-value $100$ cells and rendering them unminable.

---

## 3. The Complete State Space: All 22 Reachable Profiles

Profile DP works because the state of the 4-cell frontier can be compressed into a canonical tuple. There are **exactly 22 distinct reachable states** across the entire algorithm:

```
State Tuple = (comp_0, comp_1, comp_2, comp_3)
  0: Column is unmined (support pillar)
  1, 2, ...: Canonical connected component IDs
```

### Complete Enumeration of All 22 States

#### Special Control States (2 states)
1. **`None`**: Mining has not started yet (all rows above are untouched solid rock).
2. **`'DONE'`**: Mining has concluded (a single connected component was finished; all remaining rows below are supports).

#### 1 Cell Mined (4 profiles)
3. **`(1, 0, 0, 0)`** — Only Column 0 is mined.
4. **`(0, 1, 0, 0)`** — Only Column 1 is mined.
5. **`(0, 0, 1, 0)`** — Only Column 2 is mined.
6. **`(0, 0, 0, 1)`** — Only Column 3 is mined.

#### 2 Cells Mined (9 profiles)
* *Adjacent pairs (merged horizontally into 1 component):*
  7. **`(1, 1, 0, 0)`** — Columns 0 and 1 mined.
  8. **`(0, 1, 1, 0)`** — Columns 1 and 2 mined.
  9. **`(0, 0, 1, 1)`** — Columns 2 and 3 mined.
* *Separated by a gap (connected via ceiling arch above vs. disconnected separate branches):*
  10. **`(1, 0, 1, 0)`** — Columns 0, 2 mined (connected through ceiling above; 1 component).
  11. **`(1, 0, 2, 0)`** — Columns 0, 2 mined (disconnected separate branches; 2 components).
  12. **`(0, 1, 0, 1)`** — Columns 1, 3 mined (connected through ceiling above; 1 component).
  13. **`(0, 1, 0, 2)`** — Columns 1, 3 mined (disconnected separate branches; 2 components).
  14. **`(1, 0, 0, 1)`** — Columns 0, 3 mined (connected through wide ceiling arch above; 1 component).
  15. **`(1, 0, 0, 2)`** — Columns 0, 3 mined (disconnected separate branches; 2 components).

#### 3 Cells Mined (6 profiles)
* *Three contiguous cells (merged horizontally into 1 component):*
  16. **`(1, 1, 1, 0)`** — Columns 0, 1, 2 mined.
  17. **`(0, 1, 1, 1)`** — Columns 1, 2, 3 mined.
* *Separated by a pillar at Column 1:*
  18. **`(1, 0, 1, 1)`** — Column 0 and Columns 2–3 connected through ceiling above (1 component).
  19. **`(1, 0, 2, 2)`** — Column 0 is Comp 1; Columns 2–3 are Comp 2 (2 components).
* *Separated by a pillar at Column 2:*
  20. **`(1, 1, 0, 1)`** — Columns 0–1 and Column 3 connected through ceiling above (1 component).
  21. **`(1, 1, 0, 2)`** — Columns 0–1 are Comp 1; Column 3 is Comp 2 (2 components).

#### 4 Cells Mined (1 profile)
22. **`(1, 1, 1, 1)`** — All 4 cells mined (merged horizontally into 1 component).

> [!NOTE]
> **Why Can't There Be 3 Components (e.g., `(1, 0, 2, 3)`)?**  
> In a 4-wide row, to have 3 separate components you would need 3 mined cells separated by supports. But any selection of 3 cells in a row of 4 must contain at least one adjacent pair (e.g. cols 2 and 3 in `1 0 1 1`), which forces them to merge horizontally into the same ID. Therefore, **at most 2 components can ever coexist simultaneously**.

---

## 4. Multi-Component Lifecycles & Delayed Bridges

### Can Separate Components Exist Across Multiple Rows?
**YES.** A common misconception is that all mined cells must be joined into one component at every single row. 

The DP freely allows multiple components (e.g. `(1, 0, 0, 2)`) to travel downward side-by-side across as many rows as necessary, as long as neither branch is abandoned:

```
Row 0:     [ 1 ]   [ 0 ]   [ 0 ]   [ 2 ]      Profile = (1, 0, 0, 2)
             │                       │
Row 1:     [ 1 ]   [ 0 ]   [ 0 ]   [ 2 ]      Profile = (1, 0, 0, 2)  <-- No bridge here! Perfectly VALID.
             │                       │
Row 2:     [ 1 ────── 1 ────── 1 ──── 1 ]      Profile = (1, 1, 1, 1)  <-- Bridge forms HERE! Merged.
```

* At Row 1, the candidate mask is `[ 1, 0, 0, 1 ]`.
* The DP does **not** require them to connect to each other at Row 1.
* It only checks: *"Did Comp 1 continue downward?"* (Yes) and *"Did Comp 2 continue downward?"* (Yes).
* The profile remains `(1, 0, 0, 2)` until Row 2 provides the horizontal bridge that unifies them.

### Why an Abandoned Component Can NEVER Be Rescued Later
What if Row 1 abandons Component 2, but Row 2 tries to build a bridge `[ 1, 1, 1, 1 ]`?

```
Row 0:     [ 1 ]   [ 0 ]   [ 0 ]   [ 2 ]   <-- Cell (0, 3) was mined!
             │                       X
Row 1:     [ 1 ]   [ 0 ]   [ 0 ]   [ 0 ]   <-- Cell (1, 3) is UNMINED (Solid Rock Support!)
             │                       │
Row 2:     [ 1 ────── 1 ────── 1 ─── 1 ]   <-- Row 2 is all mined
```

Look at Cell $(0, 3)$:
* To its left $(0, 2)$: unmined rock.
* Above it: edge of grid.
* To its right: wall.
* Below it $(1, 3)$: unmined rock support.

**Cell $(0, 3)$ is completely entombed by solid rock.** Under 4-connectivity (rectilinear movement), miners cannot tunnel diagonally or jump through the unmined rock pillar at $(1, 3)$. Once a component fails to extend downward, it is permanently severed and can never be connected by any future row.

---

## 5. Does the DP Ever Modify the Previous Row?

**NO. The previous row is 100% immutable and read-only.**

Time moves strictly forward ($0 \to 1 \to \dots \to L$). The DP never retroactively changes a cell in Row $r-1$ to accommodate Row $r$.

### The "Parallel Universes" Model
DP avoids the need to edit the past because **it already computed and stored every valid alternative configuration of the past**:

When Row $r$ executes, `dp[r-1]` holds all surviving profiles:
```python
dp_prev = {
    (1, 1, 1, 1): cost_A,  # Universe A: all 4 cells mined
    (1, 0, 1, 0): cost_B,  # Universe B: cols 0, 2 mined
    (1, 0, 0, 2): cost_C,  # Universe C: separate side shafts
    ...
}
```
Row $r$ does not edit Universe A, B, or C. It simply tests its candidates against each universe and branches forward into Row $r$.

---

## 6. Higher-Order Extensions: Deeper Forbidden Blocks

What if the ceiling safety rule required avoiding larger blocks?
$$\text{Previous Rows Required in State} = (\text{Height of Forbidden Block}) - 1$$

| Forbidden Block Size | Depth in Rows | Previous Rows Needed in State | State Size ($W = 4$) |
| :--- | :---: | :---: | :--- |
| **$2 \times 2$** (Original) | 2 rows | **1 previous row** (`profile_{r-1}`) | $\approx 22$ states |
| **$3 \text{ wide} \times 2 \text{ tall}$** | 2 rows | **1 previous row** (`profile_{r-1}`) | $\approx 22$ states |
| **$2 \text{ wide} \times 3 \text{ tall}$** | 3 rows | **2 previous rows** (`profile_{r-1}`, `mask_{r-2}`) | $22 \times 16 \approx 352$ states |
| **$3 \times 3$** | 3 rows | **2 previous rows** (`profile_{r-1}`, `mask_{r-2}`) | $22 \times 16 \approx 352$ states |

* If the block is **3 columns wide by 2 rows tall**, it still only spans 2 rows vertically. You only need Row $r-1$ and check triplets of columns $(c, c+1, c+2)$ instead of pairs.
* If the block is **3 rows tall**, you cannot detect an illegal collapse without knowing which cells were mined in Row $r-2$. The state must store the mask of Row $r-2$, multiplying state count by 16.

---

## 7. Time & Space Complexity: Why It Is Strictly $O(L)$

### The Path Funneling Principle
In a brute-force search, paths branch exponentially ($16 \times 16 \times 16 \dots = 16^L$).

In Profile DP, **paths do not multiply forever—they constantly funnel back into the 22 profile buckets**:

```
Row r-1:    22 active profile buckets
               │
               ▼  (Try 16 masks on each profile)
            352 candidate transitions
               │
               ▼  (min() collapses them back into the 22 buckets!)
Row r:      STILL at most 22 profile buckets!
```

Whenever multiple paths arrive at the exact same profile, the DP discards all but the single cheapest one:
```python
next_dp[prof] = min(next_dp.get(prof, float('inf')), cost + sc)
```

Because the state table never exceeds 22 entries:
$$\text{Work per row} \le 22 \text{ profiles} \times 16 \text{ masks} = 352 \text{ operations}$$
$$\text{Total Time} = 352 \times L = \mathcal{O}(L)$$

For the maximum contest constraint $L = 10{,}000$:
$$\text{Total Operations} \approx 3.5 \times 10^6 \approx \mathbf{0.05 \text{ seconds in Python}}$$

---

## 8. Sample 1 Walkthrough

**Input:**
```
11
5  10  6   5
12  8  3   4
8   7 11   8
9  10  8   3
2  12  5  13
4   9  7   5
6   4  2   4
5   1  5   7
6   7  8   4
8   7  3   4
5   6  2   5
```

* **Total Ore Value:** $\sum \text{grid} = 273$
* **Optimal Support Configuration:** Minimum support cost identified by Profile DP is $45$.
* **Final Result:**
  $$\text{Retrievable} = 273 - 45 = \mathbf{228}$$
  $$\text{Remaining} = \mathbf{45}$$
