import sys
import time
from itertools import pairwise, tee
from typing import Iterable, Tuple, T


def iter_window(it: Iterable[T], n: int) -> Iterable[Tuple[T, ...]]:
    tees = tee(it, n)
    # Advance each tee so first starts with item 0, second with item 1, etc.
    for i in range(len(tees)):
        for _ in range(i):
            next(tees[i])
    return zip(*tees)


def count_decreasing_windows(data: Iterable[int], win_len: int) -> int:
    return sum(1 for _ in (filter(lambda i: i[0] < i[1], pairwise(sum(w) for w in iter_window(data, win_len)))))


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) < 2:
        print("Please provide input file")
        exit(1)
    with open(sys.argv[1]) as f:
        data = [int(l) for l in f.readlines()]
        start = time.time()
        print(f"1st puzzle solution: {count_decreasing_windows(data, 1)} in {time.time()-start:.6f} seconds")
        start = time.time()
        print(f"2nd puzzle solution: {count_decreasing_windows(data, 3)} in {time.time()-start:.6f} seconds")
