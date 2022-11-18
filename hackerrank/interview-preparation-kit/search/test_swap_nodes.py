from typing import List, Sequence

import pytest

import swap_nodes


@pytest.mark.parametrize(
    "indexes, queries, expected_output",
    (
        ([[2, 3], [-1, -1], [-1, -1]], [1, 1], [[3, 1, 2], [2, 1, 3]]),
        ([[2, 3], [-1, 4], [-1, 5], [-1, -1], [-1, -1]], [2], [[4, 2, 1, 5, 3]]),
        (
            [
                [2, 3],
                [4, -1],
                [5, -1],
                [6, -1],
                [7, 8],
                [-1, 9],
                [-1, -1],
                [10, 11],
                [-1, -1],
                [-1, -1],
                [-1, -1],
            ],
            [2, 4],
            [[2, 9, 6, 4, 1, 3, 7, 5, 11, 8, 10], [2, 6, 9, 4, 1, 3, 7, 5, 10, 8, 11]],
        ),
        (
            [
                [2, 3],
                [4, 5],
                [6, -1],
                [-1, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [-1, 14],
                [-1, -1],
                [15, -1],
                [16, 17],
                [-1, -1],
                [-1, -1],
                [-1, -1],
                [-1, -1],
                [-1, -1],
                [-1, -1],
            ],
            [2, 3],
            [
                [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17, 11, 16],
                [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6, 10, 15],
            ],
        ),
    ),
)
def test_should_gives_expected_output(
    indexes: Sequence[Sequence[int]],
    queries: Sequence[int],
    expected_output: Sequence[Sequence[int]],
):
    output = swap_nodes.solution(indexes, queries)

    assert len(output) == len(expected_output)
    for i in range(len(expected_output)):
        assert_lists_are_equal(
            output[i], expected_output[i], f"Lists from index {i} doesn't match"
        )


def assert_lists_are_equal(
    list: List[int], expected_list: List[int], message_error: str
):
    assert len(list) == len(expected_list), message_error
    assert all(n == m for n, m in zip(list, expected_list)), message_error
