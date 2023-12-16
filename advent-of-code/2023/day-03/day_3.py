from dataclasses import dataclass
from typing import TypedDict
import re


class Number(TypedDict):
    value: int
    is_part_number: bool

@dataclass
class Node:
    i: int
    j: int
    value: str

def sum_all_part_numbers(schematic: list[Number]) -> int:
    return sum(number["value"] for number in schematic if number["is_part_number"])

def is_symbol (c: str) -> bool:
    return ((c < '0') or (c > '9')) and c != '.'

def pick_neighbors(i: int, j: int, lines: list[str]) -> list[Node]:
    neighbors = []

    if i - 1 >= 0:
        if j - 1 >= 0:
            neighbors.append(Node(i-1, j-1, lines[i-1][j-1]))
        neighbors.append(Node(i-1, j, lines[i-1][j]))
        if j + 1 < len(lines[i].strip("\n")):
            neighbors.append(Node(i-1, j+1, lines[i-1][j+1]))

    if j - 1 >= 0:
        neighbors.append(Node(i, j-1, lines[i][j-1]))

    if j + 1 < len(lines[i].strip("\n")):
        neighbors.append(Node(i, j+1, lines[i][j+1]))

    if i + 1 < len(lines):
        if j - 1 >= 0:
            neighbors.append(Node(i+1, j-1, lines[i+1][j-1]))
        neighbors.append(Node(i+1, j, lines[i+1][j]))
        if j + 1 < len(lines[i].strip("\n")):
            neighbors.append(Node(i+1, j+1, lines[i+1][j+1]))

    return neighbors

def is_near_a_symbol(i: int, j: int, lines: list[str]) -> bool:
    neighbors = pick_neighbors(i, j, lines)
    return any(is_symbol(c.value) for c in neighbors)

def parse_lines_first_part(lines: list[str]) -> list[Number]:
    possible_number_value = ''
    is_a_part_number = False
    numbers = []

    for i, line in enumerate(lines):
        possible_number_value = ''
        is_a_part_number = False
        for j, c in enumerate(line.strip("\n")):
            if c.isdigit():
                possible_number_value += c
                is_a_part_number |= is_near_a_symbol(i, j, lines)
            else:
                if possible_number_value:
                    number = {
                        "value": int(possible_number_value),
                        "is_part_number": is_a_part_number
                    }
                    numbers.append(number)
                possible_number_value = ''
                is_a_part_number = False
        if possible_number_value:
            number = {
                "value": int(possible_number_value),
                "is_part_number": is_a_part_number
            }
            numbers.append(number)
    return numbers

def sum_all_gear_ratios (gear_ratios: list[int]) -> int:
    return sum(gear_ratios)

def is_a_possible_gear(c: str) -> bool:
    return c == '*'

def find_number(line: str, including_node: Node) -> int:
    for match_group in re.finditer(r"([0-9]+)", line):
        if match_group.start() <= including_node.j <= match_group.end():
            return int(match_group.group())


def is_same_line(node_1: Node, node_2: Node) -> bool:
    return node_1.i == node_2.i

def pick_near_part_numbers(i: int, j: int, lines: list[str]) -> list[int]:
    neighbors = pick_neighbors(i, j, lines)
    last_neighbor = None
    part_numbers = []

    for neighbor in neighbors:
        if last_neighbor != None and neighbor.i != i and is_same_line(last_neighbor, neighbor) and last_neighbor.value.isdigit() and neighbor.value.isdigit():
            last_neighbor = neighbor
            continue

        if neighbor.value.isdigit():
            number = find_number(lines[neighbor.i], neighbor)
            part_numbers.append(number)

        last_neighbor = neighbor

    return part_numbers


def parse_lines_second_part(lines: list[str]) -> list[int]:
    gear_ratios = []

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if is_a_possible_gear(c):
                part_numbers = pick_near_part_numbers(i, j, lines)
                print(part_numbers)
                if len(part_numbers) == 2:
                    gear_ratio = part_numbers[0] * part_numbers[1]
                    gear_ratios.append(gear_ratio)
    
    return gear_ratios

def read_input_second_part() -> list[int]:
    with open("./input") as f:
        lines = [line.strip() for line in f.readlines()]
        return parse_lines_second_part(lines)

def read_input_first_part() -> list[Number]:
    with open("./input") as f:
        lines = f.readlines()
        return parse_lines_first_part(lines)
    
schematic = read_input_first_part()
print(sum_all_part_numbers(schematic))

gear_ratios = read_input_second_part()
print(sum_all_gear_ratios(gear_ratios))