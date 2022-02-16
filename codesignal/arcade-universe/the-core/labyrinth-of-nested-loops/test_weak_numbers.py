from typing import Sequence

import pytest

import weak_numbers


@pytest.mark.parametrize(
    "n, expected_output",
    [
        (9, [2, 2]),
        (1, [0, 1]),
        (2, [0, 2]),
        (7, [2, 1]),
        (500, [403, 1]),
        (4, [0, 4]),
    ],
)
def test_should_gives_expected_output(n: int, expected_output: Sequence[int]):
    assert weak_numbers.solution(n) == expected_output
