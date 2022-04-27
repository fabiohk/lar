import pytest

from enclose_in_brackets import solution


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("abacaba", "(abacaba)"),
        ("abcdef", "(abcdef)"),
        ("aaad", "(aaad)"),
        ("if", "(if)"),
        ("it", "(it)"),
        ("doesnt", "(doesnt)"),
        ("challenge", "(challenge)"),
        ("you", "(you)"),
        ("itt", "(itt)"),
        ("wont", "(wont)"),
    ],
)
def test_should_gives_expected_output(input_string: str, expected_output: str):
    assert solution(input_string) == expected_output
