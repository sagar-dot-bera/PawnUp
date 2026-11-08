from dataclasses import dataclass


@dataclass(frozen=True)
class TimeControl:
    """Canonical text form is `minutes+seconds`, e.g. `5+3` (UL: Time Control)."""

    base_seconds: int
    increment_seconds: int

    @classmethod
    def parse(cls, text: str) -> "TimeControl":
        minutes, plus, increment = text.partition("+")
        if not plus or not minutes.isdigit() or not increment.isdigit():
            raise ValueError(f"time control must look like '5+3', got {text!r}")
        return cls(int(minutes) * 60, int(increment))

    def __str__(self) -> str:
        return f"{self.base_seconds // 60}+{self.increment_seconds}"
