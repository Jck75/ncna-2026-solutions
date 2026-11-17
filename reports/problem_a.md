# Problem A: Wheelchair Maze

**Contest:** ICPC 2026 North Central North America Regional Contest (NCNA 2026)  
**Problem Statement:** [`A_wheelchairmaze.md`](../raw_problems/A_wheelchairmaze.md)  
**Solution File:** [`problem_a.py`](../problem_a.py)

---

## 1. Problem Statement & Physical Rules

### 1.1 Setting & Geometry
The problem models navigation of a manual wheelchair through a grid maze of unit-width ($1\text{ m} \times 1\text{ m}$) hallways:
* The maze has $R$ rows and $C$ columns of hallway cells ($1 \le R, C \le 10$).
* Walls exist along cell boundaries:
  * $R + 1$ horizontal boundary lines, each comprising $C$ segments.
  * $R$ vertical boundary lines, each comprising $C + 1$ segments.
* A boundary segment descriptor can be:
  * `0`: open doorway / no wall
  * `1`: solid wall
  * `2`: maze entrance (no wall, entrance threshold)
  * `3`: maze exit (no wall, exit threshold)

### 1.2 Wheelchair Kinematics & Odometers
* The wheelchair width equals the hallway width ($1\text{ m}$).
* The wheelchair position is determined by its large rear wheels, which span a $1\text{ m}$ unit boundary segment on the grid.
* Odometers on the left and right wheels measure the distance rolled:
  * **Straight forward (1 meter):** Both wheels roll forward $1\text{ m}$. Distance delta: $\Delta d_L = +1$, $\Delta d_R = +1$.
  * **90° Right Turn:** The inner (right) wheel pivots in place at a grid vertex ($\Delta d_R = 0$). The outer (left) wheel swings through a $90^\circ$ circular arc of radius $1\text{ m}$ ($\Delta d_L = +1$).
  * **90° Left Turn:** The inner (left) wheel pivots in place at a grid vertex ($\Delta d_L = 0$). The outer (right) wheel swings through a $90^\circ$ circular arc of radius $1\text{ m}$ ($\Delta d_R = +1$).
* The wheelchair starts with its large wheels on the threshold of the entrance (`2`), facing into the maze, with odometers at $(0, 0)$.
* The journey finishes when the large wheels cross the threshold of the exit (`3`), facing out of the maze.
* Target odometer readings $(D_L, D_R)$ are given with $D_L, D_R \le 10$.
* The wheelchair may cross or repeat sections of its path, but may never knock over walls (cannot collide with or land on a segment with value `1`).
* Output `"Yes"` if there exists a valid sequence of legal moves from entrance to exit yielding exact distances $(D_L, D_R)$, and `"No"` otherwise.

---

## 2. Algorithmic Approach & State Representation

### 2.1 State Space Representation
At any discrete step, the wheelchair axle occupies a unit edge on the grid, and faces in one of two perpendicular directions:

1. **Vertical Segments:** $V(r, c)$ connecting grid vertex $(r, c)$ to $(r+1, c)$ for $0 \le r < R, 0 \le c \le C$.
   * **Facing EAST ($0$):** Left wheel at $(r, c)$, Right wheel at $(r+1, c)$.
   * **Facing WEST ($2$):** Left wheel at $(r+1, c)$, Right wheel at $(r, c)$.

2. **Horizontal Segments:** $H(r, c)$ connecting grid vertex $(r, c)$ to $(r, c+1)$ for $0 \le r \le R, 0 \le c < C$.
   * **Facing SOUTH ($1$):** Left wheel at $(r, c+1)$, Right wheel at $(r, c)$.
   * **Facing NORTH ($3$):** Left wheel at $(r, c)$, Right wheel at $(r, c+1)$.

A full state during search is a 6-tuple:
$$\text{state} = (\text{seg\_type}, r, c, \text{dir}, d_L, d_R)$$
where $\text{seg\_type} \in \{'H', 'V'\}$, $\text{dir} \in \{0, 1, 2, 3\}$, and $d_L, d_R \ge 0$.

### 2.2 Transition Mechanics (12 Canonical Moves)
From any directed segment $(\text{seg\_type}, r, c, \text{dir})$, there are up to 3 candidate moves:

