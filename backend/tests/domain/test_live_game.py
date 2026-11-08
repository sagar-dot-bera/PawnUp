from pawnup.domain.live_game import Color, LiveGame, MoveAccepted, MoveRejected, RejectReason
from pawnup.domain.termination import Result, Termination


def test_legal_move_on_turn_is_accepted():
    game = LiveGame()
    outcome = game.apply_move(Color.WHITE, "e2e4")
    assert isinstance(outcome, MoveAccepted)
    assert outcome.san == "e4"
    assert game.turn is Color.BLACK


def test_illegal_move_is_rejected_and_board_unchanged():
    game = LiveGame()
    before = game.fen
    assert game.apply_move(Color.WHITE, "e2e5") == MoveRejected(RejectReason.ILLEGAL)
    assert game.fen == before


def test_move_out_of_turn_is_rejected_even_if_legal_for_that_color():
    game = LiveGame()
    assert game.apply_move(Color.BLACK, "e7e5") == MoveRejected(RejectReason.NOT_YOUR_TURN)
    assert game.turn is Color.WHITE


def test_garbage_move_text_is_rejected():
    assert LiveGame().apply_move(Color.WHITE, "hello") == MoveRejected(RejectReason.MALFORMED)


def test_no_moves_after_the_game_finished():
    game = LiveGame()
    fools_mate = [(Color.WHITE, "f2f3"), (Color.BLACK, "e7e5"), (Color.WHITE, "g2g4"),
                  (Color.BLACK, "d8h4")]  # fmt: skip
    for color, uci in fools_mate:
        game.apply_move(color, uci)
    assert (game.result, game.termination) == (Result.BLACK_WINS, Termination.CHECKMATE)
    assert game.apply_move(Color.WHITE, "a2a3") == MoveRejected(RejectReason.GAME_FINISHED)


def test_resignation_gives_the_win_to_the_opponent():
    game = LiveGame()
    game.resign(Color.WHITE)
    assert (game.result, game.termination) == (Result.BLACK_WINS, Termination.RESIGNATION)


def test_stalemate_is_a_draw():
    game = LiveGame("7k/8/6K1/8/8/8/8/5Q2 w - - 0 1")
    game.apply_move(Color.WHITE, "f1f7")
    assert (game.result, game.termination) == (Result.DRAW, Termination.STALEMATE)


def test_fifty_move_rule_is_a_draw():
    game = LiveGame("4k3/8/8/8/8/8/R7/4K3 w - - 99 80")
    game.apply_move(Color.WHITE, "a2a3")
    assert (game.result, game.termination) == (Result.DRAW, Termination.FIFTY_MOVE_RULE)
