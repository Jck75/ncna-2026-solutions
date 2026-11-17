import sys


def dist_to_left(x: int, y: int, d: int) -> int:
    """
    Computes the minimum Manhattan distance for a hand centered at (x, y)
    to reach a valid swatting position on the left side of the fly.

    Valid left swatting position:
      x_target = -(d + 1)
      y_target in [-4, 4]

    The strike zone square [-d, d] x [-d, d] expanded by the hand size (2 x 12)
    creates an obstacle for the hand's center at:
      (-X_obs, X_obs) x (-Y_obs, Y_obs), where X_obs = d + 1, Y_obs = d + 6.
    """
    d = abs(d)
    x_obs = d + 1
    y_obs = d + 6

    if x >= x_obs and abs(y) < y_obs:
        # Hand is on the right side and alongside the obstacle.
        # It must detour either over (y >= y_obs) or under (y <= -y_obs).
        # Horizontal distance: x - (-x_obs) = x + x_obs
        # Vertical detour: min( (y_obs - y) + (y_obs - 4), (y - (-y_obs)) + (-4 - (-y_obs)) )
        #               = 2 * y_obs - 4 - |y| = 2 * d + 8 - |y|
        return (x + x_obs) + (2 * d + 8 - abs(y))
    else:
        # Unobstructed direct rectilinear movement:
        # Move horizontally to -x_obs, and vertically to the closest point in [-4, 4].
        return abs(x + x_obs) + max(0, abs(y) - 4)


def dist_to_right(x: int, y: int, d: int) -> int:
    """
    By bilateral symmetry across the y-axis, reaching the right swatting position
    from (x, y) is equivalent to reaching the left swatting position from (-x, y).
    """
    return dist_to_left(-x, y, d)


def solve_case(x1: int, y1: int, x2: int, y2: int, d: int) -> int:
    """
    Evaluates both hand-to-side assignment options:
      Option 1: Hand 1 -> Left,  Hand 2 -> Right
      Option 2: Hand 1 -> Right, Hand 2 -> Left
    Returns the minimum total movement distance.
    """
    opt1 = dist_to_left(x1, y1, d) + dist_to_right(x2, y2, d)
    opt2 = dist_to_right(x1, y1, d) + dist_to_left(x2, y2, d)
    return min(opt1, opt2)


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    it = iter(input_data)
    while True:
        try:
            tok = next(it)
        except StopIteration:
            break
        x1 = int(tok)
        y1 = int(next(it))
        x2 = int(next(it))
        y2 = int(next(it))
        d = int(next(it))
        print(solve_case(x1, y1, x2, y2, d))


if __name__ == "__main__":
    main()
