@echo off
cd /d "D:\PROJECTS\Asthma Sheild"
call .\venv\Scripts\Activate.bat
cd frontend
python -m streamlit run app.py