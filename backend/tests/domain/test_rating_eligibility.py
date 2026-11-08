import pytest

from pawnup.domain.rating_eligibility import Participant, can_play_rated, changes_ratings
from pawnup.domain.termination import Termination

USER = Participant(is_guest=False)
GUEST = Participant(is_guest=True)


def test_finished_rated_game_between_registered_users_changes_ratings():
    assert changes_ratings(True, USER, USER, Termination.CHECKMATE)


def test_game_in_progress_changes_nothing():
    assert not changes_ratings(True, USER, USER, None)


def test_casual_game_changes_nothing():
    assert not changes_ratings(False, USER, USER, Termination.CHECKMATE)


@pytest.mark.parametrize(("white", "black"), [(GUEST, USER), (USER, GUEST), (GUEST, GUEST)])
def test_any_guest_means_no_rating_change(white, black):
    assert not changes_ratings(True, white, black, Termination.CHECKMATE)


@pytest.mark.parametrize("termination", list(Termination))
def test_every_termination_counts_as_finished_including_abandonment(termination):
    assert changes_ratings(True, USER, USER, termination)


def test_guests_can_never_play_rated():
    assert not can_play_rated(GUEST)
    assert can_play_rated(USER)
