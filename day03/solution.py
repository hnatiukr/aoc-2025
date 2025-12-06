from typing import TypeAlias

from lib import read_input_lines

INPUT = "day03/input.txt"

Battery: TypeAlias = int
BatteryList: TypeAlias = list[Battery]
BatteriesLimit: TypeAlias = int


def max_joltage(batteries: BatteryList, limit: BatteriesLimit):
    positions_left = limit
    start = 0
    result: BatteryList = []

    for _ in range(limit):
        positions_left -= 1
        search_end = len(batteries) - positions_left
        selection = batteries[start:search_end]

        max_digit = max(selection)
        max_idx = selection.index(max_digit) + start

        result.append(max_digit)
        start = max_idx + 1

    return int("".join(map(str, result)))


def sum_values(filename: str, limit: BatteriesLimit):
    input_lines = read_input_lines(filename)
    batteries = [list(int(i) for i in row) for row in input_lines]

    total = 0
    for battery_list in batteries:
        total += max_joltage(battery_list, limit)

    return total


def part_1():
    return sum_values(INPUT, 2)


def part_2():
    return sum_values(INPUT, 12)


print(part_1())

print(part_2())
