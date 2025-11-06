@echo off
REM ================================================================
REM Quick Install Script - Relay Controller Dependencies
REM Author: HwThinker
REM ================================================================

echo.
echo ================================================================
echo    Relay Controller - Dependency Installer
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Silakan install Python terlebih dahulu:
    echo 1. Download dari: https://www.python.org/downloads/
    echo 2. Jalankan installer
    echo 3. CENTANG "Add Python to PATH"
    echo 4. Jalankan script ini lagi
    echo.
    pause
    exit /b 1
)

echo [OK] Python terdeteksi
python --version
echo.

REM Upgrade pip
echo [INFO] Mengupgrade pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [INFO] Menginstall dependencies...
echo.

if exist "requirements.txt" (
    echo [INFO] Menggunakan requirements.txt...
    pip install -r requirements.txt
) else (
    echo [INFO] Install manual...
    pip install pyserial
    pip install pyinstaller
)

if errorlevel 1 (
    echo.
    echo [ERROR] Instalasi gagal!
    echo Coba jalankan Command Prompt sebagai Administrator.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    Instalasi Selesai!
echo ================================================================
echo.
echo [OK] Semua dependencies sudah terinstall
echo.
echo Langkah selanjutnya:
echo 1. Jalankan aplikasi: python relay_control_gui.py
echo 2. Atau build executable: build.bat
echo.
pause
