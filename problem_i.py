import sys

# Set recursion depth just in case, though the implementation is completely iterative
sys.setrecursionlimit(300000)

MOD = 1000000007

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    w = [0] * (n + 1)
    for i in range(1, n + 1):
        w[i] = int(input_data[i])

    idx = n + 1
    # a has length n - 1 (parents of 2..n in Tree 1)
    adj1 = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        p = int(input_data[idx])
        idx += 1
        adj1[p].append(i)

    # b has length n - 1 (parents of 2..n in Tree 2)
    adj2 = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        p = int(input_data[idx])
        idx += 1
        adj2[p].append(i)

    # If n == 1, there are no lines of descent longer than (1)
    if n == 1:
        print(f"{w[1]} 1")
        return

    # Iterative DFS on Tree 2 to compute entry and exit timestamps (Euler tour intervals)
    # tin2[u] .. tout2[u] defines the contiguous range of all descendants of u in Tree 2
    tin2 = [0] * (n + 1)
    tout2 = [0] * (n + 1)
    stack2 = [1]
    edge_idx2 = [0] * (n + 1)
    timer = 0
    tin2[1] = timer = 1

    while stack2:
        u = stack2[-1]
        if edge_idx2[u] < len(adj2[u]):
            v = adj2[u][edge_idx2[u]]
            edge_idx2[u] += 1
            timer += 1
            tin2[v] = timer
            stack2.append(v)
        else:
            tout2[u] = timer
            stack2.pop()

    # Build iterative Dual Segment Tree
    # Leaves represent positions 1..n in Tree 2's Euler tour
    K = 1
    while K <= n + 2:
        K <<= 1

    # At each node in the segment tree, maintain a stack of (running_max, running_cnt)
    # Because Tree 1 is traversed in DFS order, range additions and deletions occur in LIFO order
    tree_stack = [[] for _ in range(2 * K)]

    def query(pos):
        """Query the maximum (value, count) among all active intervals covering pos."""
        p = K + pos
        b_val = -1
        b_cnt = 0
        while p > 0:
            st = tree_stack[p]
            if st:
                v, c = st[-1]
                if v > b_val:
                    b_val = v
                    b_cnt = c
                elif v == b_val:
                    b_cnt = (b_cnt + c) % MOD
            p //= 2
        return b_val, b_cnt

    def push_range(L, R, val, count):
        """Add (val, count) to canonical nodes covering [L, R]."""
        l = K + L
        r = K + R + 1
        while l < r:
            if l & 1:
                st = tree_stack[l]
                if not st:
                    st.append((val, count))
                else:
                    top_v, top_c = st[-1]
                    if val > top_v:
                        st.append((val, count))
                    elif val == top_v:
                        st.append((val, (top_c + count) % MOD))
                    else:
                        st.append((top_v, top_c))
                l += 1
            if r & 1:
                r -= 1
                st = tree_stack[r]
                if not st:
                    st.append((val, count))
                else:
                    top_v, top_c = st[-1]
                    if val > top_v:
                        st.append((val, count))
                    elif val == top_v:
                        st.append((val, (top_c + count) % MOD))
                    else:
                        st.append((top_v, top_c))
            l //= 2
            r //= 2

    def pop_range(L, R):
        """Remove (val, count) from canonical nodes covering [L, R] upon backtracking."""
        l = K + L
        r = K + R + 1
        while l < r:
            if l & 1:
                tree_stack[l].pop()
                l += 1
            if r & 1:
                r -= 1
                tree_stack[r].pop()
            l //= 2
            r //= 2

    dp = [0] * (n + 1)
    cnt = [0] * (n + 1)

    # Initialize root (person 1)
    dp[1] = w[1]
    cnt[1] = 1
    push_range(tin2[1], tout2[1], dp[1], cnt[1])

    # Iterative DFS on Tree 1
    stack1 = [1]
    edge_idx1 = [0] * (n + 1)

    while stack1:
        u = stack1[-1]
        if edge_idx1[u] < len(adj1[u]):
            v = adj1[u][edge_idx1[u]]
            edge_idx1[u] += 1
            # v is visited: query best predecessor in Tree 2 among ancestors in Tree 1
            b_val, b_cnt = query(tin2[v])
            dp[v] = b_val + w[v]
            cnt[v] = b_cnt % MOD
            # Add v to segment tree for its descendants in Tree 1
            push_range(tin2[v], tout2[v], dp[v], cnt[v])
            stack1.append(v)
        else:
            # Backtrack out of u in Tree 1: remove u's interval
            pop_range(tin2[u], tout2[u])
            stack1.pop()

    # Find global maximum value and the sum of counts attaining that maximum
    max_val = max(dp[1:])
    ans_cnt = sum(cnt[i] for i in range(1, n + 1) if dp[i] == max_val) % MOD

    print(f"{max_val} {ans_cnt}")

if __name__ == '__main__':
    main()
