from typing import Sequence

import pytest

from ice_cream_parlor import Solution, solver


@pytest.mark.parametrize(
    "cost, money, expected_smaller_id, expected_larger_id",
    (([1, 4, 5, 3, 2], 4, 1, 4), ([2, 2, 4, 3], 4, 1, 2)),
)
def test_should_gives_expected_output(
    cost: Sequence[int], money: int, expected_smaller_id: int, expected_larger_id: int
):
    solution: Solution = solver(cost, money)
    assert solution.smaller_id == expected_smaller_id
    assert solution.larger_id == expected_larger_id
