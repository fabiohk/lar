#!/bin/python3

import math
import os
import random
import re
import sys
from collections import defaultdict
from typing import Mapping, Dict

#
# Complete the 'reverseShuffleMerge' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#


def reverseShuffleMerge(s: str) -> str:
    chars_frequency_map = count_chars_frequency(s)
    chars_to_found_frequencies = halve_dict_values(chars_frequency_map)

    reversed_s = s[::-1]
    smallest_A = ""

    for i, char in enumerate(reversed_s):
        if not should_skip_char(
            char, reversed_s[i + 1 : :], chars_frequency_map, chars_to_found_frequencies
        ):
            smallest_A += char
            chars_to_found_frequencies[char] -= 1

    return smallest_A


def should_skip_char(
    char: str,
    remaining_string: str,
    chars_frequency_map: Mapping[str, int],
    chars_to_found_frequencies: Mapping[str, int],
) -> bool:
    if chars_to_found_frequencies[char] == 0:
        return True

    if char not in remaining_string:
        return False

    if is_smallest_char(char, chars_to_found_frequencies):
        return False

    if char_frequency(char, remaining_string) * 2 < chars_frequency_map[char]:
        return False

    return True


def count_chars_frequency(string: str) -> Dict[str, int]:
    chars_frequency_map = defaultdict(lambda: 0)

    for char in string:
        chars_frequency_map[char] += 1

    return chars_frequency_map


def halve_dict_values(dictionary: Mapping[str, int]) -> Dict[str, int]:
    return {k: v // 2 for k, v in dictionary.items()}


def is_smallest_char(char: str, chars_frequency: Mapping[str, int]) -> bool:
    chars_with_frequency_not_zero = sorted(
        [c for c in chars_frequency if chars_frequency[c] > 0]
    )
    smallest_char = chars_with_frequency_not_zero[0]

    return smallest_char == char


def char_frequency(char: str, string: str) -> int:
    return sum(1 for c in string if c == char)


if __name__ == "__main__":
    fptr = open(os.environ["OUTPUT_PATH"], "w")

    s = input()

    result = reverseShuffleMerge(s)

    fptr.write(result + "\n")

    fptr.close()
