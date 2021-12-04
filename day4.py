import sys
import time
from functools import reduce
from typing import List, Set, Tuple, IO

Board = Set[Set[int]]


def boards_to_sets(f: IO, board_size: int = 5) -> List[Board]:
    """
    Converts string boards into a set of sets representing all rows & cols (the unit bingo can be won on)

    Memory: O(board_size^2 * number of boards); Time: O(board_size^2 * number of boards)
    Note: saves time recalculating cols later by taking double memory for storing the board as both rows & cols
    """
    board_sets = []
    while f.readline():  # skipping the blanks between boards all sneaky-like
        board_rows = [[int(f.read(3)) for _ in range(board_size)] for _ in range(board_size)]
        board_sets.append(
            frozenset(frozenset(c for c in row) for row in board_rows)                       # Rows
            | frozenset(frozenset(row[i] for row in board_rows) for i in range(board_size))  # Columns
        )
    return board_sets


def bingo(board: Board, called: Set[int]) -> bool:
    """Checks if board won bingo with the set of numbers currently called

    Since rows & cols are both stored in Board data, just checks if any row/col set is as subset of called numbers
    Memory: O(1); Time: O(board_size^2) - https://stackoverflow.com/a/27674336
    """
    return any(s.issubset(called) for s in board)


def fastest_board(calls: List[int], board_sets: List[Board], board_size: int = 5) -> Tuple[Board, Set[int], int]:
    """Finds the first board to win bingo

    Memory: O(board_size^2 * number of boards) - at most adds a full copy of calls, which is necessarily
        much smaller than the board storage
    Time: O(board_size^2 * number of boards * calls) - Not great, but can't really imagine a faster way
    """
    called = set(calls[:board_size])
    last_call = calls[board_size - 1]
    while last_call != calls[-1]:
        for board in board_sets:
            if bingo(board, called):
                return board, called, last_call
        last_call = calls[len(called)]
        called.add(last_call)


def slowest_board(calls: List[int], board_sets: List[Board], board_size: int = 5) -> Tuple[Board, Set[int], int]:
    """Finds the last board to win bingo

    Same as above; slower in practice since finding the slowest board necessitates more rounds of calls
    Memory: O(board_size^2 * number of boards)
    Time: O(board_size^2 * number of boards * calls)
    """
    called = set(calls[:board_size])
    last_call = calls[board_size - 1]
    # Remove boards from the set til there's one left (or no remaining numbers to call)
    while last_call != calls[-1] and len(board_sets) > 1:
        unfinished_boards = []
        for board in board_sets:
            if not bingo(board, called):
                unfinished_boards.append(board)
        last_call = calls[len(called)]
        called.add(last_call)
        board_sets = unfinished_boards
    # If we're down to one board, continue calling numbers til it gets bingo
    board = board_sets.pop()
    while not bingo(board, called) and last_call != calls[-1]:
        last_call = calls[len(called)]
        called.add(last_call)
    return board, called, last_call


def calculate_score(board: Board, called: Set[int], last_call: int) -> int:
    return last_call * sum(reduce(frozenset.union, board) - called)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Please provide input file")
        exit(1)
    with open(sys.argv[1]) as f:
        start = time.time()
        call_numbers = [int(c) for c in f.readline().split(',')]
        boards = boards_to_sets(f)
        board, called, last_call = fastest_board(call_numbers, boards)
        score = calculate_score(board, called, last_call)
        print(f"1st puzzle solution: score={score} in {time.time()-start:.6f} seconds")
        start = time.time()
        board, called, last_call = slowest_board(call_numbers, boards)
        score = calculate_score(board, called, last_call)
        print(f"2nd puzzle solution: score={score} in {time.time()-start:.6f} seconds")
