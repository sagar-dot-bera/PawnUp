# Ubiquitous Language

The words this product is about. Use these terms in code, UI copy, issues and conversation. "Named in code at" points to where the term already lives; *planned* means it is in the [roadmap](ROADMAP.md) but has no code yet, and new code must use the name given here.

## Playing

| Term | Definition | Aliases to avoid | Named in code at |
|---|---|---|---|
| **Game** | One chess game between two sides, from the starting position to a result. It can be live (in progress) or finished, and it is the thing that gets saved, analyzed and replayed. | match, round, session | `Game` in `src/types/game.ts` |
| **Player** | A side's participant in one game: their name, rating and title *as recorded in that game*. A player is not an account. | user (when you mean the game side), opponent (as a type name) | `Player` in `src/types/game.ts` |
| **Color** | Which side a player controls: White or Black. | side, team, `"w"`/`"b"` literals in new code | `Color` enum in `src/types/enums.ts` |
| **Move** | One legal action by one color, stored as SAN (`Nf3`) for display and UCI (`g1f3`) for engines. | ply (except in engine maths), turn, action | chess.js `Move`; `uciMoves` in `src/types/eval.ts` |
| **Position** | The full state of the board at one moment, identified by its FEN. | board state, snapshot, frame | `fen` throughout; `CurrentPosition` in `src/types/eval.ts` |
| **FEN** | Text notation for a single position. | position string, board string | `fen` fields; `src/lib/chess.ts` |
| **PGN** | Text notation for a whole game, including headers (players, result, time control). Used for import and export. | game file, game string | `pgn` in `Game`, `getGameFromPgn` in `src/lib/chess.ts` |
| **Result** | How the game score ended: `1-0`, `0-1`, `½-½`, or `*` while still in progress. | outcome, score, winner | `Game.result` |
| **Termination** | *Why* the game ended: checkmate, resignation, timeout, stalemate, abandonment, agreement. | end reason, result (see ambiguities) | `Game.termination` |
| **Time Control** | The clock rules agreed before the game, written as `base+increment` (e.g. `5+3`). | clock (see ambiguities), speed, timer settings | `Game.timeControl`, `timeControlChip.tsx` |
| **Clock** | The live remaining time for one color during a game. Owned by the server. | timer, countdown | *planned* |
| **Variant** | A rule set other than standard chess. Currently only **Chess960**. | mode, game type | *planned* (Chess960 is handled via starting FEN today) |
| **Chess960** | Variant with one of 960 randomized back-rank starting positions. | Fischer Random, FRC, 960 | starting FEN in `gameSettingsDialog.tsx` |
| **Reconnection** | A player rejoining their own live game after losing connection, before the abandonment timeout. | resume, rejoin | *planned* |
| **Abandonment** | A termination where a player stays disconnected past the timeout and loses. | disconnect loss, quit | *planned* |

## Competing

| Term | Definition | Aliases to avoid | Named in code at |
|---|---|---|---|
| **User** | A registered account on our platform: login, profile, friends, ratings. One user is the player in many games. | player (for accounts), member, account holder | *planned* |
| **Guest** | Someone using the site without an account. Can play the engine and analyze, cannot play rated games. | anonymous user, visitor | *planned* |
| **Rating** | A user's Glicko-2 strength number for one rating category. Changes after each rated game. | Elo, ELO, score, points, MMR | `Player.rating` (stores the rating shown in an imported game) |
| **Rating Category** | The bucket a rating belongs to, derived from time control: Bullet, Blitz, Rapid, Classical (and Chess960). | pool, ladder, queue type | *planned* |
| **Rated Game** | A game whose result changes both users' ratings. Opposite: **Casual Game**. | ranked game, competitive game | *planned* |
| **Matchmaking** | The server pairing two waiting users with the same time control and close ratings. | lobby, queue system, auto-match | *planned* |
| **Seek** | One user's entry in the matchmaking queue: "I want a 5+3 rated game". | queue entry, ticket, request | *planned* |
| **Challenge** | A direct invitation from one user to a specific user (or via a link) to play a game. Accepted challenges create a game. | invite, invitation, duel, match request | *planned* |
| **Tournament** | A scheduled competition of many games among registered users, with standings. Its **format** is Swiss or Arena. | event, competition, cup | *planned* |
| **Pairing** | One tournament assignment of two users (and colors) to a game. | match-up, fixture | *planned* |
| **Standings** | A tournament's ordered table of users and their tournament scores. | leaderboard (see ambiguities), rankings, table | *planned* |
| **Leaderboard** | Global list of top users by rating in one rating category. | rankings, top list, hall of fame | *planned* |

## Social

| Term | Definition | Aliases to avoid | Named in code at |
|---|---|---|---|
| **Profile** | The public page of a user: ratings, recent games, stats. | user page, account page | *planned* |
| **Friend** | A user who accepted a mutual friend request. One-way following is not a friendship. | follower, contact, buddy | *planned* |
| **Message** | A private text sent from one user to another outside a game. | DM, chat (see ambiguities), mail | *planned* |
| **Game Chat** | Text exchanged by the two players (and optionally spectators) inside one live game. | messages, in-game messages | *planned* |
| **Spectator** | A user or guest watching a live game they are not playing. Read-only. | viewer, watcher, observer | *planned* |

