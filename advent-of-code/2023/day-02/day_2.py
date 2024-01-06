import re
from typing import TypedDict


cubes_limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}

class Round(TypedDict):
    red: int
    green: int
    blue: int


def is_possible (round: Round) -> bool:
    return round["red"] <= cubes_limits["red"] and round["green"] <= cubes_limits["green"] and round["blue"] <= cubes_limits["blue"]

def is_a_possible_game (game: list[Round]) -> bool:
    return all(is_possible(round) for round in game)

def sum_only_possible_games_ids (games: list[list[Round]]) -> int:
    return sum(idx for idx, game in enumerate(games, 1) if is_a_possible_game(game))

def calculate_game_power (game: list[Round]) -> int:
    min_red, min_green, min_blue = 0, 0, 0

    for round in game:
        min_red = max(min_red, round["red"])
        min_green = max(min_green, round["green"])
        min_blue = max(min_blue, round["blue"])

    return min_red * min_green * min_blue

def sum_power_of_games (games: list[list[Round]]) -> int:
    return sum(calculate_game_power(game) for game in games)

def parse_sets (sets: list[str]) -> Round:
    set_dict: Round = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for cubes in sets:
        m = re.match(r"([0-9]+)([a-z]+)", cubes.lower())
        number_of_cubes = int(m.group(1))
        cube_color = m.group(2)
        set_dict[cube_color] += number_of_cubes

    return set_dict

def parse_round_str (round_str: str) -> Round:
    sets = round_str.split(",")
    return parse_sets(sets)

def parse_line (line: str) -> list[Round]:
    _, rounds_only = line.split(":")
    rounds_only = rounds_only.replace(" ", "")
    rounds = rounds_only.split(";")
    return [parse_round_str(round_str) for round_str in rounds]


def read_input () -> list[list[Round]]:
    with open("./input") as f:
        return [parse_line(line) for line in f.readlines()]
    

games = read_input()
print(sum_only_possible_games_ids(games))
print(sum_power_of_games(games))