# config.py — env vars
import os

# Path to Stockfish binary (set this in your shell/env)
STOCKFISH_PATH = os.environ.get("STOCKFISH_EXECUTABLE", "")

# Default analysis depth (robuste si la var est mal formée)
try:
    DEFAULT_DEPTH = int(os.environ.get("CC_DEPTH", "12"))
except ValueError:
    DEFAULT_DEPTH = 12

# Optional default PGN source (file path or URL)
PGN_SOURCE = os.environ.get("PGN_SOURCE", "")
