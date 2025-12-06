from typing import NamedTuple

from lib import read_input_lines

INPUT = "day04/input.txt"


Grid = list[str]

MutableGrid = list[list[str]]


class Position(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    dx: int
    dy: int


DIRECTIONS: list[Direction] = [
    Direction(1, 0),
    Direction(1, 1),
    Direction(0, 1),
    Direction(-1, 1),
    Direction(-1, 0),
    Direction(-1, -1),
    Direction(0, -1),
    Direction(1, -1),
]


def count_adjacent_rolls(grid: Grid, pos: Position, height: int, width: int) -> int:
    count = 0

    for direction in DIRECTIONS:
        nx = pos.x + direction.dx
        ny = pos.y + direction.dy

        if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] == "@":
            count += 1

    return count


def find_accessible_rolls(grid: Grid) -> list[Position]:
    accessible: list[Position] = []
    height = len(grid)
    width = len(grid[0]) if grid else 0

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                pos = Position(x, y)
                adjacent_count = count_adjacent_rolls(grid, pos, height, width)
                if adjacent_count < 4:
                    accessible.append(pos)

    return accessible


def get_accessible_rolls(filename: str) -> int:
    grid: Grid = read_input_lines(filename)
    accessible_rolls = find_accessible_rolls(grid)

    return len(accessible_rolls)


def part_1() -> int:
    return get_accessible_rolls(INPUT)


def grid_to_mutable(grid: Grid) -> MutableGrid:
    return [list(row) for row in grid]


def find_accessible_rolls_mutable(grid: MutableGrid) -> list[Position]:
    accessible: list[Position] = []
    height = len(grid)
    width = len(grid[0]) if grid else 0

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                pos = Position(x, y)
                adjacent_count = count_adjacent_rolls_mutable(grid, pos, height, width)
                if adjacent_count < 4:
                    accessible.append(pos)

    return accessible


def count_adjacent_rolls_mutable(
    grid: MutableGrid, pos: Position, height: int, width: int
) -> int:
    count = 0
    for direction in DIRECTIONS:
        nx = pos.x + direction.dx
        ny = pos.y + direction.dy
        if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] == "@":
            count += 1

    return count


def count_total_accessible_rolls(filename: str) -> int:
    grid: MutableGrid = grid_to_mutable(read_input_lines(filename))
    total = 0

    while True:
        accessible_rolls = find_accessible_rolls_mutable(grid)
        if not accessible_rolls:
            break

        total += len(accessible_rolls)

        for pos in accessible_rolls:
            grid[pos.y][pos.x] = "."

    return total


def part_2() -> int:
    return count_total_accessible_rolls(INPUT)


print(part_1())

print(part_2())
