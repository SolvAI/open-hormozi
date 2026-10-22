@echo off
REM OpenHormozi launcher for Windows: double-click this file.
REM Installs uv (which brings its own Python) on first run, then starts the app.
setlocal
cd /d "%~dp0"
title OpenHormozi
set "PYTHONUTF8=1"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

where uv >nul 2>nul
if errorlevel 1 (
  echo Installing uv, the Python package manager ^(one time, about 30 MB^)...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
)

where uv >nul 2>nul
if errorlevel 1 (
  echo.
  echo uv could not be installed. Install it from https://docs.astral.sh/uv/ and run start.bat again.
  pause
  exit /b 1
)

uv run --frozen python -m app %*
if errorlevel 1 (
  echo.
  echo OpenHormozi stopped with an error. The messages above say why.
  pause
)
endlocal
