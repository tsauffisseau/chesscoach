
import os, io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from chesscoach.config import STOCKFISH_PATH, DEFAULT_DEPTH, PGN_SOURCE
from chesscoach.analysis import analyze_pgn, load_pgn
from chesscoach.eval_signals import detect_swings, find_turning_point
from chesscoach.stats import add_labels, precision_score, count_labels
from chesscoach.viz.render import render_position
from chesscoach.detectors import collect_issues

st.set_page_config(page_title="ChessCoach", layout="wide")

st.title("♟️ ChessCoach — Analyze your game and drill your mistakes")


with st.sidebar:
    st.header("Settings")
    engine_path = st.text_input("Stockfish path", value=os.environ.get("STOCKFISH_EXECUTABLE", STOCKFISH_PATH))
    depth = st.slider("Depth", min_value=8, max_value=24, value=DEFAULT_DEPTH, step=1)
    swing_cp = st.slider("Swing threshold (cp)", min_value=100, max_value=600, value=200, step=50)
    st.caption("Tip: set STOCKFISH_EXECUTABLE in your shell to avoid typing the path each time.")

tab1, tab2 = st.tabs(["Single game","Help"])

with tab1:
    st.subheader("Input PGN")
    col_a, col_b = st.columns(2)
    with col_a:
        up = st.file_uploader("Upload PGN file", type=["pgn"])
    with col_b:
        pgn_textarea = st.text_area("…or paste PGN", height=200, value="")

    run = st.button("Analyze", type="primary")

    if run:
        if not engine_path or not os.path.exists(engine_path):
            st.error("❌ Stockfish not found. Please set a valid path.")
            st.stop()

        if up is not None:
            pgn_text = up.read().decode("utf-8")
        elif pgn_textarea.strip():
            pgn_text = pgn_textarea
        elif PGN_SOURCE:
            pgn_text = load_pgn(PGN_SOURCE)
        else:
            st.error("Provide a PGN via upload, paste, or PGN_SOURCE env.")
            st.stop()

        with st.spinner("Running Stockfish analysis…"):
            df = analyze_pgn(pgn_text, engine_path, depth=depth)

        df = add_labels(df)
        swings = detect_swings(df, swing_cp=swing_cp)
        tp = find_turning_point(df)

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Plies", len(df))
        with col2: st.metric("Precision (proxy)", f"{precision_score(df)}%" )
        counts = count_labels(df)
        with col3: st.metric("Mistakes", counts["mistake"]) 
        with col4: st.metric("Blunders", counts["blunder"])

        # Eval curve
        st.subheader("Evaluation curve (White POV)")
        fig = plt.figure(figsize=(10,3))
        plt.plot(df["ply"], df["cp_after_white"], marker=".")
        plt.xlabel("Ply"); plt.ylabel("cp (White)" ); plt.grid(True, alpha=0.3)
        if swings:
            for s in swings:
                plt.axvline(s, linestyle=":", alpha=0.3)
        if tp:
            plt.axvline(tp, color="red", linestyle="--", alpha=0.8)
        st.pyplot(fig)

        # Key moments table
        st.subheader("Key moments")
        top_cpl = df.sort_values("centipawn_loss", ascending=False).head(5)[
            ["ply","fullmove","color","san","centipawn_loss","uci","fen_after","mate_after","cp_after_white"]
        ]
        st.dataframe(top_cpl, use_container_width=True)

        # Render images for the top-3 positions
        st.subheader("Positions (top‑3 centipawn losses)")
        for i, row in top_cpl.head(3).iterrows():
            img = render_position(row["fen_after"], row["cp_after_white"], row["mate_after"], row["uci"])
            st.image(img, caption=f"ply {int(row['ply'])} — {row['color']} played {row['san']} (CPL {int(row['centipawn_loss'] or 0)})" )

        # Principles / issues
        st.subheader("Principles you may have violated") 
        import chess.pgn, io
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        issues = collect_issues(game, df)
        if not issues:
            st.success("No major principle violations detected in this MVP heuristic.")
        else:
            for it in issues[:6]:
                st.markdown(f"**[{it.kind}] {it.rule_id}** at ply {it.ply} ({it.color} {it.san}) — {it.label}\n\n{it.details}")
                if it.fen_after:
                    img = render_position(it.fen_after, None, None, it.uci)
                    st.image(img, caption=f"After {it.color} {it.san}")

with tab2:
    st.markdown("""
**How centipawn loss is computed (MVP):**
- We evaluate the position before and after each move from White's POV.
- If White moved and eval decreased, CPL = drop amount (else 0).
- If Black moved and eval increased (helping White), CPL = increase amount (else 0).

**Turning point:** the move with the highest CPL.

These are simple proxies (sufficient for a first pass) — we can refine later by querying best lines and material deltas.
""")
