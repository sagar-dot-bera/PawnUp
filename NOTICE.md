# Notice

## PawnUp

PawnUp is free software licensed under the **GNU Affero General Public License,
version 3 only** (AGPL-3.0-only). See [LICENSE](LICENSE).

Source code of the running service: https://github.com/sagar-dot-bera/PawnUp
(also linked as "Source" in the app's navigation bar, as AGPL section 13 requires).

**Modified by the PawnUp team since 30 October 2026.** The changes are recorded
in this repository's git history.

## Upstream: Chesskit

The frontend is a modified copy of [Chesskit](https://github.com/GuillaumeSD/Chesskit)
by GuillaumeSD and contributors, licensed under the AGPL-3.0
(upstream `COPYING.md`: "version 3 of the License"; upstream's `package.json`
says `GPL-3.0-only`, which contradicts its own `COPYING.md` and `LICENCE`; we follow
the licence files).

- Forked from upstream commit `9622d502ab9fc84fc1486e22310a7df229a37e93`
  ("MoveClassification turn bug fixed (#92)", 2026-05-08, upstream `main` at the time).
  Found by diffing our first commit (`ca8e013`) against every upstream commit: it
  differs from `9622d50` only by deletions (other Stockfish versions, Sentry, Firebase,
  AWS CDK files, Chesskit's own icons) plus 8 changed lines.
- Chesskit's name, logo and icons are not used by PawnUp.

## Stockfish (GPLv3)

The engines under `public/engines/` are Stockfish builds, licensed under the GNU
General Public License v3:

- `stockfish-18/*`: Stockfish.js 18 (c) 2026 Chess.com, LLC, built from
  https://github.com/nmrugg/stockfish.js, based on
  https://github.com/official-stockfish/Stockfish. Neural nets by Linmiao Xu (linrock).
- `stockfish-11.js`: Stockfish 11 by T. Romstad, M. Costalba, J. Kiiski, G. Linscott
  and contributors; multi-variant support by Daniel Dugovic
  (https://github.com/ddugovic/Stockfish); compiled to JavaScript/WebAssembly by
  Niklas Fiekas.

The corresponding source of these binaries is available at the repositories above.

## Assets

Taken from upstream's `COPYING.md` at the fork commit. We have not re-verified any
of these licences ourselves.

**Piece sets (`public/piece/*`)**

| Licence (as stated upstream) | Sets |
|---|---|
| CC BY-NC-SA 4.0 | horsey, california, caliente, maestro, fresca, cardinal, icpieces, gioco, tatiana, staunty, dubrovny, anarcandy, cooke, monarchy |
| CC BY-NC-SA 2.5 | xkcd |
| CC BY 4.0 | kiwen-suwi, firi |
| CC BY-SA 4.0 | shapes |
| CC BY-ND 4.0 | chicago, iowa, oslo |
| CC0 1.0 | rhosgfx |
| GPLv2+ | cburnett, merida |
| GPLv3+ | mpchess |
| AGPLv3+ | letter, pirouetti, pixel |
| Apache 2.0 | chessnut |
| MIT | fantasy, spatial, celtic |
| "free for personal non-commercial use" (non-free) | alpha |
| "freeware" (non-free) | chess7, companion, leipzig |
| no licence stated upstream (non-free/unknown) | reillycraig, symmetric, riohacha |
| **not listed upstream at all (unverified)** | governor, kosal |

Authors are listed in upstream's `COPYING.md`. The non-commercial (NC) and non-free
sets limit commercial redistribution; PawnUp is a course project, but remove those
sets before any commercial use.

**Sounds (`public/sounds/*`)**: from Lichess (https://github.com/lichess-org/lila),
AGPL-3.0, as stated upstream.

**Merida chess font (`src/components/prettyMoveSan/chess_merida_unicode.ttf`)**:
not listed in upstream's `COPYING.md`. **Unverified.** The Merida piece set is by
Armando Hernandez Marroquin (GPLv2+ per upstream); the font's own licence is unknown.

**Openings data (`src/data/openings.ts`)**: not credited upstream. **Unverified.**
It appears to be derived from the Lichess chess-openings dataset (CC0), but we have
not confirmed that.

**PawnUp logo, favicons, social image**: original work by the PawnUp team, released
under the same AGPL-3.0-only licence as the code.
