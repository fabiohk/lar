from dataclasses import dataclass
from platform import node
from re import L
from turtle import left
from typing import Generator, List, Sequence


@dataclass
class Node:
    value: int


def possible_left_idx(node_idx: int) -> int:
    return (node_idx + 1) * 2 - 1


def possible_right_idx(node_idx: int) -> int:
    return (node_idx + 1) * 2


def next_valid_node(nodes: List[Node], possible_valid_node_idx: int) -> int:
    while nodes[possible_valid_node_idx].value == -1:
        possible_valid_node_idx += 1
    return possible_valid_node_idx


def build_binary_tree(indexes: Sequence[Sequence[int]]) -> List[Node]:
    nodes = [Node(1)]
    node_idx = -1
    for left, right in indexes:
        node_idx = next_valid_node(nodes, node_idx)
        nodes.append(Node(left))
        nodes.append(Node(right))

    return nodes


def should_visit_node(node: Node, in_queue_to_visit: bool, visited_node: bool) -> bool:
    return node.value != -1 and not in_queue_to_visit and not visited_node


def inorder_nodes(binary_tree: Sequence[Node]) -> Generator[Node, None, None]:
    to_visit_nodes_indices = [0]
    in_queue_map = [False for _ in range(len(binary_tree))]
    visited_node_map = [False for _ in range(len(binary_tree))]

    while len(to_visit_nodes_indices) > 0:
        node_idx = to_visit_nodes_indices.pop()
        node = binary_tree[node_idx]
        in_queue_map[node_idx] = False
        possible_left_child_idx = possible_left_idx(node_idx)
        possible_right_child_idx = possible_right_idx(node_idx)

        if possible_left_child_idx >= len(binary_tree):
            yield node
            visited_node_map[node_idx] = True
            continue

        left_child = binary_tree[possible_left_child_idx]
        right_child = binary_tree[possible_right_child_idx]

        if should_visit_node(
            right_child,
            in_queue_map[possible_right_child_idx],
            visited_node_map[possible_right_child_idx],
        ):
            to_visit_nodes_indices.append(possible_right_child_idx)
            in_queue_map[possible_right_child_idx] = True

        if should_visit_node(
            left_child,
            in_queue_map[possible_left_child_idx],
            visited_node_map[possible_left_child_idx],
        ):
            to_visit_nodes_indices.append(node_idx)
            in_queue_map[node_idx] = True
            to_visit_nodes_indices.append(possible_left_child_idx)
            in_queue_map[possible_left_child_idx] = True
        else:
            yield node
            visited_node_map[node_idx] = True


def run_in_order_traversal(binary_tree: Sequence[Node]) -> List[int]:
    return [node.value for node in inorder_nodes(binary_tree) if node.value != -1]


def nodes_idx_from_depth(depth: int) -> Generator[int, None, None]:
    start = 2 ** (depth - 1) - 1
    not_inclusive_end = 2 ** (depth) - 1
    for i in range(start, not_inclusive_end):
        yield i


def swap_elements_from_list(
    list_to_swap: Sequence[Node], idx_a: int, idx_b: int
) -> Sequence[Node]:
    list_to_swap[idx_a], list_to_swap[idx_b] = list_to_swap[idx_b], list_to_swap[idx_a]
    return list_to_swap


def swap_childs_from_node(binary_tree: Sequence[Node], node_idx: int) -> List[Node]:
    possible_left_child_idx = possible_left_idx(node_idx)
    possible_right_child_idx = possible_right_idx(node_idx)

    if possible_left_child_idx >= len(binary_tree):
        return binary_tree

    return swap_elements_from_list(
        binary_tree, possible_left_child_idx, possible_right_child_idx
    )


def swap_nodes(binary_tree: Sequence[Node], k: int) -> List[Node]:
    tree_depth = len(binary_tree) // 2 + 1
    h = k

    while h < tree_depth:
        for node_idx in nodes_idx_from_depth(h):
            binary_tree = swap_childs_from_node(binary_tree, node_idx)
        h += k

    return binary_tree


def solution(
    indexes: Sequence[Sequence[int]], queries: Sequence[int]
) -> List[List[int]]:
    # build binary tree
    binary_tree = build_binary_tree(indexes)

    results = []
    # for each query, swap childs
    for k in queries:
        binary_tree = swap_nodes(binary_tree, k)
        in_order_traversal = run_in_order_traversal(binary_tree)
        results.append(in_order_traversal)

    return results
