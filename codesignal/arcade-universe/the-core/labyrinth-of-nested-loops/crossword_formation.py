from itertools import permutations
from typing import Iterator, Sequence


def solution(words: Sequence[str]) -> int:
    return sum(count_crosswords_possibilities(words_permutation) for words_permutation in permutations(words))


def all_char_indexes(char: str, word: str) -> Iterator[int]:
    yield from (i for i, char_from_word in enumerate(word) if char == char_from_word)


def count_crosswords_possibilities(words: Sequence[str]) -> int:
    possibilities_count = 0
    for i in range(len(words[0]) - 2):
        for j in range(i + 2, len(words[0])):
            for word0_word1_intersection in all_char_indexes(words[0][i], words[1]):
                for word0_word2_intersection in all_char_indexes(words[0][j], words[2]):
                    for word1_char, word2_char in zip(
                        words[1][word0_word1_intersection + 2 :], words[2][word0_word2_intersection + 2 :]
                    ):
                        for word3_char, another_word3_char in zip(words[3], words[3][j - i :]):
                            possibilities_count += word1_char == word3_char and word2_char == another_word3_char
    return possibilities_count
