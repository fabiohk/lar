from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from queue import SimpleQueue
import re
from typing import NamedTuple, Union

class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclass
class DigStep:
    direction: Direction
    meters: int
    color: str

class Terrain(StrEnum):
    TRENCH = "#"
    GROUND_LEVEL = "."

class Position(NamedTuple):
    i: int
    j: int

@dataclass
class Node:
    terrain: Terrain
    adjacent_nodes: list[Position] = field(default_factory=list)

type Map = list[list[Terrain]]
type MapWithAdjacentNodes = list[list[Node]]

def dig_edges(dig_steps: list[DigStep], map: Map, start_position: Position) -> Map:
    new_map = copy_map(map)
    i, j = start_position
    max_i, min_i = i, i
    max_j, min_j = j, j
    for dig_step in dig_steps:
        direction, meters = dig_step.direction, dig_step.meters
        max_i, min_i = max(i, max_i), min(i, min_i)
        max_j, min_j = max(j, max_j), min(j, min_j)
        for _ in range(meters):
            match direction:
                case Direction.UP:
                    i -= 1
                case Direction.DOWN:
                    i += 1
                case Direction.LEFT:
                    j -= 1
                case Direction.RIGHT:
                    j += 1
            new_map[i][j] = Terrain.TRENCH
    print_min_max(max_i, min_i, max_j, min_j)
    return new_map

def print_min_max(max_i: int, min_i: int, max_j: int, min_j):
    print(max_i, min_i)
    print(max_j, min_j)


def dig_interior(map: Map, inside_loop_position: Position, within_loop_position: Position) -> Map:
    new_map = copy_map(map)
    map_with_adjacent_nodes = build_map_with_adjacent_nodes(new_map)
    NOT_CALCULATED_DISTANCE = len(map_with_adjacent_nodes) * len(map_with_adjacent_nodes[0]) + 1
    distances = find_distances_from_source(inside_loop_position, map_with_adjacent_nodes, NOT_CALCULATED_DISTANCE)
    inverted_adjacencies_map = get_graph_without_adjacencies_in_loop(map_with_adjacent_nodes)
    inverted_adjacencies_map_distances_from_node_inside_loop = find_distances_from_source(within_loop_position, inverted_adjacencies_map, NOT_CALCULATED_DISTANCE)
    positions_inside_loop: list[Position] = get_positions_inside_loop(distances, inverted_adjacencies_map_distances_from_node_inside_loop, NOT_CALCULATED_DISTANCE)

    for k, l in positions_inside_loop:
        new_map[k][l] = Terrain.TRENCH

    for i, row in enumerate(distances):
        for j, distance in enumerate(row):
            if distance != NOT_CALCULATED_DISTANCE:
                new_map[i][j] = Terrain.TRENCH
    return new_map

def print_map(map: Map):
    for row in map:
        for terrain in row:
            print(terrain, end="")
        print()

def print_edges(distances: list[list[int]], NOT_CALCULATED_DISTANCE: int):
    for row in distances:
        for distance in row:
            if distance != NOT_CALCULATED_DISTANCE:
                print(Terrain.TRENCH, end="")
            else:
                print(Terrain.GROUND_LEVEL, end="")
        print()

def build_map_with_adjacent_nodes(map: Map) -> MapWithAdjacentNodes:
    new_map: MapWithAdjacentNodes = []
    for i, row in enumerate(map):
        new_row = []
        for j, terrain in enumerate(row):
            adjacent_nodes = get_adjacent_nodes(Position(i, j), map)
            new_row.append(Node(terrain, adjacent_nodes))
        new_map.append(new_row)
    return new_map

def get_adjacent_nodes(position: Position, map: Map) -> list[Position]:
    i, j = position
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]

    return [Position(k, l) for k, l in neighbors if map[i][j] == Terrain.TRENCH and is_valid(Position(k, l), map) and map[k][l] == Terrain.TRENCH]

def is_valid(position: Position, map: Union[Map, MapWithAdjacentNodes]) -> bool:
    n, m = len(map), len(map[0])
    i, j = position
    return 0 <= i < n and 0 <= j < m


