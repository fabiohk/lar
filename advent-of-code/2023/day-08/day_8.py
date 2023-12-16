from dataclasses import dataclass
import re
import math


@dataclass
class Instruction:
    left: str
    right: str

type Map = dict[str, Instruction]

def calculate_steps_to_reach_end(map: Map, instructions: str, start_node: str, possible_end_nodes: list[str]) -> list[str]:
    reached_end = False
    next_instruction_index = 0
    instructions_length = len(instructions)
    current_node = start_node
    steps = []

    while not reached_end:
        instruction = instructions[next_instruction_index]
        next_instruction_index = (next_instruction_index + 1) % instructions_length

        if instruction == "L":
            current_node = map[current_node].left
        else:
            current_node = map[current_node].right

        steps.append(current_node)
        if current_node in possible_end_nodes:
            reached_end = True

    return steps


def read_input() -> tuple[Map, str]:
    map = {}

    with open("./input") as f:
        instructions = f.readline().strip()

        for line in f.readlines():
            m = re.match(r"([0-9|A-Z]{3}).*([0-9|A-Z]{3}).*([0-9|A-Z]{3})", line)
            if m:
                node, left, right = m.group(1), m.group(2), m.group(3)
                map[node] = Instruction(left, right)

        return map, instructions

def calculate_steps_to_reach_end_for_part_two(map: Map, instructions: str) -> int:
    starting_nodes = [node for node in map.keys() if node[-1] == "A"]
    possible_end_nodes = [node for node in map.keys() if node[-1] == "Z"]
    steps = [0 for _ in range(len(starting_nodes))]

    for i, node in enumerate(starting_nodes):
        steps_to_reach_end = calculate_steps_to_reach_end(map, instructions, node, possible_end_nodes)
        steps[i] = len(steps_to_reach_end)

    return math.lcm(*steps)

map, instructions = read_input()
steps_to_reach_end = calculate_steps_to_reach_end(map, instructions, "AAA", ["ZZZ"])
print(len(steps_to_reach_end))

steps_to_reach_end = calculate_steps_to_reach_end_for_part_two(map, instructions)
print(steps_to_reach_end)
