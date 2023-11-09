@echo off
set PATH=venv\Scripts;%PATH%
set PYTHONPATH=src
python src/main.py >> out.log 2>&1
