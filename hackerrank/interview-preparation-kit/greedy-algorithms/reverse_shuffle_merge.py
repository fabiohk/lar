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
    smallest_A = ""
    smallest_char, smallest_char_index = "", -1

    for i, char in enumerate(reversed_s):
        if is_smallest_char(char, chars_to_found_frequencies):
            smallest_A += char
            chars_to_found_frequencies[char] -= 1
            smallest_char = char
            smallest_char_index = i
        elif is_critical_char(char, reversed_s[i::], chars_to_found_frequencies):
            to_append_chars = ""
            smallest_candidate_char = char
            j = i - 1
            while j > smallest_char_index:
                candidate_char = reversed_s[j]
                if (
                    candidate_char <= smallest_candidate_char
                    and chars_to_found_frequencies[candidate_char] > 0
                ):
                    to_append_chars += candidate_char
                    chars_to_found_frequencies[candidate_char] -= 1
                    smallest_candidate_char = candidate_char
                j -= 1
            smallest_A += to_append_chars[::-1] + char
            chars_to_found_frequencies[char] -= 1
            smallest_char = char
            smallest_char_index = i

    return smallest_A


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
    if not chars_with_frequency_not_zero:
        return False

    smallest_char = chars_with_frequency_not_zero[0]

    return smallest_char == char


def is_critical_char(
    char: str, string, chars_to_found_frequencies: Mapping[str, int]
) -> bool:
    return char_frequency(char, string) == chars_to_found_frequencies[char]


def char_frequency(char: str, string: str) -> int:
    return sum(1 for c in string if c == char)


if __name__ == "__main__":
    fptr = open(os.environ["OUTPUT_PATH"], "w")

    s = input()

    result = reverseShuffleMerge(s)

    fptr.write(result + "\n")

    fptr.close()
