import { EngineName, MoveClassification } from "./types/enums";

// One place for the product name, so the PGN headers we write and the check that
// reads them back (loadGame.tsx) cannot drift apart.
export const BRAND_NAME = "PawnUp";
export const BRAND_PGN_EVENT = `${BRAND_NAME} Game`;
export const BRAND_PGN_SITE = BRAND_NAME;

// AGPL-3.0 section 13: users of the running service must be able to get its source.
export const SOURCE_URL = "https://github.com/sagar-dot-bera/PawnUp";
export const UPSTREAM_URL = "https://github.com/GuillaumeSD/Chesskit";

export const MAIN_THEME_COLOR = "#3B9AC6";
export const LINEAR_PROGRESS_BAR_COLOR = "#3B9AC6";

export const CLASSIFICATION_COLORS: Record<MoveClassification, string> = {
  [MoveClassification.Opening]: "#dbac86",
  [MoveClassification.Forced]: "#dbac86",
  [MoveClassification.Splendid]: "#19d4af",
  [MoveClassification.Perfect]: "#3894eb",
  [MoveClassification.Best]: "#22ac38",
  [MoveClassification.Excellent]: "#22ac38",
  [MoveClassification.Okay]: "#74b038",
  [MoveClassification.Inaccuracy]: "#f2be1f",
  [MoveClassification.Mistake]: "#e69f00",
  [MoveClassification.Blunder]: "#df5353",
};

export const DEFAULT_ENGINE: EngineName = EngineName.Stockfish18Lite;
export const STRONGEST_ENGINE: EngineName = EngineName.Stockfish18;

export const ENGINE_LABELS: Record<
  EngineName,
  { small: string; full: string; sizeMb: number }
> = {
  [EngineName.Stockfish18]: {
    full: "Stockfish 18 (108MB)",
    small: "Stockfish 18",
    sizeMb: 108,
  },
  [EngineName.Stockfish18Lite]: {
    full: "Stockfish 18 Lite (7MB)",
    small: "Stockfish 18 Lite",
    sizeMb: 7,
  },
  [EngineName.Stockfish11]: {
    full: "Stockfish 11 (HCE)",
    small: "Stockfish 11",
    sizeMb: 2,
  },
};

export const PIECE_SETS = [
  "alpha",
  "anarcandy",
  "caliente",
  "california",
  "cardinal",
  "cburnett",
  "celtic",
  "chess7",
  "chessnut",
  "chicago",
  "companion",
  "cooke",
  "dubrovny",
  "fantasy",
  "firi",
  "fresca",
  "gioco",
  "governor",
  "horsey",
  "icpieces",
  "iowa",
  "kiwen-suwi",
  "kosal",
  "leipzig",
  "letter",
  "maestro",
  "merida",
  "monarchy",
  "mpchess",
  "oslo",
  "pirouetti",
  "pixel",
  "reillycraig",
  "rhosgfx",
  "riohacha",
  "shapes",
  "spatial",
  "staunty",
  "symmetric",
  "tatiana",
  "xkcd",
] as const satisfies string[];
