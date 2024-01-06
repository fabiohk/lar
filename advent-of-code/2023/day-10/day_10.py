from dataclasses import dataclass, field
from enum import StrEnum
from itertools import chain
from queue import SimpleQueue
import logging
import logging.config
from typing import Optional

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": logging.Formatter,
            "format": "%(message)s",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"}
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console"]}
    },
})
logger = logging.getLogger("AoC Day 10")
logger.setLevel(logging.INFO)

class TileType(StrEnum):
    VERTICAL_PIPE = "|"
    HORIZONTAL_PIPE = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"
    GROUND = "."
    STARTING_POSITION = "S"

@dataclass
class Position:
    i: int
    j: int

    def __hash__(self) -> int:
        return hash((self.i, self.j))
    

@dataclass
class Node:
    tile_type: TileType
    node_position: Position
    adjacent_nodes: list[Position] = field(default_factory=list)

@dataclass
class ExpandedNode(Node):
    from_original: bool = False
    original_position: Optional[Position] = None

type Graph = list[list[Node]]
type ExpandedGraph = list[list[ExpandedNode]]

# Djikstra Algorithm
def find_distances_from_source(source: Node, graph: Graph, NOT_CALCULATED_DISTANCE: int) -> list[list[int]]:
    distances = []
    is_node_visited = []
    
    for i, line in enumerate(graph):
        distances.append([])
        is_node_visited.append([])
        for node in line:
            position = node.node_position
            distances[i].append(NOT_CALCULATED_DISTANCE if position != source.node_position else 0)
            is_node_visited[i].append(False)
    queue = SimpleQueue()
    nodes_in_queue = set()
    queue.put(source.node_position)
    nodes_in_queue.add(source.node_position)
        
    while not queue.empty():
        if queue.qsize() > NOT_CALCULATED_DISTANCE ** 2:
            logger.debug("Queue Length: %d", queue.qsize())
        u: Position = queue.get()
        is_node_visited[u.i][u.j] = True

        for v in graph[u.i][u.j].adjacent_nodes:
            if not is_node_visited[v.i][v.j] and Position(v.i, v.j) not in nodes_in_queue:
                queue.put(v)
                nodes_in_queue.add(Position(v.i, v.j))
            probable_distance = distances[u.i][u.j] + 1
            if probable_distance < distances[v.i][v.j]:
                distances[v.i][v.j] = probable_distance

    return distances

def read_input(path: str, start_tile_type: TileType) -> tuple[Node, Graph]:
    graph = []
    with open(path) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            graph_line = []
            stripped_line = line.strip()
            for j, c in enumerate(stripped_line):
                if c == TileType.STARTING_POSITION:
                    node = Node(start_tile_type, Position(i, j))
                    start_node = node
                else:
                    node = Node(c, Position(i, j))
                node.adjacent_nodes = get_adjacent_nodes(node, Position(i, j), len(lines), len(stripped_line))
                graph_line.append(node)
            graph.append(graph_line)
        return start_node, graph
    
def get_adjacent_nodes(node: Node, node_position: Position, n: int, m: int) -> list[Position]:
    possible_adjacents_sum = get_possible_adjacents(node.tile_type)
    adjacents = []

    for (x, y) in possible_adjacents_sum:
        possible_i = node_position.i + x
        possible_j = node_position.j + y
        if 0 <= possible_i < n and 0 <= possible_j < m:
            adjacents.append(Position(possible_i, possible_j))

    return adjacents

def get_possible_adjacents(tile_type: TileType) -> list[tuple[int, int]]:
    match tile_type:
        case TileType.GROUND:
            return []
        case TileType.VERTICAL_PIPE:
            return [(-1, 0), (1, 0)]
        case TileType.HORIZONTAL_PIPE:
            return [(0, -1), (0, 1)]
        case TileType.NORTH_EAST:
            return [(-1, 0), (0, 1)]
        case TileType.NORTH_WEST:
            return [(-1, 0), (0, -1)]
        case TileType.SOUTH_WEST:
            return [(0, -1), (1, 0)]
        case TileType.SOUTH_EAST:
            return [(0, 1), (1, 0)]
        case _:
            return []
        
