#!/bin/bash

# ================================================================
# Automated Build Script for Relay Controller Executable
# Author: HwThinker
# Platform: Linux
# ================================================================

echo ""
echo "================================================================"
echo "   Relay Controller - Automated Build Script (Linux)"
echo "================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${BLUE}[INFO]${NC} Memeriksa Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python3 tidak ditemukan!"
    echo "Silakan install Python3:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python terdeteksi"
python3 --version
echo ""

# Check if pip is installed
echo -e "${BLUE}[INFO]${NC} Memeriksa pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} pip3 tidak ditemukan"
    echo -e "${BLUE}[INFO]${NC} Menginstall pip..."
    sudo apt-get install python3-pip -y || sudo dnf install python3-pip -y || sudo pacman -S python-pip
fi
echo -e "${GREEN}[OK]${NC} pip tersedia"
echo ""

# Check if pyserial is installed
echo -e "${BLUE}[INFO]${NC} Memeriksa library pyserial..."
if ! python3 -c "import serial" &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} pyserial belum terinstall"
    echo -e "${BLUE}[INFO]${NC} Menginstall pyserial..."
    pip3 install pyserial --user
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Gagal install pyserial!"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} pyserial berhasil diinstall"
else
    echo -e "${GREEN}[OK]${NC} pyserial sudah terinstall"
fi
echo ""

# Check if PyInstaller is installed
echo -e "${BLUE}[INFO]${NC} Memeriksa PyInstaller..."
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} PyInstaller belum terinstall"
    echo -e "${BLUE}[INFO]${NC} Menginstall PyInstaller..."
    pip3 install pyinstaller --user
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Gagal install PyInstaller!"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} PyInstaller berhasil diinstall"
else
    echo -e "${GREEN}[OK]${NC} PyInstaller sudah terinstall"
fi
echo ""

# Check if source file exists
if [ ! -f "relay_control_gui.py" ]; then
    echo -e "${RED}[ERROR]${NC} File relay_control_gui.py tidak ditemukan!"
    echo "Pastikan file source code ada di folder yang sama dengan script ini."
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Source code ditemukan"
echo ""

# Clean previous build
echo -e "${BLUE}[INFO]${NC} Membersihkan build sebelumnya..."
rm -rf build dist *.spec
echo -e "${GREEN}[OK]${NC} Build folder dibersihkan"
echo ""

# Build executable
echo "================================================================"
echo "   Memulai Proses Build..."
echo "================================================================"
echo ""
echo -e "${BLUE}[INFO]${NC} Membuat file executable..."
echo -e "${BLUE}[INFO]${NC} Ini mungkin memakan waktu 1-2 menit..."
echo ""

# Use python3 -m PyInstaller for better compatibility
python3 -m PyInstaller --onefile --windowed --name="RelayController" relay_control_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Build gagal!"
    echo "Periksa error message di atas."
    exit 1
fi

echo ""
echo "================================================================"
echo "   Build Berhasil!"
echo "================================================================"
echo ""
echo -e "${GREEN}[OK]${NC} File executable telah dibuat!"
echo -e "${GREEN}[OK]${NC} Lokasi: dist/RelayController"
echo ""

# Check if executable exists
if [ -f "dist/RelayController" ]; then
    # Make it executable
    chmod +x dist/RelayController
    
    echo -e "${BLUE}[INFO]${NC} Ukuran file:"
    ls -lh dist/RelayController | awk '{print $5, $9}'
    echo ""
    
    # Ask to run the executable
    read -p "Apakah Anda ingin menjalankan aplikasi sekarang? (Y/n): " run
    
    if [ "$run" = "Y" ] || [ "$run" = "y" ] || [ -z "$run" ]; then
        echo ""
        echo -e "${BLUE}[INFO]${NC} Menjalankan RelayController..."
        ./dist/RelayController &
    fi
    
    echo ""
    read -p "Buka folder dengan file manager? (Y/n): " explorer
    
    if [ "$explorer" = "Y" ] || [ "$explorer" = "y" ] || [ -z "$explorer" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open dist
        elif command -v nautilus &> /dev/null; then
            nautilus dist &
        elif command -v dolphin &> /dev/null; then
            dolphin dist &
        fi
    fi
else
    echo -e "${RED}[ERROR]${NC} File executable tidak ditemukan!"
    exit 1
fi

echo ""
echo "================================================================"
echo -e "${BLUE}[INFO]${NC} File yang bisa dihapus (optional):"
echo "  - build/ folder"
echo "  - *.spec file"
echo ""
echo -e "${BLUE}[INFO]${NC} File yang perlu disimpan:"
echo "  - dist/RelayController  (untuk distribusi)"
echo "  - relay_control_gui.py  (source code)"
echo ""
echo -e "${YELLOW}[NOTE]${NC} Untuk menjalankan di Linux lain, user perlu:"
echo "  1. sudo usermod -a -G dialout \$USER"
echo "  2. Logout dan login lagi"
echo "  3. chmod +x RelayController"
echo "================================================================"
echo ""
echo "Selesai!"
