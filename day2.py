import sys
import time
from functools import reduce
from typing import Iterable, Tuple


def calculate_position(commands: Iterable[str]) -> Tuple[int, int]:
    """
    Calculates position based on simple linear movement

    Memory: O(1); Time: O(len(commands))
    """
    return reduce(
        lambda position, c: {
            "forward":  lambda x, y, n: (x+n, y),
            "down":     lambda x, y, n: (x, y+n),
            "up":       lambda x, y, n: (x, y-n)
        }[c[0]](*position, int(c[1])),
        (c.split() for c in commands),  # c[0] = command; c[1] = value
        (0, 0)
    )


def calculate_aimed_position(commands: Iterable[str]) -> Tuple[int, int, int]:
    """
    Calculates position based on complex aimed movement

    Memory: O(1); Time: O(len(commands))
    """
    return reduce(
        lambda position, c: {
            "forward":  lambda x, y, a, n: (x+n, y+a*n, a),
            "down":     lambda x, y, a, n: (x, y, a+n),
            "up":       lambda x, y, a, n: (x, y, a-n)
        }[c[0]](*position, int(c[1])),
        (c.split() for c in commands),  # c[0] = command; c[1] = value
        (0, 0, 0)
    )


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) < 2:
        print("Please provide input file")
        exit(1)
    with open(sys.argv[1]) as f:
        start = time.time()
        data = list(f.readlines())
        x, y = calculate_position(data)
        print(f"1st puzzle solution: X={x}, Y={y}, X*Y={x*y} in {time.time()-start:.6f} seconds")
        x, y, _ = calculate_aimed_position(data)
        print(f"2nd puzzle solution: X={x}, Y={y}, X*Y={x*y} in {time.time()-start:.6f} seconds")
