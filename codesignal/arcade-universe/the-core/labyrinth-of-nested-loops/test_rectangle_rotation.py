import pytest
import rectangle_rotation


@pytest.mark.parametrize(
    "a, b, expected_output",
    [
        (6, 4, 23),
        (30, 2, 65),
        (8, 6, 49),
        (16, 20, 333),
        (20, 32, 653),
        (30, 26, 795),
        (50, 4, 177),
        (2, 2, 5),
        (50, 50, 2521),
        (38, 42, 1563),
    ],
)
def test_should_gives_expected_output(a, b, expected_output):
    assert rectangle_rotation.solution(a, b) == expected_output
