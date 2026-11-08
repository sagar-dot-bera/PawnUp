from pawnup.domain.live_game import Color
from pawnup.ports import TimeSource


class Clock:
    """Both players' remaining time. Time is read only from the injected TimeSource."""

    def __init__(self, base_ms: int, increment_ms: int, time_source: TimeSource) -> None:
        self._time = time_source
        self._increment_ms = increment_ms
        self._left = {Color.WHITE: base_ms, Color.BLACK: base_ms}
        self._running: Color | None = None
        self._since_ms = 0

    def start(self, color: Color) -> None:
        self._running = color
        self._since_ms = self._time.now_ms()

    def remaining_ms(self, color: Color) -> int:
        if self._running is color:
            return self._left[color] - (self._time.now_ms() - self._since_ms)
        return self._left[color]

    def flagged(self) -> Color | None:
        """The color whose time has run out, if any."""
        for color in Color:
            if self.remaining_ms(color) <= 0:
                return color
        return None

    def press(self, mover: Color) -> None:
        """`mover` has just moved: charge their time, add the increment, flip the clock."""
        if self._running is not mover:
            raise ValueError("clock is not running for this color")
        left = self.remaining_ms(mover)
        self._left[mover] = left if left <= 0 else left + self._increment_ms
        self.start(mover.opponent)
