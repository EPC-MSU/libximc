@echo off
cd ..
venv\Scripts\python run.py
if exist ".\package\" (
    echo.
    echo Building distribution...
    cd ".\package\"
    python -m pip install --upgrade build
    python -m build
)
pause