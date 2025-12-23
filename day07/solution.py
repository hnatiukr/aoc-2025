from functools import cache
from typing import TypeAlias

from lib import read_input_lines

INPUT = "day07/input.txt"

SPLITTER = "^"
EMPTY_CELL = "."
START_MARKER = "S"

Grid: TypeAlias = list[list[str]]
Position: TypeAlias = tuple[int, int]


def part_1(filename: str) -> int:
    grid = [list(row) for row in read_input_lines(filename)]
    start_col = grid[0].index(START_MARKER)

    beam_splits = set()
    beams_to_process = [(0, start_col)]
    visited = set()

    while beams_to_process:
        row, col = beams_to_process.pop()

        if not (0 <= col < len(grid[0])) or (row, col) in visited:
            continue

        visited.add((row, col))

        row += 1
        while row < len(grid):
            cell = grid[row][col]

            if cell == EMPTY_CELL:
                row += 1
                continue

            if cell == SPLITTER:
                beam_splits.add((row, col))
                beams_to_process.append((row, col - 1))
                beams_to_process.append((row, col + 1))
                break

            row += 1

    return len(beam_splits)


def part_2(filename: str) -> int:
    grid = tuple(tuple(row) for row in read_input_lines(filename))
    start_col = grid[0].index(START_MARKER)

    @cache
    def trace_beam(row: int, col: int) -> int:
        if not (0 <= col < len(grid[0])):
            return 0

        timeline_count = 0
        row += 1

        while row < len(grid):
            cell = grid[row][col]

            if cell == EMPTY_CELL:
                row += 1
                continue

            if cell == SPLITTER:
                timeline_count += trace_beam(row, col - 1)
                timeline_count += trace_beam(row, col + 1)
                return timeline_count

            row += 1

        return 1

    return trace_beam(0, start_col)


print(part_1(INPUT))
print(part_2(INPUT))
