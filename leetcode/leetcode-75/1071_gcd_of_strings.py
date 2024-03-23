import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 == str2:
            return str1

        str1_pattern = self.find_pattern(str1)
        str2_pattern = self.find_pattern(str2)

        if str1_pattern == str2_pattern:
            return self.find_gcd(str1, str2, str1_pattern)
        return ""

    def find_gcd(self, str1: str, str2: str, pattern: str) -> str:
        pattern_len = len(pattern)
        str1_len = len(str1)
        str2_len = len(str2)

        return pattern * math.gcd(str1_len // pattern_len, str2_len // pattern_len)

    def find_pattern(self, string: str) -> str:
        i = 0
        possible_pattern = string[0]
        while not self.is_a_pattern(possible_pattern, string):
            i += 1
            possible_pattern += string[i]
        return possible_pattern

    def is_a_pattern(self, possible_pattern: str, string: str) -> bool:
        splits = string.split(possible_pattern)
        return all(splitted_str == "" for splitted_str in splits)