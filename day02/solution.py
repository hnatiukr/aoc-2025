from typing import NamedTuple

from lib import read_input_lines

INPUT = "day02/input.txt"


class IdRange(NamedTuple):
    start_id: int
    end_id: int


def parse_id_ranges(filename: str) -> list[IdRange]:
    lines = read_input_lines(filename)
    content = "".join(lines)
    range_strings = content.split(",")

    ranges: list[IdRange] = []
    for range_str in range_strings:
        parts = range_str.split("-")
        ranges.append(IdRange(int(parts[0]), int(parts[1])))

    return ranges


def is_repeated_twice(id: int) -> bool:
    id_str = str(id)

    if len(id_str) % 2 != 0:
        return False

    mid = len(id_str) // 2
    left = id_str[:mid]
    right = id_str[mid:]

    return left == right


def sum_invalid_ids_in_range(start_id: int, end_id: int) -> int:
    sum = 0
    for id in range(start_id, end_id + 1):
        if is_repeated_twice(id):
            sum += id

    return sum


def part_1(filename: str) -> int:
    ranges = parse_id_ranges(filename)
    sum = 0
    for range in ranges:
        sum += sum_invalid_ids_in_range(range.start_id, range.end_id)

    return sum


def sum_invalid_ids_with_smudge(start_id: int, end_id: int) -> int:
    sum = 0
    for id in range(start_id, end_id + 1):
        id_str = str(id)
        prefix = ""

        for char in id_str[: len(id_str) // 2]:
            prefix += char
            remaining = id_str.replace(prefix, "")
            if len(remaining) == 0:
                sum += id
                break

    return sum


def part_2(filename: str) -> int:
    ranges = parse_id_ranges(filename)

    sum = 0
    for range in ranges:
        sum += sum_invalid_ids_with_smudge(range.start_id, range.end_id)

    return sum


print(part_1(INPUT))

print(part_2(INPUT))
