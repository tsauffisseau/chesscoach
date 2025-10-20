
from __future__ import annotations
from typing import List, Optional
import pandas as pd

def detect_swings(df: pd.DataFrame, swing_cp: int = 200) -> List[int]:
    """Return list of plies where abs delta in eval (White POV) >= swing_cp."""
    swings = []
    prev = None
    for row in df.itertuples(index=False):
        cp = row.cp_after_white
        if prev is not None and cp is not None and abs(cp - prev) >= swing_cp:
            swings.append(int(row.ply))
        prev = cp
    return swings

def find_turning_point(df: pd.DataFrame) -> Optional[int]:
    """Return ply of the maximum centipawn_loss (None if empty)."""
    if "centipawn_loss" not in df or df.empty:
        return None
    idx = df["centipawn_loss"].fillna(-1).idxmax()
    if pd.isna(df.loc[idx, "centipawn_loss"]):
        return None
    return int(df.loc[idx, "ply"])
