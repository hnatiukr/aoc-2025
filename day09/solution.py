from typing import TypeAlias

from lib import read_input_lines

INPUT = "day09/input.txt"

Point: TypeAlias = tuple[int, int]
LineSegment: TypeAlias = tuple[Point, Point]


def parse_red_tiles(filename: str) -> list[Point]:
    return [
        tuple(int(coord) for coord in line.split(","))  # type: ignore
        for line in read_input_lines(filename)
    ]


def calculate_rectangle_area(point_a: Point, point_b: Point) -> int:
    x1, y1 = point_a
    x2, y2 = point_b

    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1

    return width * height


def part_1(filename: str) -> int:
    red_tiles = parse_red_tiles(filename)
    largest_area = 0

    for idx, tile_a in enumerate(red_tiles):
        for tile_b in red_tiles[idx + 1 :]:
            area = calculate_rectangle_area(tile_a, tile_b)
            largest_area = max(largest_area, area)

    return largest_area


def generate_border_points(point_a: Point, point_b: Point) -> set[Point]:
    points = set()
    x_min, x_max = min(point_a[0], point_b[0]), max(point_a[0], point_b[0])
    y_min, y_max = min(point_a[1], point_b[1]), max(point_a[1], point_b[1])

    # horizontal edges
    points.update((x, point_a[1]) for x in range(x_min, x_max + 1))
    points.update((x, point_b[1]) for x in range(x_min, x_max + 1))

    # vertical edges
    points.update((point_a[0], y) for y in range(y_min, y_max + 1))
    points.update((point_b[0], y) for y in range(y_min, y_max + 1))

    return points


def segments_intersect(segment_a: LineSegment, segment_b: LineSegment) -> bool:
    point_a1, point_a2 = sorted(segment_a)
    point_b1, point_b2 = sorted(segment_b)

    if (
        point_b1[0] < point_a1[0] < point_b2[0]
        and point_b1[0] < point_a2[0] < point_b2[0]
        and point_a1[1] < point_b1[1] < point_a2[1]
        and point_a1[1] < point_b2[1] < point_a2[1]
    ):
        return True

    if (
        point_b1[1] < point_a1[1] < point_b2[1]
        and point_b1[1] < point_a2[1] < point_b2[1]
        and point_a1[0] < point_b1[0] < point_a2[0]
        and point_a1[0] < point_b2[0] < point_a2[0]
    ):
        return True

    return False


def is_rectangle_outside_boundary(
    point_a: Point, point_b: Point, boundary_by_row: dict[int, list[int]]
) -> bool:
    if point_a[1] not in boundary_by_row or point_b[1] not in boundary_by_row:
        return True

    row_a_x_coords = boundary_by_row[point_a[1]]
    row_b_x_coords = boundary_by_row[point_b[1]]

    if not row_a_x_coords or not row_b_x_coords:
        return True

    x_min = min(point_a[0], point_b[0])
    x_max = max(point_a[0], point_b[0])

    return (
        x_min < min(row_a_x_coords)
        or x_max > max(row_a_x_coords)
        or x_min < min(row_b_x_coords)
        or x_max > max(row_b_x_coords)
    )


def part_2(filename: str) -> int:
    red_tiles = parse_red_tiles(filename)

    tile_loop = red_tiles + [red_tiles[0]]

    # Build boundary representation
    boundary_by_row: dict[int, list[int]] = {}
    boundary_segments: set[LineSegment] = set()

    for idx in range(len(tile_loop) - 1):
        current_tile = tile_loop[idx]
        next_tile = tile_loop[idx + 1]

        # Record all border points
        border_points = generate_border_points(current_tile, next_tile)
        for point in border_points:
            if point[1] not in boundary_by_row:
                boundary_by_row[point[1]] = []
            boundary_by_row[point[1]].append(point[0])

        boundary_segments.add((current_tile, next_tile))

    largest_area = 0

    for idx, tile_a in enumerate(red_tiles):
        potential_rectangles = [
            (calculate_rectangle_area(tile_a, tile_b), tile_b)
            for tile_b in red_tiles[idx + 1 :]
        ]

        for potential_area, tile_b in sorted(potential_rectangles, reverse=True):
            if potential_area <= largest_area:
                continue

            if is_rectangle_outside_boundary(tile_a, tile_b, boundary_by_row):
                continue

            rectangle_edges = [
                (tile_a, (tile_a[0], tile_b[1])),
                ((tile_a[0], tile_b[1]), tile_b),
                (tile_a, (tile_b[0], tile_a[1])),
                ((tile_b[0], tile_a[1]), tile_b),
            ]

            is_valid = True
            for rect_edge in rectangle_edges:
                for boundary_segment in boundary_segments:
                    if segments_intersect(boundary_segment, rect_edge):
                        is_valid = False
                        break
                if not is_valid:
                    break

            if is_valid:
                largest_area = potential_area
                break

    return largest_area


print(part_1(INPUT))
print(part_2(INPUT))
