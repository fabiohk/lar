import enum
from collections import defaultdict
from typing import Dict, List, NamedTuple, Sequence


class Solution(NamedTuple):
    smaller_id: int
    larger_id: int


def solver(costs: Sequence[int], money: int) -> Solution:
    costs_and_ids_map = build_costs_and_ids_map(costs)

    for cost, ids in costs_and_ids_map.items():
        money_left = money - cost
        if money_left in costs_and_ids_map:
            if money_left != cost or (
                money_left == cost
                and has_more_than_one_id(costs_and_ids_map[money_left])
            ):
                smaller_id = ids[0]
                larger_id_idx = 0 if money_left != cost else 1
                larger_id = costs_and_ids_map[money_left][larger_id_idx]
                print(f"{smaller_id} {larger_id}")
                return Solution(smaller_id, larger_id)

    raise Exception("No Solution could be found!")


def build_costs_and_ids_map(costs: Sequence[int]) -> Dict[int, List[int]]:
    costs_and_ids_map = defaultdict(lambda: [])
    for id, cost in enumerate(costs, start=1):
        costs_and_ids_map[cost].append(id)
    return costs_and_ids_map


def has_more_than_one_id(ids: Sequence[int]) -> bool:
    return len(ids) > 1
