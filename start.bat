@echo off
echo Starting Love Message Service...
cd /d %~dp0
set PYTHONPATH=%PYTHONPATH%;%~dp0
python src/main.py
pause 