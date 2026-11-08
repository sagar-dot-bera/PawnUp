import pytest

from pawnup.domain.matchmaking import FixedRatingWindow, Seek, pair
from pawnup.domain.time_control import TimeControl

BLITZ = TimeControl.parse("5+3")
BULLET = TimeControl.parse("1+0")


def seek(user, rating, time_control=BLITZ, rated=True, created=0):
    return Seek(user, time_control, rated, rating, created)


def test_same_time_control_and_close_ratings_are_paired():
    pairings = pair([seek("a", 1500), seek("b", 1600)])
    assert [(p.first.user_id, p.second.user_id) for p in pairings] == [("a", "b")]


def test_different_time_control_is_never_paired():
    assert pair([seek("a", 1500), seek("b", 1500, BULLET)]) == []


def test_ratings_outside_the_window_are_not_paired():
    assert pair([seek("a", 1500), seek("b", 1701)]) == []
    assert len(pair([seek("a", 1500), seek("b", 1700)])) == 1  # boundary is inclusive


def test_window_is_replaceable():
    assert len(pair([seek("a", 1000), seek("b", 1900)], FixedRatingWindow(1000))) == 1


def test_rated_and_casual_seeks_do_not_mix():
    assert pair([seek("a", 1500, rated=True), seek("b", 1500, rated=False)]) == []


def test_guest_cannot_seek_rated():
    with pytest.raises(ValueError):
        seek("guest", None, rated=True)


def test_guest_pairs_in_casual_only():
    guest = seek("g", None, rated=False)
    assert len(pair([guest, seek("u", 1800, rated=False)])) == 1
    assert pair([guest, seek("u", 1800, rated=True)]) == []


def test_same_user_is_not_paired_with_themselves():
    assert pair([seek("a", 1500), seek("a", 1500)]) == []


def test_longest_waiting_is_served_first_with_closest_rating():
    seeks = [seek("a", 1500, created=0), seek("b", 1650, created=1), seek("c", 1520, created=2)]
    pairings = pair(seeks)
    assert [(p.first.user_id, p.second.user_id) for p in pairings] == [("a", "c")]
