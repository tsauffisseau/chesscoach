
# ChessCoach — MVP v0.1

Analyze a PGN with Stockfish (depth N), detect big evaluation swings, label moves (inaccuracy/mistake/blunder),
and generate a one‑page report with a clickable evaluation curve and key positions.

## Quickstart

```bash
# 1) Create & activate a virtual env
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# 2) Install deps
pip install -r requirements.txt

# 3) Install Stockfish (binary) and set the path
#   - Linux:   sudo apt-get install stockfish
#   - macOS:   brew install stockfish
#   - Windows: Download from https://stockfishchess.org/download/
# Then export env var (adapt the path):
export STOCKFISH_EXECUTABLE="/usr/bin/stockfish"    # macOS/Linux example
# setx STOCKFISH_EXECUTABLE "C:\path\to\stockfish.exe"   # Windows PowerShell

# 4) Run the app
streamlit run ui/streamlit_app.py
```

## CLI (optional)
```bash
python -m chesscoach.analysis --pgn data_pgn/partie1.pgn --depth 12 --engine "$STOCKFISH_EXECUTABLE"
```

## Project layout
```
src/chesscoach/
  __init__.py
  config.py
  parse_pgn.py
  engine.py
  analysis.py
  eval_signals.py
  stats.py
  detectors.py
  viz/
    render.py
ui/
  streamlit_app.py
data_pgn/
  partie1.pgn
```

## Roadmap
- v0.2: richer heuristics (tactics motifs), clickable eval timeline
- v0.3: account‑level dashboard, openings/endgame repertoire

License: MIT
