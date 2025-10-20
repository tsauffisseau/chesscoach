@echo off
set PYTHONPATH=%cd%\src
streamlit run ui\streamlit_app.py --server.fileWatcherType none
