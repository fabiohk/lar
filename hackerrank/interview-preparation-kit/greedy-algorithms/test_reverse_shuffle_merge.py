import pytest

import reverse_shuffle_merge


@pytest.mark.parametrize(
    "s, expected_A",
    [
        ("eggegg", "egg"),
        ("abcdefgabcdefg", "agfedcb"),
        ("aeiouuoiea", "aeiou"),
        (
            "djjcddjggbiigjhfghehhbgdigjicafgjcehhfgifadihiajgciagicdahcbajjbhifjiaajigdgdfhdiijjgaiejgegbbiigida",
            "aaaaabccigicgjihidfiejfijgidgbhhehgfhjgiibggjddjjd",
        ),
    ],
)
def test_should_gives_expected_output(s, expected_A):
    assert reverse_shuffle_merge.reverseShuffleMerge(s) == expected_A
