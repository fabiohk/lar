import pytest

import comfortable_numbers


@pytest.mark.parametrize(
    "l, r, expected_output",
    [
        (10, 12, 2),
        (1, 9, 20),
        (13, 13, 0),
        (12, 108, 707),
        (239, 777, 6166),
        (1, 1000, 11435),
    ],
)
def test_should_gives_expected_output(l, r, expected_output):
    assert comfortable_numbers.solution(l, r) == expected_output
