from dataclasses import dataclass
from enum import Enum

import chess

from pawnup.domain.termination import Result, Termination


class Color(str, Enum):
    WHITE = "w"
    BLACK = "b"

    @property
    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class RejectReason(str, Enum):
    MALFORMED = "malformed"
    ILLEGAL = "illegal"
    NOT_YOUR_TURN = "not_your_turn"
    GAME_FINISHED = "game_finished"


@dataclass(frozen=True)
class MoveAccepted:
    uci: str
    san: str
    fen: str


@dataclass(frozen=True)
class MoveRejected:
    reason: RejectReason


MoveOutcome = MoveAccepted | MoveRejected


def _board_color(color: Color) -> chess.Color:
    return chess.WHITE if color is Color.WHITE else chess.BLACK


class LiveGame:
    """A game in progress. The only place that touches the python-chess Board."""

    def __init__(self, fen: str | None = None) -> None:
        self._board = chess.Board(fen) if fen else chess.Board()
        self.result: Result | None = None
        self.termination: Termination | None = None

    @property
    def fen(self) -> str:
        return self._board.fen()

    @property
    def turn(self) -> Color:
        return Color.WHITE if self._board.turn == chess.WHITE else Color.BLACK

    @property
    def is_finished(self) -> bool:
        return self.result is not None

    def apply_move(self, player: Color, uci: str) -> MoveOutcome:
        """Rule R2: accept a move only if it is legal and it is `player`'s turn."""
        if self.is_finished:
            return MoveRejected(RejectReason.GAME_FINISHED)
        if player is not self.turn:
            return MoveRejected(RejectReason.NOT_YOUR_TURN)
        try:
            move = chess.Move.from_uci(uci)
        except ValueError:
            return MoveRejected(RejectReason.MALFORMED)
        if not self._board.is_legal(move):
            return MoveRejected(RejectReason.ILLEGAL)

        san = self._board.san(move)
        self._board.push(move)
        self._finish_if_over()
        return MoveAccepted(uci=uci, san=san, fen=self.fen)

    def resign(self, player: Color) -> None:
        self._finish(_win_for(player.opponent), Termination.RESIGNATION)

    def flag(self, loser: Color) -> None:
        """Rule R5: a player whose clock reached zero loses, unless the opponent
        cannot possibly checkmate, in which case the game is drawn."""
        if self.is_finished:
            return
        if self._board.has_insufficient_material(_board_color(loser.opponent)):
            self._finish(Result.DRAW, Termination.INSUFFICIENT_MATERIAL)
        else:
            self._finish(_win_for(loser.opponent), Termination.TIMEOUT)

    def abandon(self, leaver: Color) -> None:
        self._finish(_win_for(leaver.opponent), Termination.ABANDONMENT)

    def _finish_if_over(self) -> None:
        board = self._board
        if board.is_checkmate():
            self._finish(_win_for(self.turn.opponent), Termination.CHECKMATE)
        elif board.is_stalemate():
            self._finish(Result.DRAW, Termination.STALEMATE)
        elif board.is_insufficient_material():
            self._finish(Result.DRAW, Termination.INSUFFICIENT_MATERIAL)
        elif board.can_claim_threefold_repetition():
            self._finish(Result.DRAW, Termination.THREEFOLD_REPETITION)
        elif board.can_claim_fifty_moves():
            self._finish(Result.DRAW, Termination.FIFTY_MOVE_RULE)

    def _finish(self, result: Result, termination: Termination) -> None:
        if self.is_finished:
            return
        self.result = result
        self.termination = termination


def _win_for(color: Color) -> Result:
    return Result.WHITE_WINS if color is Color.WHITE else Result.BLACK_WINS
