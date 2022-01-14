#!/bin/python3

import math
import os
import random
import re
import sys
from collections import defaultdict
from typing import Dict, Mapping

#
# Complete the 'reverseShuffleMerge' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#


def reverseShuffleMerge(s: str) -> str:
    original_chars_frequency_map = count_chars_frequency(s)
    chars_to_found_frequencies = halve_dict_values(original_chars_frequency_map)

    reversed_s = s[::-1]
    smallest_A = []

    for i, char in enumerate(reversed_s):
        if can_include(char, chars_to_found_frequencies):
            if smallest_A:
                last_element = smallest_A[-1]
                while last_element > char and can_remove(
                    last_element, reversed_s[i::], chars_to_found_frequencies
                ):
                    smallest_A.pop()
                    chars_to_found_frequencies[last_element] += 1
                    if not smallest_A:
                        break
                    last_element = smallest_A[-1]

            chars_to_found_frequencies[char] -= 1
            smallest_A.append(char)

    return "".join(smallest_A)


def count_chars_frequency(string: str) -> Dict[str, int]:
    chars_frequency_map = defaultdict(lambda: 0)

    for char in string:
        chars_frequency_map[char] += 1

    return chars_frequency_map


def halve_dict_values(dictionary: Mapping[str, int]) -> Dict[str, int]:
    return {k: v // 2 for k, v in dictionary.items()}


def can_include(char: str, chars_to_found_frequencies: Mapping[str, int]) -> bool:
    return chars_to_found_frequencies[char] > 0


def can_remove(
    char: str, remaining_string: str, chars_to_found_frequencies: Mapping[str, int]
) -> bool:
    return (
        char_frequency(char, remaining_string) - 1 >= chars_to_found_frequencies[char]
    )


def char_frequency(char: str, string: str) -> int:
    return sum(1 for c in string if c == char)


if __name__ == "__main__":
    fptr = open(os.environ["OUTPUT_PATH"], "w")

    s = input()

    result = reverseShuffleMerge(s)

    fptr.write(result + "\n")

    fptr.close()