def find_distances_from_source(source: Position, graph: MapWithAdjacentNodes, NOT_CALCULATED_DISTANCE: int) -> list[list[int]]:
    distances = []
    is_node_visited: dict[Position, bool] = defaultdict(lambda: False)
    
    for i in range(len(graph)):
        distances.append([])
        for j in range(len(graph[0])):
            position = Position(i, j)
            distances[i].append(NOT_CALCULATED_DISTANCE if position != source else 0)
    queue = SimpleQueue()
    nodes_in_queue = set()
    queue.put(source)
    nodes_in_queue.add(source)
        
    while not queue.empty():
        u: Position = queue.get()
        is_node_visited[u] = True

        for v in graph[u.i][u.j].adjacent_nodes:
            if not is_node_visited[v] and v not in nodes_in_queue:
                queue.put(v)
                nodes_in_queue.add(v)
            probable_distance = distances[u.i][u.j] + 1
            if probable_distance < distances[v.i][v.j]:
                distances[v.i][v.j] = probable_distance
                queue.put(v)
        
    return distances

def get_graph_without_adjacencies_in_loop(graph: MapWithAdjacentNodes) -> MapWithAdjacentNodes:
    new_graph: MapWithAdjacentNodes = []

    for i, line in enumerate(graph):
        new_graph.append([])
        for j, node in enumerate(line):
            new_node = Node(node.terrain)
            if node.terrain == Terrain.GROUND_LEVEL:
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for k, l in neighbors:
                    if is_valid(Position(k, l), graph) and graph[k][l].terrain == Terrain.GROUND_LEVEL:
                        new_node.adjacent_nodes.append(Position(k, l))
            new_graph[i].append(new_node)

    return new_graph

def get_graph_without_adjacencies_in_loop2(graph: MapWithAdjacentNodes, distances: list[list[int]], NOT_CALCULATED_DISTANCE: int) -> MapWithAdjacentNodes:
    new_graph: MapWithAdjacentNodes = []
    n, m = len(graph), len(graph[0])

    for i, line in enumerate(graph):
        new_graph.append([])
        for j, node in enumerate(line):
            new_node = Node(node.tile_type, node.node_position)
            if i >= 1 and distances[i][j] == NOT_CALCULATED_DISTANCE:
                new_node.adjacent_nodes.append(Position(i-1, j))
            if j >= 1 and distances[i][j] == NOT_CALCULATED_DISTANCE:
                new_node.adjacent_nodes.append(Position(i, j-1))
            if i + 1 < n and distances[i][j] == NOT_CALCULATED_DISTANCE:
                new_node.adjacent_nodes.append(Position(i+1, j))
            if j + 1 < m and distances[i][j] == NOT_CALCULATED_DISTANCE:
                new_node.adjacent_nodes.append(Position(i, j+1))
            new_graph[i].append(new_node)

    return new_graph

def get_positions_inside_loop(distances_from_top_left: list[list[int]], inverted_adjacencies_map_distances_from_node_inside_loop: list[list[int]], NOT_CALCULATED_DISTANCE: int) -> list[Position]:
    nodes_inside_loop = []
    for i, distances in enumerate(inverted_adjacencies_map_distances_from_node_inside_loop):
        for j, distance in enumerate(distances):
            is_inside_loop = distance != NOT_CALCULATED_DISTANCE and distances_from_top_left[i][j] == NOT_CALCULATED_DISTANCE
            if is_inside_loop:
                nodes_inside_loop.append(Position(i, j))
    return nodes_inside_loop


def copy_map(map: Map) -> Map:
    return [[terrain for terrain in row] for row in map]


def read_input(input_path: str) -> list[DigStep]:
    with open(input_path) as f:
        return [parse_line(line.strip()) for line in f.readlines()]
    
def parse_line(line: str) -> DigStep:
    direction, meters, color = line.split(" ")
    return DigStep(direction, int(meters), color)


def count_trenches_terrain(map: Map) -> int:
    counter = 0
    for row in map:
        for terrain in row:
            if terrain == Terrain.TRENCH:
                counter += 1
    return counter


