import sys
import time
from functools import reduce
from typing import Iterable, Tuple


def bit_to_int(c: str) -> int:
    """Processes newlines as 1 for quick-and-dirty line count simultaneously with processing"""
    return 1 if c == '\n' else int(c)


def calculate_gamma_epsilon(data: Iterable[str]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    """Calculates bit frequency by position. Gamma is most frequent; epsilon is least frequent

    Sums all 1s by bit position, then calculates frequency by dividing by count of data points
    Memory: O(1); Time: O(word length * number of words)
    """
    sums = reduce(
        lambda sums, cur: [bit_to_int(c)+s for s, c in zip(sums, cur)],
        data,
        [bit_to_int(c) for c in next(data)]  # initialize w/ first line b/c we don't know word length
    )
    gamma = tuple(s // (sums[-1] // 2) for s in sums[:-1])
    return gamma, tuple(1 - s for s in gamma)


def tuple_to_int(t: Tuple[int, ...]) -> int:
    """Converts a tuple of bits into an integer"""
    return int(''.join(str(b) for b in t), 2)


def calculate_life_support(gamma: Tuple[int, ...], epsilon: Tuple[int, ...], data: Iterable[str]) -> int:
    checks = [epsilon, gamma]
    vals = [None, None]
    precisions = [0, 0]
    for word in data:
        word = word.strip()
        flag = None
        for i, char in enumerate(int(c) for c in word):
            if i == 0:
                flag = int(char == checks[1][0])
            else:
                if char != checks[flag][i]:
                    if i > precisions[flag]:
                        precisions[flag] = i
                        vals[flag] = word
                    break
        else:
            vals[flag] = word
            precisions[flag] = i
    print(vals, precisions)
    print(checks)
    print(int(vals[0], 2), int(vals[1], 2))
    return int(vals[0], 2) * int(vals[1], 2)


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) < 2:
        print("Please provide input file")
        exit(1)
    with open(sys.argv[1]) as f:
        start = time.time()
        gamma, epsilon = calculate_gamma_epsilon(iter(f))
        power = tuple_to_int(gamma) * tuple_to_int(epsilon)
        print(f"1st puzzle solution: power={power} in {time.time()-start:.6f} seconds")
        f.seek(0)
        start = time.time()
        life_support = calculate_life_support(gamma, epsilon, iter(f))
        print(f"2nd puzzle solution: power={life_support} in {time.time()-start:.6f} seconds")
        # start = time.time()
        # x, y, _ = calculate_aimed_position(data)
        # print(f"2nd puzzle solution: X={x}, Y={y}, X*Y={x*y} in {time.time()-start:.6f} seconds")
