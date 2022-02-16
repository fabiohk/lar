from itertools import permutations
from typing import Iterator, Sequence


def solution(words: Sequence[str]) -> int:
    return sum(
        count_crosswords_possibilities(words_permutation)
        for words_permutation in permutations(words)
    )


def count_crosswords_possibilities(words: Sequence[str]) -> int:
    possibilities_count = 0
    for i, char_from_word0 in enumerate(words[0]):
        if char_from_word0 in words[1]:
            for word0_word1_intersection_idx in all_char_indexes(
                char_from_word0, words[1]
            ):
                word1_start_idx = word0_word1_intersection_idx + 2
                sub_word1 = words[1][word1_start_idx::]
                for j, char_from_word1 in enumerate(sub_word1, start=word1_start_idx):
                    if char_from_word1 in words[2]:
                        for word1_word2_intersection_idx in all_char_indexes(
                            char_from_word1, words[2]
                        ):
                            word2_start_idx = word1_word2_intersection_idx + 2
                            sub_word2 = words[2][word2_start_idx::]
                            for k, char_from_word2 in enumerate(
                                sub_word2, start=word2_start_idx
                            ):
                                if char_from_word2 in words[3]:
                                    for (
                                        word2_word3_intersection_idx
                                    ) in all_char_indexes(char_from_word2, words[3]):
                                        word0_idx = k + (
                                            i - word1_word2_intersection_idx
                                        )
                                        word3_idx = word2_word3_intersection_idx + (
                                            word0_word1_intersection_idx - j
                                        )
                                        if not is_inside_word(
                                            word0_idx, words[0]
                                        ) or not is_inside_word(word3_idx, words[3]):
                                            continue

                                        if words[0][word0_idx] == words[3][word3_idx]:
                                            possibilities_count += 1

    return possibilities_count


def all_char_indexes(char: str, word: str) -> Iterator[int]:
    for i, char_from_word in enumerate(word):
        if char == char_from_word:
            yield i


def is_inside_word(idx: int, word: str) -> bool:
    return 0 <= idx < len(word)
