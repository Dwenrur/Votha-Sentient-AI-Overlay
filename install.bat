@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ===============================
echo Votha + Piper setup (Windows)
echo ===============================

REM 1. figure out project dir (where this bat lives)
set SCRIPT_DIR=%~dp0
echo Project dir: %SCRIPT_DIR%

REM 2. check python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.x from https://www.python.org/ and run this again.
    goto :end
) else (
    echo [OK] Python found.
)

REM 3. optional: create venv
if not exist "%SCRIPT_DIR%venv" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%venv"
) else (
    echo venv already exists.
@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ===============================
echo Votha + Piper setup (Windows)
echo ===============================

REM 1. figure out project dir (where this bat lives)
set SCRIPT_DIR=%~dp0
echo Project dir: %SCRIPT_DIR%

REM 2. check python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.x from https://www.python.org/ and run this again.
    goto :end
) else (
    echo [OK] Python found.
)

REM 3. create venv if missing
if not exist "%SCRIPT_DIR%venv" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%venv"
) else (
    echo [OK] venv already exists.
)

REM 4. activate venv
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

REM 5. ensure requirements.txt exists
if not exist "%SCRIPT_DIR%requirements.txt" (
    echo simpleaudio> "%SCRIPT_DIR%requirements.txt"
)

echo Installing Python packages...
pip install --upgrade pip
pip install -r "%SCRIPT_DIR%requirements.txt"

REM 6. check piper.exe
if not exist "%SCRIPT_DIR%piper\piper.exe" (
    echo [WARN] piper.exe not found at:
    echo        %SCRIPT_DIR%piper\piper.exe
    echo Create the folder and drop piper.exe there.
) else (
    echo [OK] Found piper.exe
)

REM 7. check voices folder
if not exist "%SCRIPT_DIR%piper\voices" (
    echo [WARN] voices folder not found, creating...
    mkdir "%SCRIPT_DIR%piper\voices"
) else (
    echo [OK] voices folder exists.
)

REM 7a. optionally check for our default voice
if not exist "%SCRIPT_DIR%piper\voices\en_US-norman-medium.onnx" (
    echo [WARN] Voice model en_US-norman-medium.onnx not found in piper\voices
)
if not exist "%SCRIPT_DIR%piper\voices\en_US-norman-medium.onnx.json" (
    echo [WARN] Voice config en_US-norman-medium.onnx.json not found in piper\voices
)

REM 8. check for bundled ffmpeg
if exist "%SCRIPT_DIR%ffmpeg\bin\ffplay.exe" (
    echo [OK] Found bundled FFmpeg at ffmpeg\bin\ffplay.exe
) else (
    echo [WARN] ffplay.exe not found in ffmpeg\bin\
    echo        You can bundle FFmpeg here:
    echo        %SCRIPT_DIR%ffmpeg\bin\ffplay.exe
    echo        or install FFmpeg globally from:
    echo        https://www.gyan.dev/ffmpeg/builds/
)

echo.
echo To test speaking, run:
echo     .\venv\Scripts\python.exe test_voice.py
echo To start the AI voice, run:
echo     .\venv\Scripts\python.exe votha.py
echo.

:end
echo Done.
endlocal