## Analyzing

| Term | Definition | Aliases to avoid | Named in code at |
|---|---|---|---|
| **Engine** | A chess-playing program, today Stockfish running in the browser, used both to analyze and to play against. | AI, bot, computer (in code) | `UciEngine` in `src/lib/engine/uciEngine.ts`, `EngineName` enum |
| **Computer Opponent** | The engine playing one color against a user, at a chosen **Engine Elo**. UI wording only; in code it is the engine. | bot, AI, CPU | `src/sections/play/` |
| **Engine Elo** | The playing strength the engine is limited to when it is a computer opponent (Stockfish `UCI_Elo`). Not a user rating. | level, difficulty, rating | `engineEloAtom` in `src/sections/play/states.ts` |
| **Analysis** | Running the engine over every position of a game to produce a game evaluation. Also the page where this is shown. | review, scan, check | `src/sections/analysis/`, `analyzeButton.tsx` |
| **Evaluation** | The engine's numeric judgement of a position: centipawns (`cp`) or mate-in-N (`mate`), from White's point of view. | score, eval bar value | `cp` / `mate` in `LineEval` |
| **Line** | One sequence of best moves the engine found from a position, with its evaluation and depth. A position eval has up to *Multi-PV* lines. | variation, PV (in UI), continuation | `LineEval` in `src/types/eval.ts` |
| **Best Move** | The first move of the top line. | top move, engine move, suggestion | `PositionEval.bestMove` |
| **Position Eval** | All engine output for one position: lines, best move, classification of the move that led here, opening name. | analysis result, node | `PositionEval` |
| **Game Eval** | The result of analyzing a whole game: one position eval per position, accuracy, estimated Elo, engine settings used. | report, game analysis object, review | `GameEval` |
| **Depth** | How many plies deep the engine searched. | level, strength | `depth` in `LineEval`, `engineDepthAtom` |
| **Multi-PV** | How many lines the engine reports per position. | lines count, variations | `multiPv` fields, `engineMultiPvAtom` |
| **Move Classification** | The label given to a played move by comparing it with the engine's best line: Splendid, Perfect, Best, Excellent, Okay, Inaccuracy, Mistake, Blunder, plus Forced and Book. | annotation, grade, rating (never) | `MoveClassification` enum, `src/lib/engine/helpers/moveClassification.ts` |
| **Blunder / Mistake / Inaccuracy** | Classifications for moves that lose large / medium / small amounts of win percentage. Always these three words, in this order of severity. | error, bad move, ?? / ? / ?! in code | `MoveClassification.Blunder` etc. |
| **Splendid** | A strong move that involves a sacrifice and is hard to find. Shown as `!!`. | brilliant, great | `MoveClassification.Splendid` |
| **Perfect** | The only good move in the position. Shown as `!`. | great, only move | `MoveClassification.Perfect` |
| **Win Percentage** | An evaluation converted to the chance of winning (0–100). Basis for accuracy and classification. | win probability, expected score | `src/lib/engine/helpers/winPercentage.ts` |
| **Accuracy** | A 0–100 score per color for how close their moves stayed to the engine's, over a whole game. | precision, CAPS, performance | `Accuracy`, `computeAccuracy` in `accuracy.ts` |
| **Estimated Elo** | The rating a color *played like* in one game, guessed from accuracy. Not a user rating. | performance rating, game rating | `EstimatedElo`, `computeEstimatedElo` |
| **Evaluation Graph** | The chart of evaluation over the moves of a game. | eval chart, advantage graph | `src/sections/analysis/panelBody/graphTab/` |
| **Opening** | The named opening a game followed, e.g. "Sicilian Defense: Najdorf". | ECO name, book line | `PositionEval.opening`, `src/data/openings.ts` |
| **Game Phase** | One of three parts of a game: **Opening Phase**, **Middlegame**, **Endgame**. Used for per-phase accuracy. | stage, section, period | *planned* |
| **Missed Tactic** | A position where a winning tactic was available and the player did not play it. Detected during analysis. | missed chance, missed opportunity | *planned* |
| **Analysis Board** | The interactive board on the analysis page where a user explores moves and variations freely. | sandbox, explorer, editor | `boardAtom` in `src/sections/analysis/states.ts` |
| **Game Origin** | Where an imported game came from: PGN, Chess.com, or Lichess. | source, provider, platform | `GameOrigin` enum |
| **Game Database** | The saved collection of a user's games. Today it lives in the browser (IndexedDB); later on the server. | library, archive, history | `useGameDatabase`, `src/pages/database.tsx` |

## Training

