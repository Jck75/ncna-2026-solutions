import sys


class DSU:
    """Disjoint Set Union (Union-Find) with path compression."""

    def __init__(self):
        self.parent = {}

    def find(self, x):
        if self.parent.setdefault(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry


def solve(grid):
    R = len(grid)
    if R == 0:
        return 0, 0

    # dp state:
    #   None: mining not started yet
    #   'DONE': mining has finished (all subsequent rows are supports)
    #   tuple of 4 ints: active component IDs in current row (0 for support)
    dp = {None: 0}

    for row in grid:
        # Precompute support cost for all 16 masks (bit c = 1 if mined, 0 if support)
        support_cost = [
            sum(row[c] for c in range(4) if not (mask & (1 << c)))
            for mask in range(16)
        ]
        next_dp = {}

        for state, cost in dp.items():
            for mask in range(16):
                sc = support_cost[mask]
                mined = [(mask >> c) & 1 for c in range(4)]

                # Phase 1: Mining not started yet
                if state is None:
                    if not any(mined):
                        next_dp[None] = min(next_dp.get(None, float('inf')), cost + sc)
                    else:
                        comp = [0] * 4
                        cur_id = 1
                        for c in range(4):
                            if mined[c]:
                                comp[c] = comp[c - 1] if (c > 0 and mined[c - 1]) else cur_id
                                cur_id += (1 if comp[c] == cur_id else 0)
                        next_dp[tuple(comp)] = min(next_dp.get(tuple(comp), float('inf')), cost + sc)

                # Phase 2: Mining already finished
                elif state == 'DONE':
                    if not any(mined):
                        next_dp['DONE'] = min(next_dp.get('DONE', float('inf')), cost + sc)

                # Phase 3: Actively mining
                else:
                    # 1. Check 2x2 ceiling support rule
                    if any(state[c] > 0 and state[c + 1] > 0 and mined[c] and mined[c + 1] for c in range(3)):
                        continue

                    prev_comps = set(x for x in state if x > 0)

                    # 2. Check if mining concludes at this row
                    if not any(mined):
                        if len(prev_comps) <= 1:
                            next_dp['DONE'] = min(next_dp.get('DONE', float('inf')), cost + sc)
                        continue

                    # 3. Connect components using DSU
                    dsu = DSU()
                    for c in range(3):
                        if mined[c] and mined[c + 1]:
                            dsu.union(('curr', c), ('curr', c + 1))
                    for c in range(4):
                        if mined[c] and state[c] > 0:
                            dsu.union(('curr', c), ('prev', state[c]))

                    # 4. Ensure no previous component is abandoned
                    curr_roots = {dsu.find(('curr', c)) for c in range(4) if mined[c]}
                    if any(dsu.find(('prev', p)) not in curr_roots for p in prev_comps):
                        continue

                    # 5. Canonicalize new profile
                    mapping = {}
                    new_prof = []
                    for c in range(4):
                        if mined[c]:
                            root = dsu.find(('curr', c))
                            if root not in mapping:
                                mapping[root] = len(mapping) + 1
                            new_prof.append(mapping[root])
                        else:
                            new_prof.append(0)

                    prof = tuple(new_prof)
                    next_dp[prof] = min(next_dp.get(prof, float('inf')), cost + sc)

        dp = next_dp

    min_remaining = min(
        cost for state, cost in dp.items()
        if state == 'DONE' or (isinstance(state, tuple) and max(state) <= 1)
    )
    total_ore = sum(sum(r) for r in grid)
    return total_ore - min_remaining, min_remaining


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    while True:
        try:
            L_tok = next(it)
        except StopIteration:
            break
        L = int(L_tok)
        grid = [[int(next(it)) for _ in range(4)] for _ in range(L)]
        retrievable, remaining = solve(grid)
        print(f"Retrievable: {retrievable}")
        print(f"Remaining: {remaining}")


if __name__ == '__main__':
    main()
