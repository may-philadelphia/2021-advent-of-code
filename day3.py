import sys
import time
from functools import reduce
from typing import Iterable, Tuple, IO, List


def bit_to_int(c: str) -> int:
    """Processes newlines as 1 for quick-and-dirty line count simultaneously with processing"""
    return 1 if c == '\n' else int(c)


def calculate_gamma_epsilon(data: Iterable[str]) -> Tuple[Tuple[int, ...], Tuple[int, ...], int]:
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
    return gamma, tuple(1 - s for s in gamma), sums[-1]


def tuple_to_int(t: Tuple[int, ...]) -> int:
    """Converts a tuple of bits into an integer"""
    return int(''.join(str(b) for b in t), 2)\


def match_bit_frequency(word_len: int, num_words: int, flag: int, check: str, f: IO):
    return filter_bit_frequency(
        word_len, num_words, flag, check, f, [i * (word_len + 1) for i in range(num_words)]
    )


def filter_bit_frequency(word_len: int, num_words: int, flag: int, check: str, f: IO, candidates: List[int]) -> int:
    """
    Filters the list of candidates to those with most/least common values for each bit

    Memory: O(num_words); Time: O(num_words * word_len)
    ^ both technically upper bounds; significantly lower in practice depending on number of words filtered at each step
    """
    if num_words == 1:
        f.seek(candidates[0] - word_len - 1)
        f.readline()
        return int(f.readline().strip(), 2)
    num_words = bits = 0
    filtered = []
    for word in candidates:
        f.seek(word)
        if f.read(1) == check:
            filtered.append(word + 1)
            num_words += 1
            bits += int(f.read(1))
    return filter_bit_frequency(word_len, num_words, flag, str(abs(flag - (2 * bits) // num_words)), f, filtered)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Please provide input file")
        exit(1)
    with open(sys.argv[1]) as f:
        start = time.time()
        gamma, epsilon, num_words = calculate_gamma_epsilon(iter(f))
        power = tuple_to_int(gamma) * tuple_to_int(epsilon)
        print(f"1st puzzle solution: power={power} in {time.time()-start:.6f} seconds")
        start = time.time()
        o2 = match_bit_frequency(len(gamma), num_words, 0, str(gamma[0]), f)
        co2 = match_bit_frequency(len(epsilon), num_words, 1, str(epsilon[0]), f)
        life_support = o2 * co2
        print(f"2nd puzzle solution: power={life_support} in {time.time()-start:.6f} seconds")
