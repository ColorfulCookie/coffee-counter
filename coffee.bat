@echo off
REM Batch file to run the Python coffee logger script

REM Get the directory where this batch file is located
SET SCRIPT_DIR=%~dp0

REM Change the current directory to the script's directory
REM This ensures that the Python script runs in its own directory,
REM so it can find/create its database file correctly.
cd /d "%SCRIPT_DIR%"

REM --- IMPORTANT ---
REM Replace 'coffee.py' with the actual name of your Python script if it's different.
SET PYTHON_SCRIPT_NAME=coffee.py

REM Check if the Python script exists
IF NOT EXIST "%PYTHON_SCRIPT_NAME%" (
    echo ERROR: Python script "%PYTHON_SCRIPT_NAME%" not found in this directory:
    echo %SCRIPT_DIR%
    echo Please make sure the Python script is in the same directory as this batch file,
    echo and the PYTHON_SCRIPT_NAME variable in this batch file is set correctly.
    goto :eof
)

REM --- Run the Python script ---
REM The 'python' command assumes Python is in your system's PATH.
echo Launching Coffee Logger...
python "%PYTHON_SCRIPT_NAME%"

REM The Python script itself has an "input('Press Enter to exit...')"
REM so this pause might be redundant if the Python script runs successfully.
REM However, if the Python script fails to start or errors out early,
REM this pause will keep the command window open so you can see the error.
echo.
pause

:eof