from lib import read_input_lines

INPUT = "day01/input.txt"


def parse_rotation(rotation):
    direction = -1 if rotation[0] == "L" else 1
    offset = int(rotation[1:])

    return direction * offset


def part_1(input_path: str):
    movements = [parse_rotation(rotation) for rotation in read_input_lines(input_path)]

    position = 50
    zero_crossings = 0
    for move in movements:
        position += move
        if position % 100 == 0:
            zero_crossings += 1

    return zero_crossings


def count_zero_crossings(movement: int, position: int):
    start = position if movement > 0 else 100 - position
    end = start + abs(movement)
    count = (end // 100) - (start // 100)

    return count


def part_2(input_path: str):
    movements = [parse_rotation(rotation) for rotation in read_input_lines(input_path)]

    position = 50
    zero_crossings = 0
    for move in movements:
        next_position = position + move
        zero_crossings += count_zero_crossings(move, position)
        position = next_position % 100

    return zero_crossings


print(part_1(INPUT))

print(part_2(INPUT))
