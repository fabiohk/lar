from enum import StrEnum
from functools import cache


class RockShape(StrEnum):
    ROUND = "O"
    CUBE = "#"
    EMPTY = "."

type Platform = tuple[tuple[RockShape]]

@cache
def tilt_north(platform: Platform) -> Platform:
    tilted_platform = [list(platform[0])]

    for row in platform[1:]:
        new_row = []
        for j, rock_shape in enumerate(row):
            if rock_shape == RockShape.ROUND:
                i = find_row_to_place_round_rock_after_north_tilt(tilted_platform, j)
                if i < len(tilted_platform):
                    tilted_platform[i][j] = RockShape.ROUND
                    new_row.append(RockShape.EMPTY)
                else:
                    new_row.append(RockShape.ROUND)
            else:
                new_row.append(rock_shape)
        tilted_platform.append(new_row)

    return tuple(tuple(row) for row in tilted_platform)

def find_row_to_place_round_rock_after_north_tilt(platform: Platform, j: int) -> int:
    i = len(platform) - 1
    while i >= 0 and platform[i][j] == RockShape.EMPTY:
        i -= 1
    return i + 1

@cache
def tilt_west(platform: Platform) -> Platform:
    rotated_platform = rotate_clockwise(platform)
    tilted_platform = tilt_north(rotated_platform)
    return rotate_counterclockwise(tilted_platform)

@cache
def tilt_south(platform: Platform) -> Platform:
    rotated_platform = rotate_clockwise(rotate_clockwise(platform))
    tilted_platform = tilt_north(rotated_platform)
    return rotate_clockwise(rotate_clockwise(tilted_platform))

@cache
def tilt_east(platform: Platform) -> Platform:
    rotated_platform = rotate_counterclockwise(platform)
    tilted_platform = tilt_north(rotated_platform)
    return rotate_clockwise(tilted_platform)

def rotate_clockwise(platform: Platform) -> Platform:
    n, m = len(platform), len(platform[0])
    new_platform = empty_space(m, n)

    for j in range(m):
        for i in range(n):
            new_platform[j][i] = platform[n-i-1][j]

    return tuple(tuple(row) for row in new_platform)

def rotate_counterclockwise(platform: Platform) -> Platform:
    n, m = len(platform), len(platform[0])
    new_platform = empty_space(m, n)

    for j in range(m):
        for i in range(n):
            new_platform[j][i] = platform[i][m-j-1] # j = 0, i = 0

    return tuple(tuple(row) for row in new_platform)

def empty_space(n: int, m: int) -> list[list[RockShape]]:
    platform: Platform = []

    for i in range(n):
        platform.append([])
        for _ in range(m):
            platform[i].append(RockShape.EMPTY)

    return platform

def count_round_rocks(row: tuple[RockShape]) -> int:
    return sum(1 for rock_shape in row if rock_shape == RockShape.ROUND)

def sum_total_load(platform: Platform) -> int:
    rows_to_south_edge = len(platform)
    total_load = 0
    for row in platform:
        total_load += count_round_rocks(row) * rows_to_south_edge
        rows_to_south_edge -= 1
    return total_load

def read_input(input_path: str) -> Platform:
    with open(input_path) as f:
        return tuple(tuple(line.strip()) for line in f.readlines())
    
def spin_platform(platform: Platform, cycles: int) -> Platform:
    for i in range(cycles):
        platform = tilt_east(tilt_south(tilt_west(tilt_north(platform))))
        if i % 1_000 == 0:
            print(i)
            print(f"Tilt East Cache Hits: {tilt_east.cache_info()}")
            print(f"Tilt South Cache: {tilt_south.cache_info()}")
            print(f"Tilt West Cache: {tilt_west.cache_info()}")
            print(f"Tilt North Cache: {tilt_north.cache_info()}")
    return platform
    
platform = read_input("./example")
tilted_platform = tilt_north(platform)
print(sum_total_load(tilted_platform))
spinned_platform = spin_platform(platform, 20)
print(sum_total_load(spinned_platform))

platform = read_input("./input")
tilted_platform = tilt_north(platform)
print(sum_total_load(tilted_platform))
spinned_platform = spin_platform(platform, 230)
print(sum_total_load(spinned_platform))