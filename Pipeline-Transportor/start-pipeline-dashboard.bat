@echo off
title Transport System Launcher

echo 🚀 Starting Pipeline + Dashboard...

start cmd /k "cd /d C:\Pipeline-Transportor\src && python main.py"

start cmd /k "cd /d C:\Pipeline-Transportor\dashboard && python -m streamlit run dashboard.py"

start http://localhost:8501

pause