def ground_level_map(n: int, m: int) -> Map:
    return [[Terrain.GROUND_LEVEL for __ in range(m)] for _ in range(n)]

def convert_color_to_step(color: str) -> DigStep:
    digits_only: str = re.sub(r"[\(|\)|#]*", "", color)
    direction = digits_only[-1]
    hexadecimal = digits_only[:-1]
    return DigStep(translate_direction(int(direction)), int(hexadecimal, 16), color)


def translate_direction(direction_int: int) -> Direction:
    match direction_int:
        case 0:
            return Direction.RIGHT
        case 1:
            return Direction.DOWN
        case 2:
            return Direction.LEFT
        case 3:
            return Direction.UP

# Shoelace formula
def calculate_area(positions: list[Position]) -> int:
    determinant_sum = sum(calculate_2_x_2_matrix_determinant([x, y]) for x, y in zip(positions, positions[1:] + [positions[0]]))
    return abs(determinant_sum) // 2

def calculate_2_x_2_matrix_determinant(matrix: list[Position]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

# Pick's theorem
# Area = interior_points + boundary_points/2 - 1
# Area + 1 = interior_points + boundary_points/2
# Area + 1 + boundary_points/2 = interior_points + boundary_points
def count_trenches_terrain_using_area(area: int, boundary_points: int) -> int:
    return area + boundary_points // 2 + 1


def get_vertices_positions(dig_steps: list[DigStep], start_position: Position) -> list[Position]:
    vertices_positions = []
    i, j = start_position
    max_i, min_i = i, i
    max_j, min_j = j, j
    for dig_step in dig_steps:
        direction, meters = dig_step.direction, dig_step.meters
        max_i, min_i = max(i, max_i), min(i, min_i)
        max_j, min_j = max(j, max_j), min(j, min_j)
        match direction:
            case Direction.UP:
                i -= meters
            case Direction.DOWN:
                i += meters
            case Direction.LEFT:
                j -= meters
            case Direction.RIGHT:
                j += meters
        vertices_positions.append(Position(i, j))
    print_min_max(max_i, min_i, max_j, min_j)
    return vertices_positions

def count_boundary_positions(vertices_positions: list[Position]) -> int:
    return sum(abs(x.i - y.i) + abs(x.j - y.j) for x, y in zip(vertices_positions, vertices_positions[1:] + [vertices_positions[0]]))


steps = read_input("./example")
map = dig_edges(steps, ground_level_map(10, 7), Position(0, 0))
interior_digged = dig_interior(map, Position(0, 0), Position(1, 1))
print(count_trenches_terrain(interior_digged))
vertices_positions = get_vertices_positions(steps, Position(0, 0))
area = calculate_area(vertices_positions)
boundary_positions_count = count_boundary_positions(vertices_positions)
print(count_trenches_terrain_using_area(area, boundary_positions_count))
new_steps = [convert_color_to_step(step.color) for step in steps]
vertices_positions = get_vertices_positions(new_steps, Position(0, 0))
area = calculate_area(vertices_positions)
boundary_positions_count = count_boundary_positions(vertices_positions)
print(count_trenches_terrain_using_area(area, boundary_positions_count))

steps = read_input("./input")
map = dig_edges(steps, ground_level_map(450, 450), Position(212, 97))
interior_digged = dig_interior(map, Position(212, 97), Position(124, 1))
print(count_trenches_terrain(interior_digged))
vertices_positions = get_vertices_positions(steps, Position(212, 97))
area = calculate_area(vertices_positions)
boundary_positions_count = count_boundary_positions(vertices_positions)
print(count_trenches_terrain_using_area(area, boundary_positions_count))
new_steps = [convert_color_to_step(step.color) for step in steps]
vertices_positions = get_vertices_positions(new_steps, Position(21135647, 4132937))
area = calculate_area(vertices_positions)
boundary_positions_count = count_boundary_positions(vertices_positions)
print(count_trenches_terrain_using_area(area, boundary_positions_count))