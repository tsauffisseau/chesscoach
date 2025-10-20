
from __future__ import annotations
from dataclasses import dataclass
from typing import List
import chess, pandas as pd

@dataclass
class Issue:
    kind: str           # opening/tactical/positional
    rule_id: str        # late_castle, redevelop, hanging_piece
    ply: int
    san: str
    color: str
    label: str          # info/mistake/blunder
    details: str
    fen_after: str | None = None
    uci: str | None = None

def detect_late_castle(game: chess.pgn.Game, move_limit: int = 12) -> List[Issue]:
    issues: List[Issue] = []
    white_castled = False
    black_castled = False
    board = game.board()
    ply = 0
    for mv in game.mainline_moves():
        ply += 1
        san = board.san(mv)
        color = 'White' if board.turn else 'Black'
        board.push(mv)
        if 'O-O' in san:
            if color == 'White': white_castled = True
            else: black_castled = True
        if ply >= 2 * move_limit:  # after both sides had chance to castle
            break
    if not white_castled:
        issues.append(Issue("opening","late_castle", 2*move_limit, "—", "White","mistake",
                            f"White did not castle before move {move_limit}."))
    if not black_castled:
        issues.append(Issue("opening","late_castle", 2*move_limit, "—", "Black","mistake",
                            f"Black did not castle before move {move_limit}."))
    return issues

def detect_redevelop(df: pd.DataFrame, dev_limit_ply: int = 10) -> List[Issue]:
    """If in the first dev_limit_ply plies, the same minor piece is moved twice while
    < 4 unique pieces are developed, flag it."""
    issues: List[Issue] = []
    seen_from_white, seen_from_black = set(), set()
    moved_white, moved_black = set(), set()  # set of unique piece ids moved
    for row in df.itertuples(index=False):
        if row.ply > dev_limit_ply:
            break
        frm = row.uci[:2] if row.uci else None
        color = row.color
        san = row.san
        if color == 'White':
            if frm in seen_from_white and len(moved_white) < 4:
                issues.append(Issue("opening","redevelop", row.ply, san, color, "inaccuracy",
                                    "You moved the same piece twice before developing others."))
            seen_from_white.add(frm)
            moved_white.add(frm)
        else:
            if frm in seen_from_black and len(moved_black) < 4:
                issues.append(Issue("opening","redevelop", row.ply, san, color, "inaccuracy",
                                    "You moved the same piece twice before developing others."))
            seen_from_black.add(frm)
            moved_black.add(frm)
    return issues

def detect_hanging_after(game: chess.pgn.Game, df: pd.DataFrame) -> List[Issue]:
    """After each move, if the mover leaves any piece attacked and undefended, flag it."""
    issues: List[Issue] = []
    board = game.board()
    ply = 0
    for mv, row in zip(game.mainline_moves(), df.itertuples(index=False)):
        ply += 1
        color = 'White' if board.turn else 'Black'
        san = board.san(mv)
        board.push(mv)
        # scan pieces of mover on board
        for sq, piece in board.piece_map().items():
            if (piece.color and color=='White') or ((not piece.color) and color=='Black'):
                attackers = board.attackers(not piece.color, sq)
                defenders = board.attackers(piece.color, sq)
                if attackers and not defenders:
                    issues.append(Issue("tactical","hanging_piece", ply, san, color, "mistake",
                                        f"{color} has a hanging {piece.symbol().upper()} on {chess.square_name(sq)}.",
                                        fen_after=board.fen(), uci=row.uci))
                    break  # one flag per move
    return issues

def collect_issues(game: chess.pgn.Game, df: pd.DataFrame) -> List[Issue]:
    out: List[Issue] = []
    out.extend(detect_late_castle(game, move_limit=12))
    out.extend(detect_redevelop(df, dev_limit_ply=10))
    out.extend(detect_hanging_after(game, df))
    # sort by severity (rough): tactical first, then opening, positional
    order = {"blunder":3, "mistake":2, "inaccuracy":1, "info":0}
    out.sort(key=lambda x: (order.get(x.label,0), x.ply), reverse=True)
    return out
