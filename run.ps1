Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         AI Real-time GYM Coach - Quick Launcher       " -ForegroundColor Yellow
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".\venv\Scripts\streamlit.exe") {
    Write-Host "[INFO] Using local virtual environment (.\venv)..." -ForegroundColor Green
    & ".\venv\Scripts\streamlit.exe" run main.py
    exit
}

if (Test-Path "..\AI\ai-gym-coach\venv\Scripts\streamlit.exe") {
    Write-Host "[INFO] Using pre-configured virtual environment (..\AI\ai-gym-coach\venv)..." -ForegroundColor Green
    & "..\AI\ai-gym-coach\venv\Scripts\streamlit.exe" run main.py
    exit
}

if (Get-Command "streamlit" -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Using system Streamlit..." -ForegroundColor Green
    streamlit run main.py
    exit
}

Write-Host "[ERROR] Streamlit executable not found!" -ForegroundColor Red
Write-Host "Setup instructions:" -ForegroundColor Yellow
Write-Host "  1. python -m venv venv"
Write-Host "  2. .\venv\Scripts\activate"
Write-Host "  3. pip install -r requirements.txt"
Write-Host "  4. streamlit run main.py"
Write-Host ""
pause
