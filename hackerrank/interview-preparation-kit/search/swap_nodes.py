from dataclasses import dataclass
from typing import List, Optional, Sequence


@dataclass
class Node:
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def solution(
    indexes: Sequence[Sequence[int]], queries: Sequence[int]
) -> List[List[int]]:
    # build binary tree
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

    # for each query, swap childs
    # run in-order and append result
    print(nodes)
    return []
