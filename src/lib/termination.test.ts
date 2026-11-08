import { Color } from "@/types/enums";
import { Chess } from "chess.js";
import { describe, expect, it } from "vitest";
import {
  describeTermination,
  deriveTermination,
  GameEnd,
  Result,
  Termination,
} from "./termination";

const play = (...sans: string[]) => {
  const game = new Chess();
  sans.forEach((san) => game.move(san));
  return game;
};

// Result and Termination must always agree (rule R4).
const agrees = ({ result, termination }: GameEnd): boolean => {
  const drawn = [
    Termination.Stalemate,
    Termination.InsufficientMaterial,
    Termination.ThreefoldRepetition,
    Termination.FiftyMoveRule,
    Termination.Agreement,
  ];
  return drawn.includes(termination)
    ? result === Result.Draw
    : result !== Result.Draw;
};

describe("deriveTermination", () => {
  it("returns nothing while the game is in progress", () => {
    expect(deriveTermination(new Chess())).toBeUndefined();
  });

  it("checkmate: the side that delivered mate wins", () => {
    const foolsMate = play("f3", "e5", "g4", "Qh4#");
    expect(deriveTermination(foolsMate)).toEqual({
      result: Result.BlackWins,
      termination: Termination.Checkmate,
    });
    const scholars = play("e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6", "Qxf7#");
    expect(deriveTermination(scholars)?.result).toBe(Result.WhiteWins);
  });

  it("stalemate is a draw", () => {
    const game = new Chess("7k/8/6K1/8/8/8/8/5Q2 w - - 0 1");
    game.move("Qf7");
    expect(deriveTermination(game)).toEqual({
      result: Result.Draw,
      termination: Termination.Stalemate,
    });
  });

  it("insufficient material is a draw", () => {
    const game = new Chess("4k3/8/8/8/8/8/8/4KB2 w - - 0 1");
    expect(deriveTermination(game)).toEqual({
      result: Result.Draw,
      termination: Termination.InsufficientMaterial,
    });
  });

  it("threefold repetition is a draw", () => {
    const game = play(
      ...["Nf3", "Nf6", "Ng1", "Ng8", "Nf3", "Nf6", "Ng1", "Ng8"]
    );
    expect(deriveTermination(game)).toEqual({
      result: Result.Draw,
      termination: Termination.ThreefoldRepetition,
    });
  });

  // This case used to leave the PGN Result unset (setGameHeaders had no fifty-move branch).
  it("fifty-move rule is a draw", () => {
    const game = new Chess("4k3/8/8/8/8/8/R7/4K3 w - - 99 80");
    expect(deriveTermination(game)).toBeUndefined();
    game.move("Ra3");
    expect(deriveTermination(game)).toEqual({
      result: Result.Draw,
      termination: Termination.FiftyMoveRule,
    });
  });

  it("resignation: the opponent of the resigning side wins", () => {
    expect(deriveTermination(new Chess(), { resigned: Color.White })).toEqual({
      result: Result.BlackWins,
      termination: Termination.Resignation,
    });
    expect(
      deriveTermination(new Chess(), { resigned: Color.Black })?.result
    ).toBe(Result.WhiteWins);
  });

  it("timeout: the flagged side loses when the opponent can mate", () => {
    expect(deriveTermination(new Chess(), { timedOut: Color.White })).toEqual({
      result: Result.BlackWins,
      termination: Termination.Timeout,
    });
  });

  it("timeout is a draw when the opponent cannot possibly mate (R5)", () => {
    const bareKing = new Chess("4k3/8/8/8/8/8/8/R3K3 w - - 0 1");
    expect(deriveTermination(bareKing, { timedOut: Color.White })).toEqual({
      result: Result.Draw,
      termination: Termination.InsufficientMaterial,
    });
    const kingAndBishop = new Chess("4k3/8/8/8/8/8/8/4KB2 w - - 0 1");
    expect(
      deriveTermination(kingAndBishop, { timedOut: Color.Black })?.result
    ).toBe(Result.Draw);
  });

  it("timeout still loses against a pawn or two minor pieces", () => {
    const pawn = new Chess("4k3/8/8/8/8/8/P7/4K3 w - - 0 1");
    expect(
      deriveTermination(pawn, { timedOut: Color.Black })?.termination
    ).toBe(Termination.Timeout);
    const twoMinors = new Chess("4k3/8/8/8/8/8/8/3NKB2 w - - 0 1");
    expect(
      deriveTermination(twoMinors, { timedOut: Color.Black })?.termination
    ).toBe(Termination.Timeout);
  });

  it("every termination it can produce agrees with its result", () => {
    const ends = [
      deriveTermination(play("f3", "e5", "g4", "Qh4#")),
      deriveTermination(new Chess("4k3/8/8/8/8/8/8/4KB2 w - - 0 1")),
      deriveTermination(new Chess(), { resigned: Color.Black }),
      deriveTermination(new Chess(), { timedOut: Color.Black }),
      deriveTermination(new Chess("4k3/8/8/8/8/8/8/R3K3 w - - 0 1"), {
        timedOut: Color.Black,
      }),
    ];
    ends.forEach((end) => {
      expect(end).toBeDefined();
      expect(agrees(end as GameEnd)).toBe(true);
    });
  });
});

describe("describeTermination", () => {
  const names = { white: "Ana", black: "Ben" };

  it("names the winner for decisive ends", () => {
    const end = (termination: Termination, result: Result) => ({
      result,
      termination,
    });
    expect(
      describeTermination(end(Termination.Checkmate, Result.WhiteWins), names)
    ).toBe("Ana won by checkmate");
    expect(
      describeTermination(end(Termination.Timeout, Result.BlackWins), names)
    ).toBe("Ben won on time");
  });

  it("keeps the wording the PGN headers used before the refactor", () => {
    expect(
      describeTermination(
        { result: Result.Draw, termination: Termination.Stalemate },
        names
      )
    ).toBe("Draw by stalemate");
  });
});
