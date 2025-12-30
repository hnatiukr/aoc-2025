import math
from typing import NamedTuple, TypeAlias

from lib import read_input_lines

INPUT = "day08/input.txt"

Position: TypeAlias = tuple[int, int, int]
Circuit: TypeAlias = set[Position]


class Connection(NamedTuple):
    distance: float
    box_a: Position
    box_b: Position


def parse_junction_boxes(filename: str) -> list[Position]:
    return [
        tuple(int(coord) for coord in line.split(","))  # type: ignore
        for line in read_input_lines(filename)
    ]


def calculate_distance(pos_a: Position, pos_b: Position) -> float:
    x1, y1, z1 = pos_a
    x2, y2, z2 = pos_b

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def generate_potential_connections(boxes: list[Position]) -> list[Connection]:
    connections: list[Connection] = []

    for idx, box_a in enumerate(boxes):
        for box_b in boxes[idx + 1 :]:
            distance = calculate_distance(box_a, box_b)
            connections.append(Connection(distance, box_a, box_b))

    connections.sort(key=lambda c: c.distance)

    return connections


def build_circuits(boxes: list[Position], max_connections: int) -> list[Circuit]:
    connections_processed = 0
    circuits: list[Circuit] = [{box} for box in boxes]
    potential_connections = generate_potential_connections(boxes)

    for connection in potential_connections:
        if connections_processed >= max_connections or len(circuits) <= 1:
            break

        connections_processed += 1

        circuit_indices: list[int] = []
        for idx, circuit in enumerate(circuits):
            if connection.box_a in circuit or connection.box_b in circuit:
                circuit_indices.append(idx)

        if len(circuit_indices) == 1:
            continue

        if len(circuit_indices) == 2:
            circuits[circuit_indices[0]] = circuits[circuit_indices[0]].union(
                circuits[circuit_indices[1]]
            )
            circuits.pop(circuit_indices[1])

    return circuits


def build_circuits_until_one(boxes: list[Position]) -> int:
    final_connection: Connection | None = None
    circuits: list[Circuit] = [{box} for box in boxes]
    potential_connections = generate_potential_connections(boxes)

    for connection in potential_connections:
        if len(circuits) <= 1:
            break

        circuit_indices: list[int] = []
        for idx, circuit in enumerate(circuits):
            if connection.box_a in circuit or connection.box_b in circuit:
                circuit_indices.append(idx)

        if len(circuit_indices) == 1:
            continue

        if len(circuit_indices) == 2:
            final_connection = connection
            circuits[circuit_indices[0]] = circuits[circuit_indices[0]].union(
                circuits[circuit_indices[1]]
            )
            circuits.pop(circuit_indices[1])

    if final_connection:
        return final_connection.box_a[0] * final_connection.box_b[0]

    return 0


def calculate_result(circuits: list[Circuit]) -> int:
    sorted_circuits = sorted(circuits, key=len, reverse=True)

    if len(sorted_circuits) < 3:
        return 0

    return len(sorted_circuits[0]) * len(sorted_circuits[1]) * len(sorted_circuits[2])


def part_1(filename: str) -> int:
    boxes = parse_junction_boxes(filename)
    circuits = build_circuits(boxes, max_connections=1000)

    return calculate_result(circuits)


def part_2(filename: str) -> int:
    boxes = parse_junction_boxes(filename)

    return build_circuits_until_one(boxes)


print(part_1(INPUT))

print(part_2(INPUT))
