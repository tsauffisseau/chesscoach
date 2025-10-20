
import pandas as pd

def classify_cpl(cpl, t_inacc=50, t_mist=150, t_blund=300):
    if pd.isna(cpl): return "good"
    if cpl >= t_blund: return "blunder"
    if cpl >= t_mist:  return "mistake"
    if cpl >= t_inacc: return "inaccuracy"
    return "good"

def add_labels(df: pd.DataFrame, t_inacc=50, t_mist=150, t_blund=300):
    df = df.copy()
    df["label"] = [classify_cpl(c, t_inacc,t_mist,t_blund) for c in df["centipawn_loss"]]
    return df

def precision_score(df: pd.DataFrame, t_inacc=50, t_mist=150, t_blund=300) -> float:
    # toy mapping → 0..100
    score = 0.0
    for c in df["centipawn_loss"].fillna(0):
        if c >= t_blund: score += 0.2
        elif c >= t_mist: score += 0.4
        elif c >= t_inacc: score += 0.7
        else: score += 1.0
    return round(100 * score / max(1, len(df)), 1)

def count_labels(df: pd.DataFrame):
    counts = df["label"].value_counts().to_dict()
    return {k:int(counts.get(k,0)) for k in ["good","inaccuracy","mistake","blunder"]}
