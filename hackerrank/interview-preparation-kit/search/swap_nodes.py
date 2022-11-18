from dataclasses import dataclass
from typing import Dict, Generator, List, Mapping, Optional, Sequence


@dataclass
class Node:
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def build_binary_tree(indexes: Sequence[Sequence[int]]) -> List[Node]:
    root = Node(value=1)
    nodes = [root]
    evaluating_node = root

    for i, idx in enumerate(indexes):
        left, right = idx

        if left != -1:
            left_node = Node(value=left)
            nodes.append(left_node)
            evaluating_node.left = left_node

        if right != -1:
            right_node = Node(value=right)
            nodes.append(right_node)
            evaluating_node.right = right_node

        if i + 1 < len(nodes):
            evaluating_node = nodes[i + 1]

    return nodes


def inorder_nodes(node: Optional[Node]) -> Generator[Node, None, None]:
    if node is None:
        return

    yield from inorder_nodes(node.left)
    yield node
    yield from inorder_nodes(node.right)


def run_in_order_traversal(binary_tree: Sequence[Node]) -> List[int]:
    return [node.value for node in inorder_nodes(binary_tree[0])]


def tree_depth(binary_tree: Sequence[Node]) -> int:
    return len(binary_tree) // 2 + 1


def build_nodes_per_depth(binary_tree: Sequence[Node]) -> Dict[int, List[Node]]:
    nodes_per_depth = {}

    to_visit_nodes = [(binary_tree[0], 1)]

    while len(to_visit_nodes) > 0:
        node, node_depth = to_visit_nodes.pop()

        if node_depth not in nodes_per_depth:
            nodes_per_depth[node_depth] = [node]
        else:
            nodes_per_depth[node_depth].append(node)

        if node.right is not None:
            to_visit_nodes.append((node.right, node_depth + 1))

        if node.left is not None:
            to_visit_nodes.append((node.left, node_depth + 1))

    return nodes_per_depth


def swap_childs_from_node(node: Node):
    node.left, node.right = node.right, node.left


def swap_nodes(nodes_per_depth: Mapping[int, Sequence[Node]], k: int) -> List[Node]:
    h = k

    while h in nodes_per_depth:
        for node in nodes_per_depth[h]:
            binary_tree = swap_childs_from_node(node)
        h += k

    return binary_tree


def solution(
    indexes: Sequence[Sequence[int]], queries: Sequence[int]
) -> List[List[int]]:
    # build binary tree
    binary_tree = build_binary_tree(indexes)
    nodes_per_depth = build_nodes_per_depth(binary_tree)
    results = []
    # for each query, swap childs
    for k in queries:
        swap_nodes(nodes_per_depth, k)
        in_order_traversal = run_in_order_traversal(binary_tree)
        results.append(in_order_traversal)

    return results
