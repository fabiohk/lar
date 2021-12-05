from collections import defaultdict
from typing import List, Mapping


def solution(n: int) -> List[int]:
    divisors_map = {}
    weakness_map = defaultdict(lambda: 0)

    for i in inclusive_range(1, n):
        divisors_map[i] = count_divisors(i)
        weakness = calculate_weakness(i, divisors_map)
        weakness_map[weakness] += 1

    weakest = calculate_weakest(weakness_map)
    weakness_of_weakest = weakness_map[weakest]

    return [weakest, weakness_map[weakest]]


def inclusive_range(start: int, stop: int, step: int = 1):
    return range(start, stop + 1, step)


def count_divisors(n: int) -> int:
    divisors_counter = 0

    for i in range(1, n + 1):
        if n % i == 0:
            divisors_counter += 1

    return divisors_counter


def calculate_weakness(n: int, divisors_map: Mapping[int, int]) -> int:
    divisors = divisors_map[n]
    weakness = 0

    for k in divisors_map.keys():
        if k >= n:
            break
        if divisors_map[k] > divisors:
            weakness += 1

    return weakness


def calculate_weakest(weakness_map: Mapping[int, int]) -> int:
    return sorted(weakness_map.keys())[-1]
