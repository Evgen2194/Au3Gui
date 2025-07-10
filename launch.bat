@echo off
SET SCRIPT_DIR=%~dp0
SET PYTHON_DIR=%SCRIPT_DIR%python_embedded
SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts;%PATH%
SET PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%

REM Check if pip is installed
if not exist "%PYTHON_DIR%\Scripts\pip.exe" (
    echo Installing pip...
    "%PYTHON_DIR%\python.exe" -m ensurepip --upgrade
)

REM Install required packages
echo Installing required packages...
"%PYTHON_DIR%\python.exe" -m pip install --no-warn-script-location -r "%SCRIPT_DIR%requirements.txt"

echo Starting AutoItCodeWriter...
"%PYTHON_DIR%\python.exe" "%SCRIPT_DIR%\AutoItCodeWriter V1.1.py"
pause
