from dataclasses import dataclass

from pawnup.domain.termination import Termination


@dataclass(frozen=True)
class Participant:
    is_guest: bool


def can_play_rated(participant: Participant) -> bool:
    return not participant.is_guest


def changes_ratings(
    rated: bool,
    white: Participant,
    black: Participant,
    termination: Termination | None,
) -> bool:
    """Rule R1: only a finished rated game between two registered users changes ratings.

    `termination` is None while the game is in progress. Abandonment counts as finished.
    """
    return rated and termination is not None and can_play_rated(white) and can_play_rated(black)
