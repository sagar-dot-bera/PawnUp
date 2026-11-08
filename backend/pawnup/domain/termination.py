from enum import Enum


class Result(str, Enum):
    WHITE_WINS = "1-0"
    BLACK_WINS = "0-1"
    DRAW = "1/2-1/2"


class Termination(str, Enum):
    CHECKMATE = "checkmate"
    RESIGNATION = "resignation"
    TIMEOUT = "timeout"
    STALEMATE = "stalemate"
    INSUFFICIENT_MATERIAL = "insufficient_material"
    FIFTY_MOVE_RULE = "fifty_move_rule"
    THREEFOLD_REPETITION = "threefold_repetition"
    AGREEMENT = "agreement"
    ABANDONMENT = "abandonment"