| Term | Definition | Aliases to avoid | Named in code at |
|---|---|---|---|
| **Puzzle** | A position with one correct solution line that a user must find. | tactic (as the object), exercise, problem, quiz | *planned* |
| **Solution** | The move sequence that solves a puzzle. | answer, key line | *planned* |
| **Theme** | The tactical idea a puzzle trains: fork, pin, mate-in-2, back-rank, etc. | tag, category, motif | *planned* |
| **Weakness** | A theme or game phase where a user's games show repeated mistakes or blunders. Drives personalized puzzles. | weak spot, problem area | *planned* |
| **Personalized Puzzle** | A puzzle chosen or generated for a user from their weaknesses, or built from a blunder in their own games. | custom puzzle, recommended puzzle | *planned* |
| **Puzzle Rating** | A user's Glicko-2 rating for solving puzzles, separate from game ratings. | puzzle score, puzzle Elo | *planned* |

## Flagged ambiguities

Each entry: the word(s), the conflict, and which meaning wins.

1. **"Game" means three things.**
   - `Game` in `src/types/game.ts` is the saved record (our meaning).
   - `gameAtom` in both `src/sections/analysis/states.ts` and `src/sections/play/states.ts` holds a chess.js `Chess` instance, which is the *rules engine object*, not our domain game.
   - `LoadedGame` is a row in the import list from Chess.com/Lichess.

   **Winner: Game = the domain record.** The chess.js object should be called `chess` (e.g. `chessAtom`) in new code, and `LoadedGame` should become `ImportableGame`.

2. **"Board" means both the UI and a game copy.** `src/components/board/` is the visual board, but `boardAtom` is a second chess.js instance holding the line being explored. **Winner: Board = the visual component.** The explored copy is the **Analysis Board** state; rename to `analysisBoardAtom` when touched.

3. **"Player" vs "User".** Chesskit has no accounts, so `Player` means "whoever sat at this color". Once we add accounts, people will say "player" for both. **Winner: User = account; Player = a user's (or a stranger's, for imports) participation in one game.** A `Player` may reference a `userId`; it never replaces it.

4. **"Elo" vs "Rating".** Code says `rating` (`Player.rating`), `engineElo`, and `estimatedElo`; our ratings will be Glicko-2, not Elo. **Winner: Rating = a user's Glicko-2 number.** "Elo" survives only in the two compound terms **Engine Elo** and **Estimated Elo**, which are never shown as a user's rating.

5. **"Opening" means three things.**
   - The named opening (`PositionEval.opening`).
   - The first phase of a game (needed for per-phase accuracy).
   - `MoveClassification.Opening`, which actually means "this move is in the opening book".

   **Winner: Opening = the named opening.** The phase is **Opening Phase**. The classification is **Book Move**: rename `MoveClassification.Opening` to `Book` (keep the stored value compatible with existing saved evals).

6. **"Eval" means both a number and a container.** Players say "the eval is +1.5" (a number), while `PositionEval`, `GameEval` and `SavedEval` are objects holding lines, best move and more. **Winner: Evaluation = the number (`cp` / `mate`).** The containers keep their full names **Position Eval** and **Game Eval**; never call either one just "eval" in new code.

7. **"Analysis" vs "Review" vs "Evaluation".** The README used "review", the code uses "analyze" and "evaluate". **Winner: Analysis = the process and the page; Evaluation = the number.** Don't use "review".

8. **"Line" vs "PV" vs "Variation".** The engine calls it a PV, the type is `LineEval`, players say "variation". **Winner: Line.** "PV" stays only inside engine-parsing code (`pv` field, `multiPv`); "Variation" is reserved for a user's own side branch on the analysis board.

9. **"Brilliant/Great" vs "Splendid/Perfect".** The old README said "Brilliant, Great"; the code and UI say Splendid and Perfect. **Winner: Splendid and Perfect**, as in code. Don't use Brilliant or Great (they are another site's labels).

10. **"Board orientation" has two types.** `boardOrientationAtom` in `src/sections/analysis/states.ts` is a boolean (`true` = White at bottom), but the board component's `boardOrientation` prop is a `Color`. **Winner: Color.** Convert the atom to `Color` when touched.

11. **"Clock" vs "Time Control".** Both get called "the clock". **Winner: Time Control = the rules (5+3); Clock = live remaining time.**

12. **"Result" vs "Termination".** "How did the game end?" can mean the score or the reason. **Winner: Result = the score (`1-0`); Termination = the reason (timeout).**

13. **"Engine" vs "Bot" vs "Computer" vs "AI".** The brief says "computer opponents". **Winner: Engine in code and docs; Computer Opponent only in UI copy for the play-against-engine mode.** Never "AI" or "bot".

14. **"Match" vs "Game".** **Winner: Game.** "Match" appears only inside **Matchmaking**. A future multi-game series between two users would be a new term, not "match" by default.

15. **"Leaderboard" vs "Standings".** **Winner: both, with different scopes.** Leaderboard = global ranking by rating; Standings = one tournament's table.

16. **"Tactic" as object vs pattern.** **Winner: Puzzle = the training object; Theme = the tactical pattern; Missed Tactic = an analysis finding in a real game.** Don't call a puzzle a "tactic".

17. **"Message" vs "Chat".** **Winner: Message = private user-to-user; Game Chat = inside a live game.** A bare "chat" is not a term.
