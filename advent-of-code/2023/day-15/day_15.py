from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Lens:
    label: str
    focal_length: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.label == other.label

def run_hash_algorithm(step: str) -> int:
    hash_value = 0
    for c in step:
        hash_value += ord(c)
        hash_value *= 17
        hash_value %= 256
    return hash_value

def sum_all_hash_values(steps: list[str]) -> int:
    return sum(run_hash_algorithm(step) for step in steps)

def read_input(input_path: str) -> list[str]:
    with open(input_path) as f:
        return f.readline().strip().split(",")
    
def sum_focusing_power(boxes: dict[int, list[Lens]]) -> int:
    total_sum = 0
    for box_number, lenses in boxes.items():
        for slot, lens in enumerate(lenses, start=1):
            total_sum += ((box_number+1) * slot * lens.focal_length)
    return total_sum


def run_hashmap_algorithm(steps: list[str]) -> dict[int, list[Lens]]:
    boxes: dict[int, list[Lens]] = defaultdict(list)
    for step in steps:
        if "=" in step:
            label, focal_length = step.split("=")
            box_number = run_hash_algorithm(label)
            lens = Lens(label, int(focal_length))
            if lens in boxes[box_number]:
                i = boxes[box_number].index(lens)
                boxes[box_number][i] = lens
            else:
                boxes[box_number].append(lens)
        else:
            label = step.split("-")[0]
            box_number = run_hash_algorithm(label)
            lens = Lens(label, 0)
            if lens in boxes[box_number]:
                boxes[box_number].remove(lens)
    return boxes
    
steps = read_input("./example")
print(sum_all_hash_values(steps))
boxes = run_hashmap_algorithm(steps)
print(sum_focusing_power(boxes))

steps = read_input("./input")
print(sum_all_hash_values(steps))
boxes = run_hashmap_algorithm(steps)
print(sum_focusing_power(boxes))