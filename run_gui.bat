@echo off
setlocal
set "APP_DIR=%~dp0"
"%APP_DIR%\.venv\Scripts\python.exe" "%APP_DIR%run_gui.py" %*
endlocal
