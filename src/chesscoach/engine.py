
import chess, chess.engine
import sys, asyncio

def open_engine(engine_path: str):
    # Windows needs the Proactor loop to spawn subprocesses
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        except Exception:
            pass

    eng = chess.engine.SimpleEngine.popen_uci(engine_path)
    # Optionnel: paramètres raisonnables
    try:
        eng.configure({"Threads": 4, "Hash": 256})
    except Exception:
        pass
    return eng

def eval_cp_white(board: chess.Board, engine, depth: int = 12):
    """Return (cp_white, mate_in) from White's POV.
    cp in centipawns; mate_in integer if mate sequence known, else None.
    """
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    score = info["score"].pov(chess.WHITE)
    if score.is_mate():
        return None, score.mate()
    return score.score(mate_score=100000), None
