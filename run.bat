@echo off
set ENGINE_PATH=%~dp0bin\stockfish\stockfish.exe
call .venv\Scripts\activate
streamlit run ui\streamlit_app.py
