@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   Starting RAG Project Application
echo ==========================================

REM -------------------------------------------------------
REM Check Python
REM -------------------------------------------------------
call python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed!
    pause
    exit /b
)

REM -------------------------------------------------------
REM Check or create virtual environment
REM -------------------------------------------------------
if not exist ".venv" (
    echo Creating virtual environment...
    call python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

REM -------------------------------------------------------
REM Ensure .env exists (copy from .env.example if missing)
REM -------------------------------------------------------
if not exist ".env" (
    echo .env not found. Copying from .env.example...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo Please edit .env and set your environment variables!
    ) else (
        echo ERROR: .env.example not found!
        pause
        exit /b
    )
)

REM -------------------------------------------------------
REM Ensure requirements.txt exists
REM -------------------------------------------------------
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    pause
    exit /b
)

REM -------------------------------------------------------
REM Install dependencies
REM -------------------------------------------------------
echo Installing dependencies...
call pip install -r requirements.txt

REM -------------------------------------------------------
REM Run the main application
REM -------------------------------------------------------
echo Running RAG Project...
call python -m src.main

echo ==========================================
echo   RAG Project Application Stopped
echo ==========================================
pause