@echo off
SET SCRIPT_DIR=%~dp0
SET PYTHON_DIR=%SCRIPT_DIR%python_embedded
SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts;%PATH%

REM Create directories if they don't exist
if not exist "%PYTHON_DIR%\Lib\site-packages" mkdir "%PYTHON_DIR%\Lib\site-packages"
if not exist "%PYTHON_DIR%\Scripts" mkdir "%PYTHON_DIR%\Scripts"

REM Download get-pip.py if not exists
if not exist "%SCRIPT_DIR%get-pip.py" (
    echo Downloading get-pip.py...
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
)

REM Install pip
echo Installing pip...
"%PYTHON_DIR%\python.exe" "%SCRIPT_DIR%get-pip.py" --no-warn-script-location

REM Install required packages
echo Installing required packages...
"%PYTHON_DIR%\Scripts\pip.exe" install --no-warn-script-location -r "%SCRIPT_DIR%requirements.txt"

REM Copy DLLs to the correct location
echo Setting up pywin32...
if exist "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pythoncom312.dll" (
    copy /Y "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pythoncom312.dll" "%PYTHON_DIR%"
    copy /Y "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pythoncom312.dll" "%PYTHON_DIR%\Lib\site-packages"
)
if exist "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pywintypes312.dll" (
    copy /Y "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pywintypes312.dll" "%PYTHON_DIR%"
    copy /Y "%PYTHON_DIR%\Lib\site-packages\pywin32_system32\pywintypes312.dll" "%PYTHON_DIR%\Lib\site-packages"
)

REM Copy win32 files to make them discoverable
if exist "%PYTHON_DIR%\Lib\site-packages\win32" (
    xcopy /E /I /Y "%PYTHON_DIR%\Lib\site-packages\win32\*.pyd" "%PYTHON_DIR%\Lib\site-packages"
)

echo Checking imports...
"%PYTHON_DIR%\python.exe" "%SCRIPT_DIR%\check_imports.py"

echo Starting AutoItCodeWriter...
"%PYTHON_DIR%\python.exe" "%SCRIPT_DIR%\AutoItCodeWriter V1.1.py"
pause
