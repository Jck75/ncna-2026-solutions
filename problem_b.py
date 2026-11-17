import math
import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    if n <= 1:
        print(0)
        return

    # Parse planets: (distance, arc_length, theta)
    planets = []
    idx = 1
    for _ in range(n):
        d = float(input_data[idx])
        w = float(input_data[idx + 1])
        th = float(input_data[idx + 2])
        planets.append((d, w, th))
        idx += 3

    # Sort planets by distance from the star in ascending order
    planets.sort(key=lambda p: p[0])

    TWO_PI = 2.0 * math.pi
    PI = math.pi
    EPS = 1e-9

    eclipsed_count = 0

    for i in range(n):
        d_i, w_i, th_i = planets[i]

        # Handle point-like planet (arc length effectively zero)
        if w_i <= EPS:
            is_eclipsed = False
            for j in range(i):
                d_j, w_j, th_j = planets[j]
                if d_j >= d_i - EPS:
                    break
                delta = (th_j - th_i + PI) % TWO_PI - PI
                if abs(delta) <= w_j * 0.5 + EPS:
                    is_eclipsed = True
                    break
            if is_eclipsed:
                eclipsed_count += 1
            continue

        L = th_i - w_i * 0.5
        R = th_i + w_i * 0.5

        intervals = []
        covered_single = False

        for j in range(i):
            d_j, w_j, th_j = planets[j]
            if d_j >= d_i - EPS:
                break
            if w_j <= EPS:
                continue

            # Shortest angular displacement from th_i to th_j in [-pi, pi)
            delta = (th_j - th_i + PI) % TWO_PI - PI

            # Quick check if their angular intervals could possibly overlap
            if abs(delta) > (w_i + w_j) * 0.5 + EPS:
                continue

            th_j_prime = th_i + delta
            cl = max(L, th_j_prime - w_j * 0.5)
            cr = min(R, th_j_prime + w_j * 0.5)

            if cl < cr:
                # If this single closer planet completely covers [L, R]
                if cl <= L + EPS and cr >= R - EPS:
                    covered_single = True
                    break
                intervals.append((cl, cr))

        if covered_single:
            eclipsed_count += 1
            continue

        if not intervals:
            continue

        # Check if the union of intervals completely covers [L, R]
        intervals.sort()
        cur = L
        covered = True

        for cl, cr in intervals:
            if cl > cur + EPS:
                covered = False
                break
            if cr > cur:
                cur = cr
            if cur >= R - EPS:
                break

        if cur < R - EPS:
            covered = False

        if covered:
            eclipsed_count += 1

    print(eclipsed_count)


if __name__ == "__main__":
    solve()