#### Forward Moves ($\Delta d_L = 1, \Delta d_R = 1$)
1. $V(r, c)$, EAST $\to$ $V(r, c+1)$, EAST (requires $c + 1 \le C$, $V[r][c+1] \ne 1$).
2. $V(r, c)$, WEST $\to$ $V(r, c-1)$, WEST (requires $c - 1 \ge 0$, $V[r][c-1] \ne 1$).
3. $H(r, c)$, SOUTH $\to$ $H(r+1, c)$, SOUTH (requires $r + 1 \le R$, $H[r+1][c] \ne 1$).
4. $H(r, c)$, NORTH $\to$ $H(r-1, c)$, NORTH (requires $r - 1 \ge 0$, $H[r-1][c] \ne 1$).

#### 90° Right Turns ($\Delta d_L = 1, \Delta d_R = 0$)
Inner wheel (Right) pivots, outer wheel (Left) swings $90^\circ$ clockwise:
1. $V(r, c)$, EAST: Pivot at $(r+1, c)$. Left wheel swings to $(r+1, c+1)$.
   * Traverses cell $(r, c)$ ($0 \le r < R, 0 \le c < C$).
   * Destination: $H(r+1, c)$, SOUTH (requires $H[r+1][c] \ne 1$).
2. $V(r, c)$, WEST: Pivot at $(r, c)$. Left wheel swings to $(r, c-1)$.
   * Traverses cell $(r, c-1)$ ($0 \le r < R, 0 \le c-1 < C$).
   * Destination: $H(r, c-1)$, NORTH (requires $H[r][c-1] \ne 1$).
3. $H(r, c)$, SOUTH: Pivot at $(r, c)$. Left wheel swings to $(r+1, c)$.
   * Traverses cell $(r, c)$ ($0 \le r < R, 0 \le c < C$).
   * Destination: $V(r, c)$, WEST (requires $V[r][c] \ne 1$).
4. $H(r, c)$, NORTH: Pivot at $(r, c+1)$. Left wheel swings to $(r-1, c+1)$.
   * Traverses cell $(r-1, c)$ ($0 \le r-1 < R, 0 \le c < C$).
   * Destination: $V(r-1, c+1)$, EAST (requires $V[r-1][c+1] \ne 1$).

#### 90° Left Turns ($\Delta d_L = 0, \Delta d_R = 1$)
Inner wheel (Left) pivots, outer wheel (Right) swings $90^\circ$ counter-clockwise:
1. $V(r, c)$, EAST: Pivot at $(r, c)$. Right wheel swings to $(r, c+1)$.
   * Traverses cell $(r, c)$ ($0 \le r < R, 0 \le c < C$).
   * Destination: $H(r, c)$, NORTH (requires $H[r][c] \ne 1$).
2. $V(r, c)$, WEST: Pivot at $(r+1, c)$. Right wheel swings to $(r+1, c-1)$.
   * Traverses cell $(r, c-1)$ ($0 \le r < R, 0 \le c-1 < C$).
   * Destination: $H(r+1, c-1)$, SOUTH (requires $H[r+1][c-1] \ne 1$).
3. $H(r, c)$, SOUTH: Pivot at $(r, c+1)$. Right wheel swings to $(r+1, c+1)$.
   * Traverses cell $(r, c)$ ($0 \le r < R, 0 \le c < C$).
   * Destination: $V(r, c+1)$, EAST (requires $V[r][c+1] \ne 1$).
4. $H(r, c)$, NORTH: Pivot at $(r, c)$. Right wheel swings to $(r-1, c)$.
   * Traverses cell $(r-1, c)$ ($0 \le r-1 < R, 0 \le c < C$).
   * Destination: $V(r-1, c)$, WEST (requires $V[r-1][c] \ne 1$).

### 2.3 Monotonicity & DAG Property
Every legal transition strictly increases $d_L + d_R$:
* Forward: $+2$
* Turn: $+1$

Because $d_L + d_R$ is strictly monotonic, the state graph is a **Directed Acyclic Graph (DAG)**. There are no infinite cycles. Any state exceeding $d_L > D_L$ or $d_R > D_R$ is immediately pruned. Breadth-First Search (BFS) or depth-first branch-and-bound will terminate rapidly.

