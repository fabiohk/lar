from dataclasses import dataclass
from enum import IntEnum
from functools import cmp_to_key
from typing import Callable

CardStrengths = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1
}

CardStrengthsForPartTwo = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 0,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1
}

class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

@dataclass
class Hand:
    hand: str
    bid: int
    type: HandType

def calculate_total_winnings(hands: list[Hand], cards_strength: dict[str, int]) -> int:
    sorted_hands = sort_hands_by_strongest(hands, cards_strength)
    return sum(sorted_hands[i-1].bid * i for i in range(1, len(sorted_hands)+1))

def sort_hands_by_strongest(hands: list[Hand], cards_strength: dict[str, int]) -> list[Hand]:
    return sorted(hands, key=cmp_to_key(sort_by_strongest_hand(cards_strength)))

def sort_by_strongest_hand(cards_strength: dict[str, int]) -> Callable[[Hand, Hand], int]:
    def compare_function(hand_a: Hand, hand_b: Hand) -> int:
        if hand_a.type != hand_b.type:
            return hand_a.type - hand_b.type
        for a, b in zip(hand_a.hand, hand_b.hand):
            if a != b:
                return cards_strength[a] - cards_strength[b]
        return 0
    return compare_function


def read_input() -> list[Hand]:
    with open("./input") as f:
        return [parse_line(line) for line in f.readlines()]
    
def parse_line(line: str) -> Hand:
    hand, bid_str = line.strip().split(" ")
    return Hand(hand, int(bid_str), get_hand_type(hand))


def get_cards_in_hand(hand: str) -> dict[str, int]:
    cards_map = {}
    for card in hand:
        if card not in cards_map:
            cards_map[card] = 0
        cards_map[card] += 1
    return cards_map

def get_hand_type(hand: str) -> HandType:
    cards_map = get_cards_in_hand(hand)
    cards_map_length = len(cards_map)

    if cards_map_length == 5:
        return HandType.HIGH_CARD
    elif cards_map_length == 4:
        return HandType.ONE_PAIR
    elif cards_map_length == 3:
        return HandType.THREE_OF_A_KIND if any(card_quantity == 3 for card_quantity in cards_map.values()) else HandType.TWO_PAIR
    elif cards_map_length == 2:
        return HandType.FOUR_OF_A_KIND if any(card_quantity == 4 for card_quantity in cards_map.values()) else HandType.FULL_HOUSE
    return HandType.FIVE_OF_A_KIND

def read_input_for_part_two() -> list[Hand]:
    with open("./input") as f:
        return [parse_line_for_part_two(line) for line in f.readlines()]
    
def parse_line_for_part_two(line: str) -> Hand:
    hand, bid_str = line.strip().split(" ")
    return Hand(hand, int(bid_str), get_hand_type_for_part_two(hand))

def get_hand_type_for_part_two(hand: str) -> HandType:
    cards_map = get_cards_in_hand(hand)

    if "J" in cards_map:
        card_with_max_quantity = get_card_with_max_quantity_besides_joker(cards_map)
        if card_with_max_quantity != "J":
            cards_map[card_with_max_quantity] += cards_map["J"]
            del cards_map["J"]

    cards_map_length = len(cards_map)

    if cards_map_length == 5:
        return HandType.HIGH_CARD
    elif cards_map_length == 4:
        return HandType.ONE_PAIR
    elif cards_map_length == 3:
        return HandType.THREE_OF_A_KIND if any(card_quantity == 3 for card_quantity in cards_map.values()) else HandType.TWO_PAIR
    elif cards_map_length == 2:
        return HandType.FOUR_OF_A_KIND if any(card_quantity == 4 for card_quantity in cards_map.values()) else HandType.FULL_HOUSE
    return HandType.FIVE_OF_A_KIND

def get_card_with_max_quantity_besides_joker(cards_map: dict[str, int]) -> str:
    current_max_quantity = 0
    card_with_max_quantity = "J"

    for card, card_quantity in cards_map.items():
        if card != "J" and card_quantity >= current_max_quantity:
            current_max_quantity = card_quantity
            card_with_max_quantity = card

    return card_with_max_quantity

hands = read_input()
print(calculate_total_winnings(hands, CardStrengths))

hands = read_input_for_part_two()
print(calculate_total_winnings(hands, CardStrengthsForPartTwo))