import { Color } from "@/types/enums";
import { Chess } from "chess.js";

export enum Result {
  WhiteWins = "1-0",
  BlackWins = "0-1",
  Draw = "1/2-1/2",
}

export enum Termination {
  Checkmate = "checkmate",
  Resignation = "resignation",
  Timeout = "timeout",
  Stalemate = "stalemate",
  InsufficientMaterial = "insufficient_material",
  FiftyMoveRule = "fifty_move_rule",
  ThreefoldRepetition = "threefold_repetition",
  Agreement = "agreement",
  Abandonment = "abandonment",
}

export interface GameEnd {
  result: Result;
  termination: Termination;
}

const winFor = (color: Color): Result =>
  color === Color.White ? Result.WhiteWins : Result.BlackWins;

const opponentOf = (color: Color): Color =>
  color === Color.White ? Color.Black : Color.White;

// Same simplification as python-chess's has_insufficient_material for the common
// cases: a bare king, or a king with a single minor piece, cannot mate.
const hasMatingMaterial = (game: Chess, color: Color): boolean => {
  const pieces = game
    .board()
    .flat()
    .filter((square) => square?.color === color && square.type !== "k");
  if (pieces.some((p) => p?.type === "p" || p?.type === "r" || p?.type === "q"))
    return true;
  return pieces.length >= 2;
};

/**
 * Rule R4: a finished game has exactly one Result and one Termination, and they
 * agree. Returns undefined while the game is still in progress.
 */
export const deriveTermination = (
  game: Chess,
  params: { resigned?: Color; timedOut?: Color } = {}
): GameEnd | undefined => {
  if (params.resigned) {
    return {
      result: winFor(opponentOf(params.resigned)),
      termination: Termination.Resignation,
    };
  }

  if (params.timedOut) {
    // FIDE: a flagged player draws if the opponent cannot possibly checkmate
    const opponent = opponentOf(params.timedOut);
    return hasMatingMaterial(game, opponent)
      ? { result: winFor(opponent), termination: Termination.Timeout }
      : { result: Result.Draw, termination: Termination.InsufficientMaterial };
  }

  if (game.isCheckmate()) {
    // the side to move is the one that has been mated
    return {
      result: winFor(opponentOf(game.turn() as Color)),
      termination: Termination.Checkmate,
    };
  }
  if (game.isStalemate()) {
    return { result: Result.Draw, termination: Termination.Stalemate };
  }
  if (game.isInsufficientMaterial()) {
    return {
      result: Result.Draw,
      termination: Termination.InsufficientMaterial,
    };
  }
  if (game.isThreefoldRepetition()) {
    return {
      result: Result.Draw,
      termination: Termination.ThreefoldRepetition,
    };
  }
  if (game.isDrawByFiftyMoves()) {
    return { result: Result.Draw, termination: Termination.FiftyMoveRule };
  }

  return undefined;
};

/** Human wording of a game end, e.g. "Ana won by checkmate" or "Draw by stalemate". */
export const describeTermination = (
  { result, termination }: GameEnd,
  names: { white: string; black: string }
): string => {
  const winner = result === Result.WhiteWins ? names.white : names.black;

  switch (termination) {
    case Termination.Checkmate:
      return `${winner} won by checkmate`;
    case Termination.Resignation:
      return `${winner} won by resignation`;
    case Termination.Timeout:
      return `${winner} won on time`;
    case Termination.Abandonment:
      return `${winner} won by abandonment`;
    case Termination.Stalemate:
      return "Draw by stalemate";
    case Termination.InsufficientMaterial:
      return "Draw by insufficient material";
    case Termination.ThreefoldRepetition:
      return "Draw by threefold repetition";
    case Termination.FiftyMoveRule:
      return "Draw by fifty-move rule";
    case Termination.Agreement:
      return "Draw by agreement";
  }
};
