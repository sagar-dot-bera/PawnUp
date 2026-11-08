import pytest

from pawnup.domain.rating_category import RatingCategory, rating_category
from pawnup.domain.time_control import TimeControl


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1+0", RatingCategory.BULLET),
        ("2+1", RatingCategory.BULLET),  # 120 + 40 = 160 s
        ("3+0", RatingCategory.BLITZ),  # 180 s is the first blitz value
        ("5+3", RatingCategory.BLITZ),  # 420 s
        ("10+0", RatingCategory.RAPID),  # 600 s
        ("15+10", RatingCategory.RAPID),  # 1300 s
        ("25+0", RatingCategory.CLASSICAL),  # 1500 s is the first classical value
        ("90+30", RatingCategory.CLASSICAL),
    ],
)
def test_categories(text, expected):
    assert rating_category(TimeControl.parse(text)) is expected


def test_parse_round_trips_and_rejects_junk():
    assert str(TimeControl.parse("5+3")) == "5+3"
    for bad in ["5", "5m+3", "a+b", "+3", ""]:
        with pytest.raises(ValueError):
            TimeControl.parse(bad)
