@echo off
title AI Real-Time GYM Coach
echo =======================================================
echo          AI Real-time GYM Coach - Quick Launcher
echo =======================================================
echo.

REM 1. Check local venv
if exist "venv\Scripts\streamlit.exe" (
    echo [INFO] Found local virtual environment in .\venv
    echo [INFO] Launching Streamlit...
    echo.
    venv\Scripts\streamlit.exe run main.py
    goto end
)

REM 2. Check pre-configured workspace venv
if exist "..\AI\ai-gym-coach\venv\Scripts\streamlit.exe" (
    echo [INFO] Found pre-configured virtual environment in ..\AI\ai-gym-coach\venv
    echo [INFO] Launching Streamlit...
    echo.
    ..\AI\ai-gym-coach\venv\Scripts\streamlit.exe run main.py
    goto end
)

REM 3. Check system-wide streamlit
where streamlit >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [INFO] Using system-installed Streamlit...
    echo.
    streamlit run main.py
    goto end
)

echo [ERROR] Streamlit not found!
echo Please set up a virtual environment:
echo   1. python -m venv venv
echo   2. .\venv\Scripts\activate
echo   3. pip install -r requirements.txt
echo   4. streamlit run main.py
echo.
pause

:end
