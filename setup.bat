@echo off
REM setup.bat - First-time setup for Windows users
REM Run this file by double-clicking it or running it in Command Prompt
REM Do NOT use PowerShell - use Command Prompt (cmd.exe)

echo.
echo Player Care AI - Windows Setup
echo ================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in your PATH.
    echo.
    echo Please install Python 3.10 or higher from: https://www.python.org/downloads/
    echo During installation, check the box that says "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Found Python %PYVER%

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)
echo Virtual environment created.

REM Install dependencies
echo.
echo Installing dependencies (this may take 2-5 minutes)...
echo Note: sentence-transformers will download an 80MB model on first use. This is normal.
venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    echo Try running: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
echo Dependencies installed.

REM Copy .env.example if .env does not exist
if not exist .env (
    copy .env.example .env
    echo.
    echo .env file created from .env.example
    echo IMPORTANT: Open .env in a text editor and fill in your API keys before continuing.
) else (
    echo .env already exists - skipping.
)

echo.
echo ================================================
echo Setup complete!
echo.
echo NEXT STEPS:
echo.
echo 1. Open .env in Notepad and add your ANTHROPIC_API_KEY
echo    Get your key at: https://console.anthropic.com
echo.
echo 2. Activate the virtual environment:
echo    Run: venv\Scripts\activate
echo    Your prompt will change to show (venv)
echo.
echo 3. Sync the knowledge base:
echo    Run: python rag\kb_sync.py
echo    Note: First run downloads ~80MB model. May take 1-2 minutes. Do not close.
echo.
echo 4. Run the example:
echo    Run: python example_run.py
echo.
echo IMPORTANT: You must run venv\Scripts\activate every time you open a new
echo Command Prompt window before running any python commands.
echo ================================================
echo.
pause
