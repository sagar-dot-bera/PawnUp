import pytest

from pawnup.domain.clock import Clock
from pawnup.domain.live_game import Color, LiveGame
from pawnup.domain.termination import Result, Termination
from tests.fakes import FakeTimeSource


def make_clock(base_ms=60_000, increment_ms=2_000):
    time = FakeTimeSource()
    clock = Clock(base_ms, increment_ms, time)
    clock.start(Color.WHITE)
    return clock, time


def test_running_side_loses_time_and_other_side_does_not():
    clock, time = make_clock()
    time.advance(10_000)
    assert clock.remaining_ms(Color.WHITE) == 50_000
    assert clock.remaining_ms(Color.BLACK) == 60_000


def test_press_adds_increment_and_flips_the_clock():
    clock, time = make_clock()
    time.advance(10_000)
    clock.press(Color.WHITE)
    assert clock.remaining_ms(Color.WHITE) == 52_000
    time.advance(5_000)
    assert clock.remaining_ms(Color.BLACK) == 55_000
    assert clock.remaining_ms(Color.WHITE) == 52_000


def test_flagged_when_time_reaches_zero_exactly():
    clock, time = make_clock()
    time.advance(59_999)
    assert clock.flagged() is None
    time.advance(1)
    assert clock.flagged() is Color.WHITE


def test_no_increment_for_a_move_made_after_flagging():
    clock, time = make_clock()
    time.advance(61_000)
    clock.press(Color.WHITE)
    assert clock.remaining_ms(Color.WHITE) <= 0


def test_pressing_for_the_wrong_color_is_an_error():
    clock, _ = make_clock()
    with pytest.raises(ValueError):
        clock.press(Color.BLACK)


def test_flag_fall_loses_on_time_when_opponent_can_mate():
    game = LiveGame()
    game.flag(Color.WHITE)
    assert (game.result, game.termination) == (Result.BLACK_WINS, Termination.TIMEOUT)


def test_flag_fall_is_a_draw_when_opponent_has_insufficient_material():
    game = LiveGame("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    game.flag(Color.WHITE)  # black has a bare king and can never mate
    assert (game.result, game.termination) == (Result.DRAW, Termination.INSUFFICIENT_MATERIAL)


def test_a_lone_minor_piece_counts_as_insufficient():
    game = LiveGame("4k3/8/8/8/8/8/8/4KB2 w - - 0 1")
    game.flag(Color.BLACK)  # white has king + bishop only
    assert game.result is Result.DRAW


def test_flag_fall_with_mating_material_loses_for_the_flagged_side():
    game = LiveGame("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    game.flag(Color.BLACK)  # white has a rook
    assert (game.result, game.termination) == (Result.WHITE_WINS, Termination.TIMEOUT)


def test_flag_after_game_finished_changes_nothing():
    game = LiveGame()
    game.resign(Color.WHITE)
    game.flag(Color.BLACK)
    assert game.termination is Termination.RESIGNATION