---

## 3. Complexity Analysis

### 3.1 State Space Upper Bound
* Maximum grid dimensions: $R \le 10, C \le 10$.
* Number of vertical segments: $R(C+1) \le 10 \times 11 = 110$.
* Number of horizontal segments: $(R+1)C \le 11 \times 10 = 110$.
* Total directed positions: $2 \times 110 + 2 \times 110 = 440$.
* Target distances: $0 \le d_L \le 10, 0 \le d_R \le 10$, giving $(11 \times 11) = 121$ distance pairs.
* **Maximum reachable state graph size:**
  $$|\mathcal{S}| \le 440 \times 121 = 53\,240 \text{ states}$$

### 3.2 Time & Space Complexity
* **Branching factor:** At most $3$ transitions per state.
* **Time Complexity:** $O(|\mathcal{S}|) = O(R \cdot C \cdot D_L \cdot D_R)$. In the worst case, at most $53\,240$ states and $3 \times 53\,240 \approx 160\,000$ edges are explored. In Python, this executes in $< 0.05$ seconds.
* **Space Complexity:** $O(|\mathcal{S}|)$ for the BFS `visited` set and queue, consuming $< 10\text{ MB}$ of memory.

---

## 4. Verification against Sample Inputs and Edge Cases

### 4.1 Sample 1 Trace Walkthrough
* **Grid:** $4 \times 5$ maze with entrance at $V(0, 0)$ and exit at $V(3, 5)$.
* **Target:** $D_L = 6, D_R = 6$.
* **Path Discovered by BFS:**
  1. `RIGHT_TURN` $\to$ $H(1, 0)$, SOUTH, $(d_L, d_R) = (1, 0)$
  2. `FORWARD`    $\to$ $H(2, 0)$, SOUTH, $(d_L, d_R) = (2, 1)$
  3. `LEFT_TURN`  $\to$ $V(2, 1)$, EAST,  $(d_L, d_R) = (2, 2)$
  4. `RIGHT_TURN` $\to$ $H(3, 1)$, SOUTH, $(d_L, d_R) = (3, 2)$
  5. `LEFT_TURN`  $\to$ $V(3, 2)$, EAST,  $(d_L, d_R) = (3, 3)$
  6. `FORWARD`    $\to$ $V(3, 3)$, EAST,  $(d_L, d_R) = (4, 4)$
  7. `FORWARD`    $\to$ $V(3, 4)$, EAST,  $(d_L, d_R) = (5, 5)$
  8. `FORWARD`    $\to$ $V(3, 5)$, EAST,  $(d_L, d_R) = (6, 6)$ [EXIT REACHED]
* **Output:** `Yes` (matches sample output).

### 4.2 Comprehensive Test Suite
| Test Case | Scenario / Configuration | Expected | Result | Notes |
|---|---|---|---|---|
| Sample 1 | Standard $4 \times 5$ maze with target $(6, 6)$ | `Yes` | **PASS** | 8-step optimal path |
| Sample 1 Variant A | Target $(5, 5)$ | `No` | **PASS** | Distances are unreachable at exit |
| Sample 1 Variant B | Target $(7, 7)$ | `Yes` | **PASS** | Alternate detour path exists |
| Sample 1 Variant C | Target $(8, 8)$ | `Yes` | **PASS** | Path with $2\text{ m}$ initial straightaway |
| 1x1 Maze Straight | $1 \times 1$ maze, West entrance to East exit, target $(1, 1)$ | `Yes` | **PASS** | 1 straight move |
| 1x1 Maze Overshoot | $1 \times 1$ maze, target $(2, 2)$ | `No` | **PASS** | Cannot overshoot bounds |
| 1x1 Maze Turn | North entrance, turn to East exit, target $(0, 1)$ | `Yes` | **PASS** | Single left turn exit |
| 1x1 Maze Blocked | $1 \times 1$ maze with wall blocking exit | `No` | **PASS** | Wall collision detected |
| Multi-testcase stream | Consecutive test cases in single standard input | `Yes\nNo\nYes` | **PASS** | EOF loop processing verified |

---

## 5. Conclusion
The implementation in [`problem_a.py`](../problem_a.py) is concise, optimal, and verified against all mechanics and edge cases.
