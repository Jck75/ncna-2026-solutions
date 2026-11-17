import sys
from collections import deque


def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)

    while True:
        try:
            tok = next(it)
        except StopIteration:
            break
        R = int(tok)
        C = int(next(it))

        # Horizontal borders: (R + 1) lines, each with C integers
        # Vertical borders: R lines, each with (C + 1) integers
        # Alternating: H[0], V[0], H[1], V[1], ..., H[R]
        H = []
        V = []
        for r in range(R):
            H.append([int(next(it)) for _ in range(C)])
            V.append([int(next(it)) for _ in range(C + 1)])
        H.append([int(next(it)) for _ in range(C)])

        target_L = int(next(it))
        target_R = int(next(it))

        # Directions:
        # 0: EAST, 1: SOUTH, 2: WEST, 3: NORTH

        # Entrance (2) and Exit (3) identification
        starts = []
        exits = set()

        for r in range(R + 1):
            for c in range(C):
                if H[r][c] == 2:
                    if r == 0:
                        starts.append(('H', r, c, 1))  # Facing SOUTH into maze
                    elif r == R:
                        starts.append(('H', r, c, 3))  # Facing NORTH into maze
                    else:
                        starts.append(('H', r, c, 1))
                        starts.append(('H', r, c, 3))
                if H[r][c] == 3:
                    if r == 0:
                        exits.add(('H', r, c, 3))  # Facing NORTH out of maze
                    elif r == R:
                        exits.add(('H', r, c, 1))  # Facing SOUTH out of maze
                    else:
                        exits.add(('H', r, c, 1))
                        exits.add(('H', r, c, 3))

        for r in range(R):
            for c in range(C + 1):
                if V[r][c] == 2:
                    if c == 0:
                        starts.append(('V', r, c, 0))  # Facing EAST into maze
                    elif c == C:
                        starts.append(('V', r, c, 2))  # Facing WEST into maze
                    else:
                        starts.append(('V', r, c, 0))
                        starts.append(('V', r, c, 2))
                if V[r][c] == 3:
                    if c == 0:
                        exits.add(('V', r, c, 2))  # Facing WEST out of maze
                    elif c == C:
                        exits.add(('V', r, c, 0))  # Facing EAST out of maze
                    else:
                        exits.add(('V', r, c, 0))
                        exits.add(('V', r, c, 2))

        def is_wall(seg_type, r, c):
            if seg_type == 'H':
                return H[r][c] == 1
            else:
                return V[r][c] == 1

        def get_moves(seg_type, r, c, direction):
            moves = []

            # 1. FORWARD (straight away: dL += 1, dR += 1)
            if seg_type == 'V':
                if direction == 0:  # EAST
                    if c + 1 <= C and not is_wall('V', r, c + 1):
                        moves.append(('V', r, c + 1, 0, 1, 1))
                elif direction == 2:  # WEST
                    if c - 1 >= 0 and not is_wall('V', r, c - 1):
                        moves.append(('V', r, c - 1, 2, 1, 1))
            elif seg_type == 'H':
                if direction == 1:  # SOUTH
                    if r + 1 <= R and not is_wall('H', r + 1, c):
                        moves.append(('H', r + 1, c, 1, 1, 1))
                elif direction == 3:  # NORTH
                    if r - 1 >= 0 and not is_wall('H', r - 1, c):
                        moves.append(('H', r - 1, c, 3, 1, 1))

            # 2. RIGHT TURN (dL += 1, dR += 0: inner wheel R pivots, outer wheel L moves 1)
            if seg_type == 'V':
                if direction == 0:  # EAST -> cell (r, c), lands on H(r+1, c) facing SOUTH
                    if 0 <= r < R and 0 <= c < C and not is_wall('H', r + 1, c):
                        moves.append(('H', r + 1, c, 1, 1, 0))
                elif direction == 2:  # WEST -> cell (r, c-1), lands on H(r, c-1) facing NORTH
                    if 0 <= r < R and 0 <= c - 1 < C and not is_wall('H', r, c - 1):
                        moves.append(('H', r, c - 1, 3, 1, 0))
            elif seg_type == 'H':
                if direction == 1:  # SOUTH -> cell (r, c), lands on V(r, c) facing WEST
                    if 0 <= r < R and 0 <= c < C and not is_wall('V', r, c):
                        moves.append(('V', r, c, 2, 1, 0))
                elif direction == 3:  # NORTH -> cell (r-1, c), lands on V(r-1, c+1) facing EAST
                    if 0 <= r - 1 < R and 0 <= c < C and not is_wall('V', r - 1, c + 1):
                        moves.append(('V', r - 1, c + 1, 0, 1, 0))

            # 3. LEFT TURN (dL += 0, dR += 1: inner wheel L pivots, outer wheel R moves 1)
            if seg_type == 'V':
                if direction == 0:  # EAST -> cell (r, c), lands on H(r, c) facing NORTH
                    if 0 <= r < R and 0 <= c < C and not is_wall('H', r, c):
                        moves.append(('H', r, c, 3, 0, 1))
                elif direction == 2:  # WEST -> cell (r, c-1), lands on H(r+1, c-1) facing SOUTH
                    if 0 <= r < R and 0 <= c - 1 < C and not is_wall('H', r + 1, c - 1):
                        moves.append(('H', r + 1, c - 1, 1, 0, 1))
            elif seg_type == 'H':
                if direction == 1:  # SOUTH -> cell (r, c), lands on V(r, c+1) facing EAST
                    if 0 <= r < R and 0 <= c < C and not is_wall('V', r, c + 1):
                        moves.append(('V', r, c + 1, 0, 0, 1))
                elif direction == 3:  # NORTH -> cell (r-1, c), lands on V(r-1, c) facing WEST
                    if 0 <= r - 1 < R and 0 <= c < C and not is_wall('V', r - 1, c):
                        moves.append(('V', r - 1, c, 2, 0, 1))

            return moves

        # BFS state: (seg_type, r, c, direction, dL, dR)
        q = deque()
        visited = set()

        for s in starts:
            init_state = (s[0], s[1], s[2], s[3], 0, 0)
            visited.add(init_state)
            q.append(init_state)

        possible = False
        while q:
            st, r, c, d, dL, dR = q.popleft()

            if (st, r, c, d) in exits and dL == target_L and dR == target_R:
                possible = True
                break

            for nst, nr, nc, nd, dl, dr in get_moves(st, r, c, d):
                nL = dL + dl
                nR = dR + dr
                if nL <= target_L and nR <= target_R:
                    nstate = (nst, nr, nc, nd, nL, nR)
                    if nstate not in visited:
                        visited.add(nstate)
                        q.append(nstate)

        print("Yes" if possible else "No")


if __name__ == '__main__':
    solve()
