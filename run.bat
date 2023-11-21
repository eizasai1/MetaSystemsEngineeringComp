@echo off
echo Installing python requirements
1>NUL python -m pip install -r requirements.txt
echo Running Program
python .\main.py