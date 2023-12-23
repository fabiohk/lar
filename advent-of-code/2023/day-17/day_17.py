from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from queue import SimpleQueue
from typing import Generator, NamedTuple, Optional

class Direction(StrEnum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    TOP = "TOP"
    DOWN = "DOWN"

class Position(NamedTuple):
    i: int
    j: int
    weight: int = 0

@dataclass
class Node:
    heat_loss: int
    position: Position = field(default_factory=lambda: Position(0, 0))


type Graph = list[list[Node]]

def find_distances_from_source(source: Node, graph: Graph, NOT_CALCULATED_DISTANCE: int) -> dict[tuple[Position, Optional[Direction], int], int]:
    distances = defaultdict(lambda: NOT_CALCULATED_DISTANCE)
    is_node_visited = defaultdict(lambda: False)
    
    queue = SimpleQueue()
    nodes_in_queue = set()
    queue.put((source.position, None, 0))
    distances[(source.position, None, 0)] = 0
    nodes_in_queue.add((source.position, None, 0))
        
    while not queue.empty():
        u, direction, consecutive_nodes = queue.get()
        is_node_visited[(u, direction, consecutive_nodes)] = True

        for adjacent_node in get_adjacent_nodes(graph[u.i][u.j], direction, consecutive_nodes, graph):
            if not is_node_visited[adjacent_node] and adjacent_node not in nodes_in_queue:
                queue.put(adjacent_node)
                nodes_in_queue.add(adjacent_node)
            probable_distance = distances[u, direction, consecutive_nodes] + adjacent_node[0].weight
            if probable_distance < distances[adjacent_node]:
                distances[adjacent_node] = probable_distance
                queue.put(adjacent_node)

    return distances

def get_adjacent_nodes(node: Node, current_direction: Optional[Direction], consecutive_nodes: int, graph: Graph) -> Generator[tuple[Position, Direction, int], None, None]:
    n, m = len(graph), len(graph[0])
    i, j, _ = node.position
    possible_adjacent_nodes_positions = [(Position(i-1, j), Direction.TOP), (Position(i+1, j), Direction.DOWN), (Position(i, j-1), Direction.LEFT), (Position(i, j+1), Direction.RIGHT)]

    for possible_position, new_direction in possible_adjacent_nodes_positions:
        if is_valid_position(possible_position, new_direction, current_direction, consecutive_nodes, n, m):
            k, l, _ = possible_position
            yield (Position(k, l, graph[k][l].heat_loss), new_direction, 1 if new_direction != current_direction else consecutive_nodes + 1)

def is_valid_position(position: Position, new_direction: Direction, current_direction: Direction, consecutive_nodes: int, n: int, m: int) -> bool:
    if new_direction == current_direction and consecutive_nodes == 3:
        return False
    
    if new_direction == Direction.DOWN and current_direction == Direction.TOP:
        return False
    
    if new_direction == Direction.TOP and current_direction == Direction.DOWN:
        return False
    
    if new_direction == Direction.LEFT and current_direction == Direction.RIGHT:
        return False
    
    if new_direction == Direction.RIGHT and current_direction == Direction.LEFT:
        return False

    i, j, _ = position
    return 0 <= i < n and 0 <= j < m
            

def read_input(input_path: str) -> Graph:
    with open(input_path) as f:
        graph = [parse_line(line.strip()) for line in f.readlines()]

        for i, row in enumerate(graph):
            for j, node in enumerate(row):
                node.position = Position(i, j)
        return graph
    
def parse_line(line: str) -> list[Node]:
    return [Node(int(digit)) for digit in line]

def find_distances_from_source_with_crucibles(source: Node, graph: Graph, NOT_CALCULATED_DISTANCE: int) -> dict[tuple[Position, Optional[Direction], int], int]:
    distances = defaultdict(lambda: NOT_CALCULATED_DISTANCE)
    is_node_visited = defaultdict(lambda: False)
    
    queue = SimpleQueue()
    nodes_in_queue = set()
    queue.put((source.position, None, 0))
    distances[(source.position, None, 0)] = 0
    nodes_in_queue.add((source.position, None, 0))
        
    while not queue.empty():
        u, direction, consecutive_nodes = queue.get()
        is_node_visited[(u, direction, consecutive_nodes)] = True
        adjacent_nodes = get_adjacent_nodes_with_crucibles(graph[u.i][u.j], direction, consecutive_nodes, graph)

        for adjacent_node in adjacent_nodes:
            if not is_node_visited[adjacent_node] and adjacent_node not in nodes_in_queue:
                queue.put(adjacent_node)
                nodes_in_queue.add(adjacent_node)
            probable_distance = distances[u, direction, consecutive_nodes] + adjacent_node[0].weight
            if probable_distance < distances[adjacent_node]:
                distances[adjacent_node] = probable_distance
                queue.put(adjacent_node)

    return distances


def get_adjacent_nodes_with_crucibles(node: Node, current_direction: Optional[Direction], consecutive_nodes: int, graph: Graph) -> Generator[tuple[Position, Direction, int], None, None]:
    n, m = len(graph), len(graph[0])
    i, j, _ = node.position
    match current_direction:
        case Direction.TOP:
            possible_adjacent_nodes_positions = [(Position(i-1, j), Direction.TOP), (Position(i+4, j), Direction.DOWN), (Position(i, j-4), Direction.LEFT), (Position(i, j+4), Direction.RIGHT)]
        case Direction.DOWN:
            possible_adjacent_nodes_positions = [(Position(i-4, j), Direction.TOP), (Position(i+1, j), Direction.DOWN), (Position(i, j-4), Direction.LEFT), (Position(i, j+4), Direction.RIGHT)]
        case Direction.LEFT:
            possible_adjacent_nodes_positions = [(Position(i-4, j), Direction.TOP), (Position(i+4, j), Direction.DOWN), (Position(i, j-1), Direction.LEFT), (Position(i, j+4), Direction.RIGHT)]
        case Direction.RIGHT:
            possible_adjacent_nodes_positions = [(Position(i-4, j), Direction.TOP), (Position(i+4, j), Direction.DOWN), (Position(i, j-4), Direction.LEFT), (Position(i, j+1), Direction.RIGHT)]
        case _:
            possible_adjacent_nodes_positions = [(Position(i-4, j), Direction.TOP), (Position(i+4, j), Direction.DOWN), (Position(i, j-4), Direction.LEFT), (Position(i, j+4), Direction.RIGHT)]

    for possible_position, new_direction in possible_adjacent_nodes_positions:
        if is_valid_position_for_crucible(possible_position, new_direction, current_direction, consecutive_nodes, n, m):
            k, l, _ = possible_position
            heat_loss_sum = get_heat_loss_sum(node.position, possible_position, graph)
            yield (Position(k, l, heat_loss_sum), new_direction, 4 if new_direction != current_direction else consecutive_nodes + 1)

def is_valid_position_for_crucible(position: Position, new_direction: Direction, current_direction: Direction, consecutive_nodes: int, n: int, m: int) -> bool:
    if new_direction == current_direction and consecutive_nodes == 10:
        return False
    
    if new_direction == Direction.DOWN and current_direction == Direction.TOP:
        return False
    
    if new_direction == Direction.TOP and current_direction == Direction.DOWN:
        return False
    
    if new_direction == Direction.LEFT and current_direction == Direction.RIGHT:
        return False
    
    if new_direction == Direction.RIGHT and current_direction == Direction.LEFT:
        return False

    i, j, _ = position
    return 0 <= i < n and 0 <= j < m

def get_heat_loss_sum(position: Position, new_position: Position, graph: Graph) -> int:
    i, j, _ = position
    k, l, _ = new_position

    if i == k:
        range_to_consider = range(l, j) if j > l else range(j+1, l+1)
        return sum(graph[i][m].heat_loss for m in range_to_consider)
    range_to_consider = range(k, i) if i > k else range(i+1, k+1)
    return sum(graph[n][j].heat_loss for n in range_to_consider)

graph = read_input("./example")
n, m = len(graph), len(graph[0])
NOT_CALCULATED_DISTANCE = 1_000_000_000
distances = find_distances_from_source(graph[0][0], graph, NOT_CALCULATED_DISTANCE)
min_distance = NOT_CALCULATED_DISTANCE
for key, distance in distances.items():
    position, *_ = key
    if position.i == n-1 and position.j == m-1:
        min_distance = min(min_distance, distance)
print(min_distance)

distances = find_distances_from_source_with_crucibles(graph[0][0], graph, NOT_CALCULATED_DISTANCE)
min_distance = NOT_CALCULATED_DISTANCE
for key, distance in distances.items():
    position, *_ = key
    if position.i == n-1 and position.j == m-1:
        min_distance = min(min_distance, distance)
print(min_distance)

graph = read_input("./example_2")
n, m = len(graph), len(graph[0])
NOT_CALCULATED_DISTANCE = 1_000_000_000
distances = find_distances_from_source_with_crucibles(graph[0][0], graph, NOT_CALCULATED_DISTANCE)
min_distance = NOT_CALCULATED_DISTANCE
for key, distance in distances.items():
    position, *_ = key
    if position.i == n-1 and position.j == m-1:
        min_distance = min(min_distance, distance)
print(min_distance)

graph = read_input("./input")
n, m = len(graph), len(graph[0])
NOT_CALCULATED_DISTANCE = 1_000_000_000
distances = find_distances_from_source(graph[0][0], graph, NOT_CALCULATED_DISTANCE)
min_distance = NOT_CALCULATED_DISTANCE
for key, distance in distances.items():
    position, *_ = key
    if position.i == n-1 and position.j == m-1:
        min_distance = min(min_distance, distance)
print(min_distance)

distances = find_distances_from_source_with_crucibles(graph[0][0], graph, NOT_CALCULATED_DISTANCE)
min_distance = NOT_CALCULATED_DISTANCE
for key, distance in distances.items():
    position, *_ = key
    if position.i == n-1 and position.j == m-1:
        min_distance = min(min_distance, distance)
print(min_distance)