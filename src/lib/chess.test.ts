import { Chess } from "chess.js";
import { describe, expect, it } from "vitest";
import { getEvaluateGameParams } from "./chess";

describe("getEvaluateGameParams", () => {
  it("returns nothing to evaluate for a game without moves", () => {
    expect(getEvaluateGameParams(new Chess())).toEqual({
      fens: [],
      uciMoves: [],
    });
  });

  it("returns one more fen than moves", () => {
    const game = new Chess();
    game.move("e4");
    game.move("e5");
    const { fens, uciMoves } = getEvaluateGameParams(game);
    expect(uciMoves).toEqual(["e2e4", "e7e5"]);
    expect(fens).toHaveLength(3);
    expect(fens[2]).toBe(game.fen());
  });
});
