from typing import Protocol


class TimeSource(Protocol):
    """Where 'now' comes from, so domain code never reads the wall clock."""

    def now_ms(self) -> int: ...
