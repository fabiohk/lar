from dataclasses import dataclass
from platform import node
from turtle import left
from typing import Generator, List, Sequence


@dataclass
class Node:
    value: int
    in_queue_to_visit: bool = False
    visited_node: bool = False


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


def should_visit_node(node: Node) -> bool:
    return node.value != -1 and not node.in_queue_to_visit and not node.visited_node


def inorder_nodes(binary_tree: Sequence[Node]) -> Generator[Node, None, None]:
    to_visit_nodes_indices = [0]

    while len(to_visit_nodes_indices) > 0:
        node_idx = to_visit_nodes_indices.pop()
        node = binary_tree[node_idx]
        node.in_queue_to_visit = False
        possible_left_child_idx = (node_idx + 1) * 2 - 1
        possible_right_child_idx = (node_idx + 1) * 2

        if possible_left_child_idx >= len(binary_tree):
            yield node
            node.visited_node = True
            continue

        left_child = binary_tree[possible_left_child_idx]
        right_child = binary_tree[possible_right_child_idx]

        if should_visit_node(right_child):
            to_visit_nodes_indices.append(possible_right_child_idx)
            right_child.in_queue_to_visit = True

        if should_visit_node(left_child):
            to_visit_nodes_indices.append(node_idx)
            node.in_queue_to_visit = True
            to_visit_nodes_indices.append(possible_left_child_idx)
            left_child.in_queue_to_visit = True
        else:
            yield node
            node.visited_node = True


def run_in_order_traversal(binary_tree: Sequence[Node]) -> List[int]:
    return [node.value for node in inorder_nodes(binary_tree) if node.value != -1]


def swap_nodes(binary_tree: Sequence[Node], k: int) -> List[Node]:
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
