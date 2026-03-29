@echo off
title Transport Dashboard

cd /d C:\Pipeline-Transportor\dashboard

echo 🚀 Starting Dashboard...

python -m streamlit run dashboard.py

pause