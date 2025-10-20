
from __future__ import annotations
import os, argparse, pandas as pd
import chess, chess.pgn
from typing import Optional

from .config import STOCKFISH_PATH, DEFAULT_DEPTH
from .parse_pgn import parse_pgn_text
from .engine import open_engine, eval_cp_white
 
def load_pgn(source_path_or_url: Optional[str]) -> str:
    if not source_path_or_url:
        raise ValueError("Provide a PGN source via --pgn or PGN_SOURCE env.")
    if source_path_or_url.lower().startswith(("http://","https://")):
        import requests
        r = requests.get(source_path_or_url, timeout=30)
        r.raise_for_status()
        return r.text
    with open(source_path_or_url, "r", encoding="utf-8") as f:
        return f.read()

def analyze_pgn(pgn_text: str, engine_path: str, depth: int = DEFAULT_DEPTH) -> pd.DataFrame:
    game = parse_pgn_text(pgn_text)
    board = game.board()

    engine = open_engine(engine_path)
    rows = []
    ply = 0
    cp_before, mate_before = eval_cp_white(board, engine, depth=depth)

    for mv in game.mainline_moves():
        ply += 1
        color = "White" if board.turn else "Black"    # side to move BEFORE the push
        san = board.san(mv)
        uci = mv.uci()
        fen_before = board.fen()

        board.push(mv)

        fen_after = board.fen()
        cp_after, mate_after = eval_cp_white(board, engine, depth=depth)

        # centipawn loss from the mover's perspective, using White's POV eval
        delta = None
        cpl = None
        if cp_before is not None and cp_after is not None:
            delta = cp_after - cp_before  # positive means White improved
            if color == "White":
                # White moved; loss if eval decreased
                cpl = max(0, cp_before - cp_after)
            else:
                # Black moved; loss if eval increased (benefiting White)
                cpl = max(0, cp_after - cp_before)

        rows.append(dict(
            ply=ply,
            fullmove=board.fullmove_number,
            color=color,
            san=san,
            uci=uci,
            fen_before=fen_before,
            fen_after=fen_after,
            cp_before_white=cp_before,
            cp_after_white=cp_after,
            mate_before=mate_before,
            mate_after=mate_after,
            centipawn_loss=cpl,
            delta_cp_white=delta,
        ))
        cp_before, mate_before = cp_after, mate_after

    engine.quit()
    return pd.DataFrame(rows)

if __name__ == "__main__":
    from .config import PGN_SOURCE
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", type=str, help="Stockfish path (override)" )
    ap.add_argument("--pgn", type=str, help="PGN file path or URL" )
    ap.add_argument("--depth", type=int, default=DEFAULT_DEPTH)
    args = ap.parse_args()

    engine_path = args.engine or os.environ.get("STOCKFISH_EXECUTABLE") or STOCKFISH_PATH
    if not (engine_path and os.path.exists(engine_path)):
        raise FileNotFoundError(f"Stockfish not found at: {engine_path!r}")

    pgn_text = load_pgn(args.pgn or os.environ.get("PGN_SOURCE", PGN_SOURCE))
    df = analyze_pgn(pgn_text, engine_path, depth=args.depth)
    print(df.head(20))
    print("Total plies:", len(df))
