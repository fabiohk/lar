from copy import copy
from ctypes import Union
from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Position:
    i: int
    j: int

@dataclass
class Galaxy:
    position: Position

class Space(StrEnum):
    EMPTY_SPACE = "."
    GALAXY = "#"

type UniverseImage = list[list[Space]]

def find_distances_between_every_pair_of_galaxy(galaxies: list[Galaxy]) -> list[int]:
    distances = []

    for i, galaxy_a in enumerate(galaxies):
        for galaxy_b in galaxies[i:]:
            min_distance = calculate_min_distance_between_galaxies(galaxy_a, galaxy_b)
            distances.append(min_distance)

    return distances

def calculate_min_distance_between_galaxies(galaxy_a: Galaxy, galaxy_b: Galaxy) -> int:
    return abs(galaxy_a.position.i - galaxy_b.position.i) + abs(galaxy_a.position.j - galaxy_b.position.j)

def expand_universe(universe_image: UniverseImage) -> UniverseImage:
    return column_expansion(row_expansion(universe_image))

def row_expansion(universe_image: UniverseImage) -> UniverseImage:
    new_universe_image = []

    for row in universe_image:
        new_universe_image.append(row)
        if no_galaxies(row):
            new_universe_image.append([space for space in row])
        
    return new_universe_image

def no_galaxies(spaces: list[Space]) -> bool:
    return all(space == Space.EMPTY_SPACE for space in spaces)

def column_expansion(universe_image: UniverseImage) -> UniverseImage:
    return rotate_counterclockwise(row_expansion(rotate_clockwise(universe_image)))

def rotate_clockwise(universe_image: UniverseImage) -> UniverseImage:
    n, m = len(universe_image), len(universe_image[0])
    new_universe_image = empty_space(m, n)

    for j in range(m):
        for i in range(n):
            new_universe_image[j][i] = universe_image[n-i-1][j]

    return new_universe_image
    
def empty_space(n: int, m: int) -> UniverseImage:
    universe_image: UniverseImage = []

    for i in range(n):
        universe_image.append([])
        for _ in range(m):
            universe_image[i].append(Space.EMPTY_SPACE)

    return universe_image

def rotate_counterclockwise(universe_image: UniverseImage) -> UniverseImage:
    n, m = len(universe_image), len(universe_image[0])
    new_universe_image = empty_space(m, n)

    for j in range(m):
        for i in range(n):
            new_universe_image[j][i] = universe_image[i][m-j-1] # j = 0, i = 0

    return new_universe_image

def read_input(input_path: str) -> UniverseImage:
    universe_image = []
    with open(input_path) as f:
        for line in f.readlines():
            row = [c for c in line.strip()]
            universe_image.append(row)

        return universe_image
    
def find_galaxies(universe_image: UniverseImage) -> list[Galaxy]:
    galaxies = []

    for i, line in enumerate(universe_image):
        for j, space in enumerate(line):
            if space == Space.GALAXY:
                galaxies.append(Galaxy(Position(i, j)))

    return galaxies

def find_new_galaxy_position(galaxy: Galaxy, expansion_ratio: int, original_universe_image: UniverseImage) -> Galaxy:
    empty_rows_indexes = [i for i, row in enumerate(original_universe_image) if no_galaxies(row)]
    empty_columns_indexes = [j for j, column in enumerate(rotate_clockwise(original_universe_image)) if no_galaxies(column)]

    rows_to_consider_in_expansion = [i for i in empty_rows_indexes if i < galaxy.position.i]
    columns_to_consider_in_expansion = [j for j in empty_columns_indexes if j < galaxy.position.j]

    new_position_i = len(rows_to_consider_in_expansion) * (expansion_ratio - 1) + galaxy.position.i
    new_position_j = len(columns_to_consider_in_expansion) * (expansion_ratio - 1) + galaxy.position.j

    return Galaxy(Position(new_position_i, new_position_j))


universe_image = read_input("./example")
expanded_universe_image = expand_universe(universe_image)
galaxies = find_galaxies(expanded_universe_image)
original_galaxies = find_galaxies(universe_image)
pair_distances_between_galaxies = find_distances_between_every_pair_of_galaxy(galaxies)
print(sum(pair_distances_between_galaxies))
print(sum(find_distances_between_every_pair_of_galaxy([find_new_galaxy_position(galaxy, 10, universe_image) for galaxy in original_galaxies])))
print(sum(find_distances_between_every_pair_of_galaxy([find_new_galaxy_position(galaxy, 100, universe_image) for galaxy in original_galaxies])))

universe_image = read_input("./input")
expanded_universe_image = expand_universe(universe_image)
galaxies = find_galaxies(expanded_universe_image)
original_galaxies = find_galaxies(universe_image)
pair_distances_between_galaxies = find_distances_between_every_pair_of_galaxy(galaxies)
print(sum(pair_distances_between_galaxies))
print(sum(find_distances_between_every_pair_of_galaxy([find_new_galaxy_position(galaxy, 2, universe_image) for galaxy in original_galaxies])))
print(sum(find_distances_between_every_pair_of_galaxy([find_new_galaxy_position(galaxy, 1_000_000, universe_image) for galaxy in original_galaxies])))