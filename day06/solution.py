import operator
from functools import reduce
from typing import Literal, NamedTuple

from lib import read_input_lines

INPUT = "day06/input.txt"

Operator = Literal["+", "*"]
Worksheet = list[list[str]]


class Problem(NamedTuple):
    numbers: list[int]
    operator: Operator


def evaluate_problem(problem: Problem) -> int:
    if problem.operator == "+":
        return sum(problem.numbers)
    else:  # "*"
        return reduce(operator.mul, problem.numbers, 1)


def parse_worksheet_part1(filename: str) -> list[Problem]:
    worksheet: Worksheet = [line.split() for line in read_input_lines(filename)]

    problems: list[Problem] = []
    columns_as_problems = list(zip(*worksheet[::1]))

    for column in columns_as_problems:
        op: Operator = column[-1]  # type: ignore
        numbers = [int(val) for val in column[:-1]]
        problems.append(Problem(numbers, op))

    return problems


def part_1(filename: str) -> int:
    problems = parse_worksheet_part1(filename)

    return sum(evaluate_problem(problem) for problem in problems)


def parse_worksheet_part2(filename: str) -> list[Problem]:
    worksheet_raw = read_input_lines(filename)

    if all(line.endswith("|") for line in worksheet_raw):
        worksheet = [line[:-1] for line in worksheet_raw]
    else:
        max_length = max(len(line) for line in worksheet_raw)
        worksheet = [line.ljust(max_length) for line in worksheet_raw]

    rotated = list(zip(*worksheet[::-1]))
    mirrored = [list(reversed(row)) for row in reversed(rotated)]

    problems: list[Problem] = []
    accumulated_numbers: list[int] = []

    while len(mirrored) > 0:
        column = mirrored.pop(0)
        number_string = "".join(column[:-1]).strip()

        if not number_string.isdigit():
            continue

        accumulated_numbers.append(int(number_string))
        operator_char = column[-1]

        if operator_char in ("+", "*"):
            problems.append(Problem(accumulated_numbers.copy(), operator_char))  # type: ignore
            accumulated_numbers = []

    return problems


def part_2(filename: str) -> int:
    problems = parse_worksheet_part2(filename)

    return sum(evaluate_problem(problem) for problem in problems)


print(part_1(INPUT))

print(part_2(INPUT))
