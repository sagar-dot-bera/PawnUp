from dataclasses import dataclass
from typing import Protocol

from pawnup.domain.time_control import TimeControl


@dataclass(frozen=True)
class Seek:
    """One user's entry in the matchmaking queue (UL: Seek)."""

    user_id: str
    time_control: TimeControl
    rated: bool
    rating: int | None  # None for a guest, who has no rating
    created_ms: int

    def __post_init__(self) -> None:
        if self.rated and self.rating is None:
            raise ValueError("a guest cannot seek a rated game")


@dataclass(frozen=True)
class Pairing:
    first: Seek
    second: Seek


class RatingWindow(Protocol):
    def allows(self, first: int, second: int) -> bool: ...


@dataclass(frozen=True)
class FixedRatingWindow:
    half_width: int = 200

    def allows(self, first: int, second: int) -> bool:
        return abs(first - second) <= self.half_width


def _compatible(a: Seek, b: Seek, window: RatingWindow) -> bool:
    """Rule R3: same time control, same rated/casual pool, and ratings inside the window."""
    if a.user_id == b.user_id or a.time_control != b.time_control or a.rated != b.rated:
        return False
    if a.rating is None or b.rating is None:  # guests: casual only, no window to apply
        return True
    return window.allows(a.rating, b.rating)


def _rating_gap(a: Seek, b: Seek) -> int:
    return 0 if a.rating is None or b.rating is None else abs(a.rating - b.rating)


def pair(seeks: list[Seek], window: RatingWindow | None = None) -> list[Pairing]:
    """Pair seeks greedily, longest-waiting first, each with the closest-rated compatible seek."""
    window = window or FixedRatingWindow()
    waiting = sorted(seeks, key=lambda s: s.created_ms)
    pairings: list[Pairing] = []
    while waiting:
        first = waiting.pop(0)
        candidates = [s for s in waiting if _compatible(first, s, window)]
        if not candidates:
            continue
        best = min(candidates, key=lambda s: _rating_gap(first, s))
        waiting.remove(best)
        pairings.append(Pairing(first, best))
    return pairings
