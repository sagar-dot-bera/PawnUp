import { useAtomValue } from "jotai";
import {
  enginePlayNameAtom,
  gameAtom,
  isGameInProgressAtom,
  playerColorAtom,
} from "./states";
import { Button, Grid2 as Grid, Typography } from "@mui/material";
import { Color } from "@/types/enums";
import { setGameHeaders } from "@/lib/chess";
import { ENGINE_LABELS } from "@/constants";
import {
  describeTermination,
  deriveTermination,
  Termination,
} from "@/lib/termination";
import { useGameDatabase } from "@/hooks/useGameDatabase";
import { useRouter } from "next/router";

export default function GameRecap() {
  const game = useAtomValue(gameAtom);
  const playerColor = useAtomValue(playerColorAtom);
  const engineName = useAtomValue(enginePlayNameAtom);
  const isGameInProgress = useAtomValue(isGameInProgressAtom);
  const { addGame } = useGameDatabase();
  const router = useRouter();

  if (isGameInProgress || !game.history().length) return null;

  const getResultLabel = () => {
    const resigned = game.isGameOver() ? undefined : playerColor;
    const end = deriveTermination(game, { resigned });
    if (!end) return "";
    if (end.termination === Termination.Resignation) return "You resigned";

    const opponentName = ENGINE_LABELS[engineName].small;
    return describeTermination(end, {
      white: playerColor === Color.White ? "You" : opponentName,
      black: playerColor === Color.Black ? "You" : opponentName,
    });
  };

  const handleOpenGameAnalysis = async () => {
    const gameToAnalysis = setGameHeaders(game, {
      resigned: !game.isGameOver() ? playerColor : undefined,
    });
    const gameId = await addGame(gameToAnalysis);

    router.push({ pathname: "/", query: { gameId } });
  };

  return (
    <Grid
      container
      justifyContent="center"
      alignItems="center"
      gap={2}
      size={12}
    >
      <Grid container justifyContent="center" size={12}>
        <Typography>{getResultLabel()}</Typography>
      </Grid>

      <Button variant="outlined" onClick={handleOpenGameAnalysis}>
        Open game analysis
      </Button>
    </Grid>
  );
}
