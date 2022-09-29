from dataclasses import dataclass
from tkinter.messagebox import NO
from typing import List, Optional, Sequence
from xmlrpc.client import boolean


@dataclass
class Node:
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    visited: boolean = False
    in_queue_to_visit: boolean = False


def build_binary_tree(indexes: Sequence[Sequence[int]]) -> List[Node]:
    root = Node(1)
    nodes = [root]
    evaluating_node = root

    for i, idx in enumerate(indexes):
        left, right = idx

        if left != -1:
            left_node = Node(left)
            nodes.append(left_node)
            evaluating_node.left = left_node

        if right != -1:
            right_node = Node(right)
            nodes.append(right_node)
            evaluating_node.right = right_node

        if i + 1 < len(nodes):
            evaluating_node = nodes[i + 1]

    return nodes


def should_visit_node_in_future(node: Optional[Node]) -> bool:
    return node is not None and not node.visited and not node.in_queue_to_visit


def run_in_order_traversal(binary_tree: Sequence[Node]) -> List[int]:
    root = binary_tree[0]
    to_visit_nodes = [root]
    visited_nodes = []

    while len(to_visit_nodes) > 0:
        current_visited_node: Node = to_visit_nodes.pop()
        current_visited_node.in_queue_to_visit = False
        if should_visit_node_in_future(current_visited_node.right):
            to_visit_nodes.append(current_visited_node.right)
            current_visited_node.right.in_queue_to_visit = True

        if should_visit_node_in_future(current_visited_node.left):
            to_visit_nodes.append(current_visited_node)
            to_visit_nodes.append(current_visited_node.left)
            current_visited_node.left.in_queue_to_visit = True
            current_visited_node.in_queue_to_visit = True
        elif not current_visited_node.visited:
            visited_nodes.append(current_visited_node.value)
            current_visited_node.visited = True

    return visited_nodes


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
