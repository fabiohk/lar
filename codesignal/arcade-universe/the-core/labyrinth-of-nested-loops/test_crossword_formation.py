from typing import Sequence

import pytest

import crossword_formation


@pytest.mark.parametrize(
    "words, expected_output",
    [
        (["crossword", "square", "formation", "something"], 6),
        (["anaesthetist", "thatch", "ethnics", "sabulous"], 0),
        (["eternal", "texas", "chainsaw", "massacre"], 4),
        (["africa", "america", "australia", "antarctica"], 62),
        (["phenomenon", "remuneration", "particularly", "pronunciation"], 62),
        (["onomatopoeia", "philosophical", "provocatively", "thesaurus"], 20),
    ],
)
def test_should_gives_expected_output(words: Sequence[str], expected_output: int):
    crossword_formation.solution(words) == expected_output
