import sys
from collections import deque


def solve():
    """
    Solves Problem E: Rubik's Towers of Hanoi.
    
    Hannah's brother Rubik left the Hanoi puzzle scrambled on 3 pegs.
    We need to find the minimum number of legal moves to bring the puzzle
    to a solved state (all disks stacked on ANY one of the 3 pegs in strictly
    decreasing order of size from bottom to top, meaning largest disk at the
    bottom, smallest at the top).
    
    A legal move allows taking the top disk from any peg and placing it on
    another peg if that other peg is empty or has a strictly larger top disk.
    
    At most 8 disks total, with unique integer diameters <= 100.
    Since N <= 8, the state space is small (at most ~7,300 reachable states),
    and standard Breadth-First Search (BFS) finds the shortest path optimally.
    """
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    it = iter(input_data)
    pegs = []
    all_disks = []
    for _ in range(3):
        count = int(next(it))
        peg = [int(next(it)) for _ in range(count)]
        pegs.append(peg)
        all_disks.extend(peg)

    # In the solved state, all disks are on a single peg, stacked from bottom
    # to top in strictly decreasing order of diameter (largest on bottom, smallest on top).
    sorted_disks = tuple(sorted(all_disks, reverse=True))

    start_state = tuple(tuple(peg) for peg in pegs)

    # Check if the initial configuration is already solved on any peg
    for peg in start_state:
        if peg == sorted_disks:
            print(0)
            return

    # BFS to find the shortest path / minimum number of steps
    queue = deque([start_state])
    dist = {start_state: 0}

    while queue:
        state = queue.popleft()
        d = dist[state]

        for i in range(3):
            if not state[i]:
                continue
            
            disk = state[i][-1]
            rem_i = state[i][:-1]

            for j in range(3):
                if i == j:
                    continue
                
                # Check if moving disk from peg i to peg j is legal:
                # Peg j must be empty, or its top disk must be larger than disk.
                if not state[j] or state[j][-1] > disk:
                    new_peg_j = state[j] + (disk,)

                    # Construct the next state tuple
                    if j == 0:
                        new_state = (
                            new_peg_j,
                            rem_i if i == 1 else state[1],
                            rem_i if i == 2 else state[2],
                        )
                    elif j == 1:
                        new_state = (
                            rem_i if i == 0 else state[0],
                            new_peg_j,
                            rem_i if i == 2 else state[2],
                        )
                    else:
                        new_state = (
                            rem_i if i == 0 else state[0],
                            rem_i if i == 1 else state[1],
                            new_peg_j,
                        )

                    # Early termination check: did we reach the solved state on peg j?
                    if new_state[j] == sorted_disks:
                        print(d + 1)
                        return

                    if new_state not in dist:
                        dist[new_state] = d + 1
                        queue.append(new_state)

    # If all reachable states are explored without reaching a solved state
    print(-1)


if __name__ == "__main__":
    solve()
