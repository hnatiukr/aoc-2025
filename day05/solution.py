from typing import NamedTuple

from lib import read_input_lines

INPUT = "day05/input.txt"


class IngredientRange(NamedTuple):
    start: int
    end: int


def parse_database(filename: str) -> tuple[list[IngredientRange], list[int]]:
    lines = read_input_lines(filename)

    separator_idx = lines.index("")
    range_lines = lines[:separator_idx]
    id_lines = lines[separator_idx + 1 :]

    fresh_ranges: list[IngredientRange] = []
    for line in range_lines:
        start, end = line.split("-")
        fresh_ranges.append(IngredientRange(int(start), int(end)))

    available_ids = [int(line) for line in id_lines]

    return fresh_ranges, available_ids


def is_ingredient_fresh(
    ingredient_id: int, fresh_ranges: list[IngredientRange]
) -> bool:
    for range in fresh_ranges:
        if range.start <= ingredient_id <= range.end:
            return True
    return False


def count_fresh_ingredients(
    available_ids: list[int], fresh_ranges: list[IngredientRange]
) -> int:
    count = 0
    for ingredient_id in available_ids:
        if is_ingredient_fresh(ingredient_id, fresh_ranges):
            count += 1
    return count


def part_1(filename: str) -> int:
    fresh_ranges, available_ids = parse_database(filename)

    return count_fresh_ingredients(available_ids, fresh_ranges)


def ranges_overlap(a: IngredientRange, b: IngredientRange) -> bool:
    return (
        b.start <= a.start <= b.end
        or b.start <= a.end <= b.end
        or a.start <= b.start <= a.end
        or a.start <= b.end <= a.end
    )


def merge_overlapping_ranges(
    fresh_ranges: list[IngredientRange],
) -> list[IngredientRange]:
    ranges = list(fresh_ranges)

    merging = True
    while merging:
        merging = False
        for a_idx, range_a in enumerate(ranges):
            for b_idx, range_b in enumerate(ranges[a_idx + 1 :]):
                if ranges_overlap(range_a, range_b):
                    merging = True
                    merged_start = min(range_a.start, range_b.start)
                    merged_end = max(range_a.end, range_b.end)
                    ranges[a_idx] = IngredientRange(merged_start, merged_end)
                    ranges.pop(a_idx + b_idx + 1)
                    break
            if merging:
                break

    return ranges


def count_total_fresh_ingredients(fresh_ranges: list[IngredientRange]) -> int:
    merged_ranges = merge_overlapping_ranges(fresh_ranges)
    total = sum(range.end - range.start + 1 for range in merged_ranges)

    return total


def part_2(filename: str) -> int:
    fresh_ranges, _ = parse_database(filename)

    return count_total_fresh_ingredients(fresh_ranges)


print(part_1(INPUT))

print(part_2(INPUT))