def expand_graph(graph: Graph, source: Node, print_expanded_graph: bool = False) -> tuple[ExpandedNode, ExpandedGraph]:
    new_graph: ExpandedGraph = []
    new_n, new_m = 3 * len(graph), 3 * len(graph[0])

    for i, line in enumerate(graph):
        new_graph.append([])
        new_graph.append([])
        new_graph.append([])
        for j, node in enumerate(line):
            new_i, new_j = 3 * i, 3 * j
            new_positions = [(new_i, new_j), (new_i, new_j+1), (new_i, new_j+2), (new_i+1, new_j), (new_i+1, new_j+1), (new_i+1, new_j+2), (new_i+2, new_j), (new_i+2, new_j+1), (new_i+2, new_j+2)]
            match node.tile_type:
                case TileType.GROUND:
                    new_nodes_types = [TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND]
                case TileType.VERTICAL_PIPE:
                    new_nodes_types = [TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND, TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND, TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND]
                case TileType.HORIZONTAL_PIPE:
                    new_nodes_types = [TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.HORIZONTAL_PIPE, TileType.HORIZONTAL_PIPE, TileType.HORIZONTAL_PIPE, TileType.GROUND, TileType.GROUND, TileType.GROUND]
                case TileType.NORTH_EAST:
                    new_nodes_types = [TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND, TileType.GROUND, TileType.NORTH_EAST, TileType.HORIZONTAL_PIPE, TileType.GROUND, TileType.GROUND, TileType.GROUND]
                case TileType.NORTH_WEST:
                    new_nodes_types = [TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND, TileType.HORIZONTAL_PIPE, TileType.NORTH_WEST, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND]
                case TileType.SOUTH_WEST:
                    new_nodes_types = [TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.HORIZONTAL_PIPE, TileType.SOUTH_WEST, TileType.GROUND, TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND]
                case TileType.SOUTH_EAST:
                    new_nodes_types = [TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.GROUND, TileType.SOUTH_EAST, TileType.HORIZONTAL_PIPE, TileType.GROUND, TileType.VERTICAL_PIPE, TileType.GROUND]
            for new_position, new_node_type in zip(new_positions, new_nodes_types):
                new_node_i, new_node_j = new_position
                new_node_position = Position(new_node_i, new_node_j)
                new_node = ExpandedNode(new_node_type, new_node_position)
                new_node.adjacent_nodes = get_adjacent_nodes(new_node, new_node_position, new_n, new_m)
                if new_node_position == Position(new_i+1, new_j+1):
                    new_node.from_original = True
                    new_node.original_position = Position(i, j)
                new_graph[new_node_i].append(new_node)

            if source.node_position == Position(i, j):
                new_source = new_graph[new_i+1][new_j+1]

    if print_expanded_graph:
        for line in new_graph:
            for node in line:
                print(node.tile_type, end="")
            print("")

    return new_source, new_graph

def filter_only_calculated_distances(distances: list[list[int]], NOT_CALCULATED_DISTANCE: int) -> list[int]:
    return [distance for distance in chain.from_iterable(distances) if distance != NOT_CALCULATED_DISTANCE]

def get_graph_without_adjacencies_in_loop(graph: Graph, distances: list[list[int]], NOT_CALCULATED_DISTANCE: int) -> Graph:
    new_graph: Graph = []
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


def get_nodes_inside_loop(expanded_graph_distances: list[list[int]], inverted_adjacencies_expanded_graph_distances_top_left: list[list[int]], expanded_graph: ExpandedGraph, NOT_CALCULATED_DISTANCE: int) -> list[ExpandedNode]:
    nodes_inside_loop = []
    for i, distances in enumerate(inverted_adjacencies_expanded_graph_distances_top_left):
        for j, distance in enumerate(distances):
            is_inside_loop = distance == NOT_CALCULATED_DISTANCE and expanded_graph_distances[i][j] == NOT_CALCULATED_DISTANCE
            if is_inside_loop:
                nodes_inside_loop.append(expanded_graph[i][j])
    return nodes_inside_loop

def filter_only_original_nodes(nodes: list[ExpandedNode]) -> list[ExpandedNode]:
    return [node for node in nodes if node.from_original]

def solve(input_path: str, source_tile_type: TileType, debugging_mode: bool = False):
    if debugging_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    print(input_path)
    source, graph = read_input(input_path, source_tile_type)
    NOT_CALCULATED_DISTANCE = len(graph) * len(graph[0]) + 1
    distances = find_distances_from_source(source, graph, NOT_CALCULATED_DISTANCE)
    max_distance = max(distance for distance in chain.from_iterable(distances) if distance != NOT_CALCULATED_DISTANCE)
    print(max_distance)

    new_source, expanded_graph = expand_graph(graph, source, debugging_mode)
    NOT_CALCULATED_DISTANCE = len(expanded_graph) * len(expanded_graph[0]) + 1
    expanded_graph_distances = find_distances_from_source(new_source, expanded_graph, NOT_CALCULATED_DISTANCE)

    inverted_adjacencies_expanded_graph = get_graph_without_adjacencies_in_loop(expanded_graph, expanded_graph_distances, NOT_CALCULATED_DISTANCE)
    logger.debug("Max Distances: %d", NOT_CALCULATED_DISTANCE)
    inverted_adjacencies_expanded_graph_distances_top_left = find_distances_from_source(inverted_adjacencies_expanded_graph[0][0], inverted_adjacencies_expanded_graph, NOT_CALCULATED_DISTANCE)
    logger.debug("EXPANDED GRAPH DISTANCES")
    logger.debug(expanded_graph_distances)
    logger.debug("INVERTED ADJACENCIES DISTANCES TOP LEFT")
    logger.debug(inverted_adjacencies_expanded_graph_distances_top_left)

    nodes_inside_loop = get_nodes_inside_loop(expanded_graph_distances, inverted_adjacencies_expanded_graph_distances_top_left, expanded_graph, NOT_CALCULATED_DISTANCE)
    only_original_nodes_inside_loop = filter_only_original_nodes(nodes_inside_loop)
    logger.debug([(node.original_position, node.tile_type) for node in only_original_nodes_inside_loop])
    print(len(only_original_nodes_inside_loop))
    print("-------------")

solve("./example", TileType.SOUTH_EAST, False)
solve("./example_2", TileType.SOUTH_EAST, False)
solve("./example_3", TileType.SOUTH_EAST, False)
solve("./example_4", TileType.SOUTH_EAST, False)
solve("./example_5", TileType.SOUTH_EAST, False)
solve("./example_6", TileType.SOUTH_WEST, False)
solve("./input", TileType.SOUTH_WEST, False)