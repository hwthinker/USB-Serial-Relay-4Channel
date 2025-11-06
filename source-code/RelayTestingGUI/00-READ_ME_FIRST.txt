╔═══════════════════════════════════════════════╗
║                                                                ║
║     4-Channel USB Relay Controller - ICSE012A                  ║
║                 Professional GUI Version                       ║
║                                                                ║
║              Created by: HwThinker                             ║
║         Tokopedia.com/hwthinker                                ║
║         shopee.co.id/hwthinker                                 ║
╚══════════════════════════════════════════════╝

📦 PAKET INI BERISI:
═══════════════════════════════════════════════════════════════

✨ APLIKASI:
   relay_control_gui.py          - Source code GUI profesional

🛠️ TOOLS:
   install.bat                   - Install dependencies (Windows)
   build.bat                     - Build executable (Windows)
   build.sh                      - Build executable (Linux)
   requirements.txt              - List library Python

📚 DOKUMENTASI:
   GETTING_STARTED.md           - ⭐ MULAI DI SINI! ⭐
   QUICKSTART.md                - Cara cepat build executable
   README.md                    - Dokumentasi lengkap
   TUTORIAL.md                  - Tutorial step-by-step detail
   PROJECT_STRUCTURE.md         - Struktur project

═══════════════════════════════════════════════════════════════

🚀 CARA TERCEPAT MEMULAI:
═══════════════════════════════════════════════════════════════

OPSI 1: Jika Sudah Ada Executable
──────────────────────────────────
   Double-click: RelayController.exe (Windows)
   atau: ./RelayController (Linux)
   
   ✅ Tidak perlu install Python!
   ✅ Langsung jalan!

OPSI 2: Jalankan dari Source Code
──────────────────────────────────
   Windows:
      1. Double-click: install.bat
      2. Run: python relay_control_gui.py
   
   Linux:
      1. pip3 install -r requirements.txt
      2. python3 relay_control_gui.py

OPSI 3: Build Executable Sendiri
──────────────────────────────────
   Windows:
      Double-click: build.bat
      
   Linux:
      chmod +x build.sh
      ./build.sh
   
   Hasil ada di folder: dist/

═══════════════════════════════════════════════════════════════

📖 BACA DOKUMENTASI:
═══════════════════════════════════════════════════════════════

1. GETTING_STARTED.md  ← Baca ini dulu! (Quick start)
2. QUICKSTART.md       ← Build executable cepat
3. README.md           ← Dokumentasi lengkap
4. TUTORIAL.md         ← Tutorial detail untuk pemula

═══════════════════════════════════════════════════════════════

✨ FITUR UTAMA:
═══════════════════════════════════════════════════════════════

✓ GUI modern dan profesional dengan tkinter
✓ Auto-detect COM ports
✓ Visual indicator untuk setiap relay (LED hijau/abu)
✓ Activity log dengan timestamp
✓ Quick controls: All ON, All OFF, Toggle All
✓ Safety features: auto turn off saat disconnect
✓ Error handling yang comprehensive

═══════════════════════════════════════════════════════════════

⚙️ SPESIFIKASI HARDWARE:
═══════════════════════════════════════════════════════════════

Module      : USB Relay ICSE012A 4-Channel
Interface   : USB Serial (CH340/FTDI)
Baud Rate   : 9600 bps (default)
Voltage     : 5V (USB powered)
Relay Rating: 250VAC/30VDC, 10A Max
Channels    : 4

═══════════════════════════════════════════════════════════════

💻 REQUIREMENTS:
═══════════════════════════════════════════════════════════════

Software (untuk development):
   - Python 3.7 atau lebih baru
   - pyserial library
   - PyInstaller (untuk build executable)

Software (untuk executable):
   - Tidak perlu apapun! File .exe standalone

Hardware:
   - USB Relay Module ICSE012A
   - Kabel USB
   - Port USB tersedia
   - Driver CH340/FTDI (biasanya otomatis)

═══════════════════════════════════════════════════════════════

🆘 TROUBLESHOOTING CEPAT:
═══════════════════════════════════════════════════════════════

❌ COM Port tidak muncul?
   1. Install driver CH340/FTDI
   2. Coba kabel & port USB lain
   3. Restart komputer
   4. Klik tombol Refresh

❌ Error "Access Denied"?
   Windows: Tutup Arduino IDE, PuTTY, dll
   Linux: sudo usermod -a -G dialout $USER

❌ Relay tidak respon?
   1. Cek LED power relay menyala
   2. Pastikan baud rate 9600
   3. Disconnect dan connect ulang

❌ Build error?
   pip install --upgrade pip
   pip install pyinstaller --force-reinstall

Detail troubleshooting ada di README.md

═══════════════════════════════════════════════════════════════

📁 STRUKTUR FILE SETELAH BUILD:
═══════════════════════════════════════════════════════════════

RelayController/
│
├── relay_control_gui.py      (source code)
├── requirements.txt          (dependencies)
├── build.bat / .sh           (build script)
├── install.bat               (installer)
├── [dokumentasi].md          (docs)
│
├── build/                    (temporary - bisa dihapus)
└── dist/
    └── RelayController.exe   ⭐ FILE EXECUTABLE ⭐

═══════════════════════════════════════════════════════════════

Author      : hwthinker
Version     : 1.0.0
Date        : November 2024
Platform    : Windows / Linux

═══════════════════════════════════════════════════════════════

🎯 LANGKAH SELANJUTNYA:
═══════════════════════════════════════════════════════════════

1. ✅ Baca GETTING_STARTED.md
2. ⚙️ Pilih metode yang sesuai (executable/source/build)
3. 🔌 Hubungkan relay module
4. 🚀 Jalankan aplikasi
5. 🎉 Nikmati kontrol relay yang mudah!

═══════════════════════════════════════════════════════════════

💡 TIPS:
═══════════════════════════════════════════════════════════════

- Gunakan executable untuk kemudahan (no Python needed)
- Build sendiri jika ingin modifikasi source code
- Simpan dokumentasi untuk referensi
- Test di device target sebelum deploy
- Buat backup sebelum update

═══════════════════════════════════════════════════════════════

Made with ❤️ from hwthinker
