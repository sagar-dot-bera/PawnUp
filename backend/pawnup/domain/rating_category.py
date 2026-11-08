from enum import Enum

from pawnup.domain.time_control import TimeControl

# Lichess-style: estimated game length = base + 40 * increment (seconds).
_MOVES_PER_GAME = 40
_BULLET_BELOW = 180
_BLITZ_BELOW = 480
_RAPID_BELOW = 1500


class RatingCategory(str, Enum):
    BULLET = "bullet"
    BLITZ = "blitz"
    RAPID = "rapid"
    CLASSICAL = "classical"


def rating_category(time_control: TimeControl) -> RatingCategory:
    estimated = time_control.base_seconds + _MOVES_PER_GAME * time_control.increment_seconds
    if estimated < _BULLET_BELOW:
        return RatingCategory.BULLET
    if estimated < _BLITZ_BELOW:
        return RatingCategory.BLITZ
    if estimated < _RAPID_BELOW:
        return RatingCategory.RAPID
    return RatingCategory.CLASSICAL
