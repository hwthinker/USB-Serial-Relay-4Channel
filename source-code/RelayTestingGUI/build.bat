@echo off
REM ================================================================
REM Automated Build Script for Relay Controller Executable
REM Author: hwthinker
REM ================================================================

echo.
echo ================================================================
echo    Relay Controller - Automated Build Script
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python dari: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python terdeteksi
python --version
echo.

REM Check if pyserial is installed
echo [INFO] Memeriksa library pyserial...
python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pyserial belum terinstall
    echo [INFO] Menginstall pyserial...
    pip install pyserial
    if errorlevel 1 (
        echo [ERROR] Gagal install pyserial!
        pause
        exit /b 1
    )
    echo [OK] pyserial berhasil diinstall
) else (
    echo [OK] pyserial sudah terinstall
)
echo.

REM Check if PyInstaller is installed
echo [INFO] Memeriksa PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyInstaller belum terinstall
    echo [INFO] Menginstall PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Gagal install PyInstaller!
        pause
        exit /b 1
    )
    echo [OK] PyInstaller berhasil diinstall
) else (
    echo [OK] PyInstaller sudah terinstall
)
echo.

REM Check if source file exists
if not exist "relay_control_gui.py" (
    echo [ERROR] File relay_control_gui.py tidak ditemukan!
    echo Pastikan file source code ada di folder yang sama dengan script ini.
    echo.
    pause
    exit /b 1
)
echo [OK] Source code ditemukan
echo.

REM Clean previous build
echo [INFO] Membersihkan build sebelumnya...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /f /q *.spec
echo [OK] Build folder dibersihkan
echo.

REM Build executable
echo ================================================================
echo    Memulai Proses Build...
echo ================================================================
echo.
echo [INFO] Membuat file executable...
echo [INFO] Ini mungkin memakan waktu 1-2 menit...
echo.

pyinstaller --onefile --windowed --name="RelayController" relay_control_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build gagal!
    echo Periksa error message di atas.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    Build Berhasil!
echo ================================================================
echo.
echo [OK] File executable telah dibuat!
echo [OK] Lokasi: dist\RelayController.exe
echo.

REM Check if executable exists
if exist "dist\RelayController.exe" (
    echo [INFO] Ukuran file:
    dir "dist\RelayController.exe" | find "RelayController.exe"
    echo.
    
    REM Ask to run the executable
    echo Apakah Anda ingin menjalankan aplikasi sekarang?
    set /p run="Ketik Y untuk menjalankan, N untuk skip: "
    
    if /i "%run%"=="Y" (
        echo.
        echo [INFO] Menjalankan RelayController.exe...
        start "" "dist\RelayController.exe"
    )
    
    echo.
    echo [INFO] Buka folder Explorer?
    set /p explorer="Ketik Y untuk membuka folder dist, N untuk skip: "
    
    if /i "%explorer%"=="Y" (
        explorer dist
    )
) else (
    echo [ERROR] File executable tidak ditemukan!
)

echo.
echo ================================================================
echo [INFO] File yang bisa dihapus (optional):
echo   - build\ folder
echo   - *.spec file
echo.
echo [INFO] File yang perlu disimpan:
echo   - dist\RelayController.exe  (untuk distribusi)
echo   - relay_control_gui.py      (source code)
echo ================================================================
echo.
echo Tekan tombol apapun untuk keluar...
pause >nul
