from collections import namedtuple
import re


Card = namedtuple('Card', ['winning_numbers', 'card_numbers'])

def sum_points(points: list[int]) -> int:
    return sum(points)

def calculate_card_points(card: Card) -> int:
    quantity_of_winning_numbers = len(winning_numbers_from_card(card))

    if quantity_of_winning_numbers < 1:
        return 0

    return 2 ** (quantity_of_winning_numbers - 1)

def winning_numbers_from_card(card: Card) -> list[int]:
    return [winning_number for winning_number in card.winning_numbers if winning_number in card.card_numbers]

def read_input() -> list[Card]:
    with open("./input") as f:
        return [parse_line(line) for line in f.readlines()]
    
def parse_line(line: str) -> Card:
    numbers = line.split(":")[1]
    winning_numbers_str, card_numbers_str = numbers.split("|")
    winning_numbers = parse_numbers_string(winning_numbers_str)
    card_numbers = parse_numbers_string(card_numbers_str)
    return Card(winning_numbers, card_numbers)

def parse_numbers_string(numbers_str: str) -> list[int]:
    match_iterator = re.finditer(r"([0-9]+)", numbers_str)
    return [int(match.group()) for match in match_iterator]


cards = read_input()
card_points = [calculate_card_points(card) for card in cards]
print(sum_points(card_points))

def calculate_quantity_of_card_copies(cards: list[Card]) -> int:
    card_copies = [1 for _ in cards]

    for i, card in enumerate(cards):
        quantity_of_winning_numbers = winning_numbers_from_card(card)
        for j in range(len(quantity_of_winning_numbers)):
            card_copies[i+j+1] += card_copies[i]
        print(card_copies)

    
    return sum(value for value in card_copies)

quantity_of_card_copies = calculate_quantity_of_card_copies(cards)
print(quantity_of_card_copies)