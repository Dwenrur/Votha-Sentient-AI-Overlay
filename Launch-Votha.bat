@echo on
setlocal
REM ================== Votha One-Click Launcher ==================
REM Keep this window open so we can see errors
title Votha Launcher

REM 1) Jump to project root
cd /d "%~dp0"

REM 2) Ensure venv exists
if not exist "venv\Scripts\python.exe" (
  echo [SETUP] Creating virtual environment...
  py -3 -m venv venv || goto :fail_python
)

REM 3) Activate venv
call "venv\Scripts\activate.bat" || goto :fail_python

REM 4) Make sure pip works
python -m pip --version || goto :fail_pip

REM 5) Upgrade pip (prints output)
python -m pip install --upgrade pip

REM 6) Install requirements (show output; log to file too)
if exist requirements.txt (
  echo [INFO] Installing packages from requirements.txt ...
  python -m pip install -r requirements.txt -v > install.log 2>&1 || goto :fail_install
) else (
  echo [INFO] No requirements.txt found; installing minimal deps...
  python -m pip install requests sounddevice soundfile websockets simpleaudio -v > install.log 2>&1 || goto :fail_install
)

REM 7) Optional: set audio device (remove if using config\config.json)
if not defined VOTHA_AUDIO_DEVICE set "VOTHA_AUDIO_DEVICE=22"

REM 8) Optional: start Ollama in background
start "" /MIN ollama serve

REM 9) Optional: start overlay HTTP server
REM start "" /MIN cmd /c "python -m http.server 5500"

REM 10) Launch GUI (module path so imports work)
python -m src.app.votha || goto :fail_run

echo.
echo [OK] Votha exited normally.
pause
endlocal
exit /b 0

:fail_python
echo [ERROR] Python 3 not found or venv activation failed.
echo Install Python 3.x and be sure "py" is on PATH.
pause
exit /b 1

:fail_pip
echo [ERROR] pip is not available in this environment.
echo Trying to bootstrap pip...
python -m ensurepip --upgrade || echo [WARN] ensurepip failed.
python -m pip --version || (echo [ERROR] pip still missing.& pause & exit /b 1)
goto :eof

:fail_install
echo [ERROR] Dependency install failed. See install.log for details.
type install.log
pause
exit /b 1

:fail_run
echo [ERROR] Votha failed to start.
echo Check the traceback above. Also check install.log for any missing packages.
pause
exit /b 1
