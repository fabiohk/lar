from dataclasses import dataclass
from enum import StrEnum
from queue import SimpleQueue
from typing import NamedTuple

class BeamDirection(StrEnum):
    UPWARD = "UPWARD"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    DOWNWARD = "DOWNWARD"

class Space(StrEnum):
    EMPTY_SPACE = "."
    MIRROR_DOWN_UP = "/"
    MIRROR_UP_DOWN = "\\"
    HORIZONTAL_SPLITTER = "-"
    VERTICAL_SPLITTER = "|"

@dataclass
class Tile:
    space: Space
    energized: bool

class Position(NamedTuple):
    i: int
    j: int

type ContraptionLayout = list[list[Tile]]

def energize_tiles(contraption_layout: ContraptionLayout, beam_direction: BeamDirection, current_position: Position) -> ContraptionLayout:
    energized_contraption_layout = [[Tile(tile.space, False) for tile in row] for row in contraption_layout]
    queue = SimpleQueue()
    queue.put((beam_direction, current_position))
    visited = {}

    while not queue.empty():
        direction, position = queue.get()
        visited[(direction, position)] = True
        i, j = position
        energized_contraption_layout[i][j].energized = True
        possible_directions_and_positions = get_next_possible_directions_and_positions(energized_contraption_layout[i][j].space, direction, position)
        for possible_direction, possible_position in possible_directions_and_positions:
            if is_valid_position(energized_contraption_layout, possible_position) and not alread_visited(possible_direction, possible_position, visited):
                queue.put((possible_direction, possible_position))

    return energized_contraption_layout


def get_next_possible_directions_and_positions(space: Space, beam_direction: BeamDirection, current_position: Position) -> list[tuple[BeamDirection, Position]]:
    i, j = current_position
    left_direction = (BeamDirection.LEFT, Position(i, j-1))
    right_direction = (BeamDirection.RIGHT, Position(i, j+1))
    upward_direction = (BeamDirection.UPWARD, Position(i-1, j))
    downward_direction = (BeamDirection.DOWNWARD, Position(i+1, j))
    if space == Space.EMPTY_SPACE:
        match beam_direction:
            case BeamDirection.UPWARD:
                return [upward_direction]
            case BeamDirection.LEFT:
                return [left_direction]
            case BeamDirection.RIGHT:
                return [right_direction]
            case BeamDirection.DOWNWARD:
                return [downward_direction]
    if space == Space.HORIZONTAL_SPLITTER:
        match beam_direction:
            case BeamDirection.UPWARD | BeamDirection.DOWNWARD:
                return [left_direction, right_direction]
            case BeamDirection.LEFT:
                return [left_direction]
            case BeamDirection.RIGHT:
                return [right_direction]
    if space == Space.VERTICAL_SPLITTER:
        match beam_direction:
            case BeamDirection.UPWARD:
                return [upward_direction]
            case BeamDirection.LEFT | BeamDirection.RIGHT:
                return [upward_direction, downward_direction]
            case BeamDirection.DOWNWARD:
                return [downward_direction]
    if space == Space.MIRROR_DOWN_UP:
        match beam_direction:
            case BeamDirection.UPWARD:
                return [right_direction]
            case BeamDirection.LEFT:
                return [downward_direction]
            case BeamDirection.RIGHT:
                return [upward_direction]
            case BeamDirection.DOWNWARD:
                return [left_direction]
    if space == Space.MIRROR_UP_DOWN:
        match beam_direction:
            case BeamDirection.UPWARD:
                return [left_direction]
            case BeamDirection.LEFT:
                return [upward_direction]
            case BeamDirection.RIGHT:
                return [downward_direction]
            case BeamDirection.DOWNWARD:
                return [right_direction]
            

def is_valid_position(contraption_layout: ContraptionLayout, position: Position) -> bool:
    n, m = len(contraption_layout), len(contraption_layout[0])
    i, j = position
    return 0 <= i < n and 0 <= j < m

def alread_visited(direction: BeamDirection, position: Position, visited: dict[tuple[BeamDirection, Position], bool]) -> bool:
    return (direction, position) in visited


def read_input(input_path: str) -> ContraptionLayout:
    with open(input_path) as f:
        return [parse_line(line) for line in f.readlines()]
    
def parse_line(line: str) -> list[Tile]:
    return [Tile(c, False) for c in line.strip()]

def count_energized_tiles(contraption_layout: ContraptionLayout) -> int:
    counter = 0
    for row in contraption_layout:
        for tile in row:
            if tile.energized:
                counter += 1
    return counter

def max_energized_tiles_starting_from_top_or_bottom(contraption_layout: ContraptionLayout) -> int:
    n, m = len(contraption_layout), len(contraption_layout[0])
    max_energized_tiles = 0
    for j in range(m):
        energized_starting_from_top_contraption = energize_tiles(contraption_layout, BeamDirection.DOWNWARD, Position(0, j))
        energized_starting_from_bottom_contraption = energize_tiles(contraption_layout, BeamDirection.UPWARD, Position(n-1, j))
        max_energized_tiles = max(count_energized_tiles(energized_starting_from_top_contraption), count_energized_tiles(energized_starting_from_bottom_contraption), max_energized_tiles)
    return max_energized_tiles

def max_energized_tiles_starting_from_left_or_right(contraption_layout: ContraptionLayout) -> int:
    n, m = len(contraption_layout), len(contraption_layout[0])
    max_energized_tiles = 0
    for i in range(n):
        energized_starting_from_left_contraption = energize_tiles(contraption_layout, BeamDirection.RIGHT, Position(i, 0))
        energized_starting_from_right_contraption = energize_tiles(contraption_layout, BeamDirection.LEFT, Position(i, m-1))
        max_energized_tiles = max(count_energized_tiles(energized_starting_from_left_contraption), count_energized_tiles(energized_starting_from_right_contraption), max_energized_tiles)
    return max_energized_tiles

contraption_layout = read_input("./example")
energized_contraption = energize_tiles(contraption_layout, BeamDirection.RIGHT, Position(0, 0))
print(count_energized_tiles(energized_contraption))
print(max(max_energized_tiles_starting_from_top_or_bottom(contraption_layout), max_energized_tiles_starting_from_left_or_right(contraption_layout)))

contraption_layout = read_input("./input")
energized_contraption = energize_tiles(contraption_layout, BeamDirection.RIGHT, Position(0, 0))
print(count_energized_tiles(energized_contraption))
print(max(max_energized_tiles_starting_from_top_or_bottom(contraption_layout), max_energized_tiles_starting_from_left_or_right(contraption_layout)))