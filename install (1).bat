@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║         💰 NOOR EXPENSE TRACKER — Windows Installer             ║
REM ║              Developed by Noor Hoorain                           ║
REM ║          github.com/noorhoorain44-ship-it                        ║
REM ╚══════════════════════════════════════════════════════════════════╝

setlocal EnableDelayedExpansion
title Noor Expense Tracker - Windows Installer
color 0B

echo.
echo   ╔════════════════════════════════════════════════════╗
echo   ║   💰  NOOR EXPENSE TRACKER  INSTALLER (Windows)   ║
echo   ║   Developed by Noor Hoorain                        ║
echo   ║   github.com/noorhoorain44-ship-it                  ║
echo   ╚════════════════════════════════════════════════════╝
echo.

REM ─── Set paths ────────────────────────────────────────────────────
set "APP_DIR=%USERPROFILE%\NoorExpenseTracker"
set "VENV_DIR=%APP_DIR%\venv"
set "SCRIPTS_DIR=%APP_DIR%\scripts"
set "SCRIPT_SRC=%~dp0expensetracker.py"

REM ─── 1. Python check ──────────────────────────────────────────────
echo   [INFO]  Checking for Python 3.8+ ...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo   [ERROR] Python not found!
        echo.
        echo   Please install Python 3.8+ from https://www.python.org/downloads/
        echo   Make sure to check "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)

for /f "tokens=*" %%v in ('%PYTHON_CMD% --version 2^>^&1') do set PY_VER=%%v
echo   [OK]    Found: %PY_VER%

REM ─── 2. pip check ─────────────────────────────────────────────────
echo   [INFO]  Checking pip ...
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [WARN]  pip not found. Attempting to install ...
    %PYTHON_CMD% -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo   [ERROR] Could not install pip. Please install manually.
        pause
        exit /b 1
    )
)
echo   [OK]    pip is available

REM ─── 3. Create directories ────────────────────────────────────────
echo   [INFO]  Creating application directories ...
if not exist "%APP_DIR%"     mkdir "%APP_DIR%"
if not exist "%SCRIPTS_DIR%" mkdir "%SCRIPTS_DIR%"
echo   [OK]    Directories created: %APP_DIR%

REM ─── 4. Virtual environment ───────────────────────────────────────
echo   [INFO]  Creating virtual environment ...
%PYTHON_CMD% -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo   [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo   [OK]    Virtual environment ready: %VENV_DIR%

REM ─── 5. Install dependencies ──────────────────────────────────────
echo   [INFO]  Installing dependencies ...
call "%VENV_DIR%\Scripts\activate.bat"
pip install --upgrade pip --quiet
pip install colorama rich --quiet
if %errorlevel% neq 0 (
    echo   [WARN]  Some packages may not have installed correctly.
    echo          The app will still work without them (plain text mode).
) else (
    echo   [OK]    colorama and rich installed successfully
)

REM ─── 6. Copy script ───────────────────────────────────────────────
echo   [INFO]  Installing expensetracker.py ...
if not exist "%SCRIPT_SRC%" (
    echo   [ERROR] expensetracker.py not found next to install.bat
    pause
    exit /b 1
)
copy /Y "%SCRIPT_SRC%" "%APP_DIR%\expensetracker.py" >nul
echo   [OK]    Script copied to %APP_DIR%

REM ─── 7. Create launcher batch file ───────────────────────────────
echo   [INFO]  Creating launcher ...
(
    echo @echo off
    echo title Noor Expense Tracker
    echo color 0B
    echo call "%VENV_DIR%\Scripts\activate.bat"
    echo python "%APP_DIR%\expensetracker.py" %%*
    echo pause
) > "%SCRIPTS_DIR%\expense.bat"
echo   [OK]    Launcher created: %SCRIPTS_DIR%\expense.bat

REM ─── 8. Create Desktop shortcut ───────────────────────────────────
echo   [INFO]  Creating desktop shortcut ...
set "SHORTCUT=%USERPROFILE%\Desktop\Noor Expense Tracker.lnk"
set "VBS_TMP=%TEMP%\create_shortcut.vbs"
(
    echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
    echo sLinkFile = "%SHORTCUT%"
    echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
    echo oLink.TargetPath = "%SCRIPTS_DIR%\expense.bat"
    echo oLink.WorkingDirectory = "%APP_DIR%"
    echo oLink.Description = "Noor Expense Tracker"
    echo oLink.Save
) > "%VBS_TMP%"
cscript //nologo "%VBS_TMP%"
del "%VBS_TMP%" >nul 2>&1
echo   [OK]    Desktop shortcut created

REM ─── 9. Add to PATH ───────────────────────────────────────────────
echo   [INFO]  Adding to user PATH ...
powershell -Command "[System.Environment]::SetEnvironmentVariable('Path', [System.Environment]::GetEnvironmentVariable('Path','User') + ';%SCRIPTS_DIR%', 'User')" >nul 2>&1
echo   [OK]    %SCRIPTS_DIR% added to user PATH

REM ─── Done ─────────────────────────────────────────────────────────
echo.
echo   ════════════════════════════════════════════════════
echo   ✅  Installation complete!
echo   ════════════════════════════════════════════════════
echo.
echo   ▶  Double-click "Noor Expense Tracker" on your Desktop
echo   ▶  Or open a new CMD/PowerShell and type:  expense
echo   ▶  Or run directly:  python %APP_DIR%\expensetracker.py
echo.
echo   Developed by Noor Hoorain — github.com/noorhoorain44-ship-it
echo.
pause
endlocal
