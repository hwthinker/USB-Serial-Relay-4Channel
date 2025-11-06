# 📖 Tutorial Lengkap - Relay Controller
## Panduan Step-by-Step untuk Pemula

---

## 📑 Daftar Isi

1. [Persiapan Hardware](#1-persiapan-hardware)
2. [Install Software](#2-install-software)
3. [Menjalankan dari Source Code](#3-menjalankan-dari-source-code)
4. [Membuat File Executable](#4-membuat-file-executable)
5. [Menggunakan Aplikasi](#5-menggunakan-aplikasi)
6. [Tips & Troubleshooting](#6-tips--troubleshooting)

---

## 1. Persiapan Hardware

### ✅ Yang Anda Butuhkan:

1. **USB Relay Module ICSE012A** (4-Channel)
2. **Kabel USB** (Type-A to Type-B atau Micro USB)
3. **Komputer** (Windows atau Linux)
4. **Perangkat yang akan dikontrol** (lampu, motor, dll)

### 🔌 Koneksi Hardware:

```
┌─────────────────────┐
│                     │
│   Relay Module      │
│     ICSE012A        │
│                     │
│  [1][2][3][4]       │  ← Relay outputs
│                     │
│     [USB Port]      │
└──────────┬──────────┘
           │
           │ USB Cable
           │
           ▼
    ┌──────────────┐
    │   Computer   │
    │              │
    └──────────────┘
```

### ⚠️ Perhatian Keselamatan:

- **MATIKAN DAYA** perangkat sebelum menyambung ke relay
- Jangan melebihi rating relay: **250VAC / 10A**
- Gunakan kabel dengan ukuran yang sesuai
- Pastikan koneksi kuat dan tidak longgar

---

## 2. Install Software

### A. Install Python (Jika Belum Ada)

#### Windows:

1. **Download Python**
   - Kunjungi: https://www.python.org/downloads/
   - Download versi terbaru (3.7 atau lebih baru)

2. **Install Python**
   - Jalankan installer
   - ✅ **PENTING:** Centang **"Add Python to PATH"**
   - Klik "Install Now"
   - Tunggu hingga selesai

3. **Verifikasi Instalasi**
   ```cmd
   python --version
   ```
   Harus muncul versi Python, contoh: `Python 3.11.5`

#### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### B. Install Library yang Diperlukan

Buka **Command Prompt** (Windows) atau **Terminal** (Linux):

```bash
# Install pyserial untuk komunikasi serial
pip install pyserial

# Install PyInstaller untuk membuat executable (optional)
pip install pyinstaller
```

Atau install semua sekaligus dengan:

```bash
pip install -r requirements.txt
```

### C. Install Driver USB (Jika Diperlukan)

**Windows:**
- Windows 10/11 biasanya otomatis detect
- Jika tidak terdeteksi, install driver **CH340** atau **FTDI**
- Download dari website produsen chip

**Linux:**
- Driver biasanya sudah built-in
- Tambahkan user ke grup dialout:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- Logout dan login lagi

---

## 3. Menjalankan dari Source Code

### Step 1: Download Source Code

Download file `relay_control_gui.py` dan simpan di folder yang mudah diakses.

Contoh struktur folder:
```
C:\RelayController\
├── relay_control_gui.py
├── requirements.txt
└── README.md
```

### Step 2: Buka Command Prompt

**Windows:**
- Tekan `Win + R`
- Ketik `cmd`, tekan Enter
- Navigasi ke folder project:
  ```cmd
  cd C:\RelayController
  ```

**Linux:**
- Buka Terminal
- Navigasi ke folder project:
  ```bash
  cd ~/RelayController
  ```

### Step 3: Jalankan Aplikasi

```bash
python relay_control_gui.py
```

**Windows (alternative):**
Double-click file `relay_control_gui.py` jika Python sudah ter-associate dengan `.py` files.

### Step 4: Aplikasi Terbuka

Jika berhasil, window aplikasi akan muncul!

---

## 4. Membuat File Executable

### Metode A: Menggunakan Script Otomatis (MUDAH)

#### Windows:

1. Double-click file `build.bat`
2. Script akan otomatis:
   - Cek Python
   - Install library yang diperlukan
   - Build executable
3. Tunggu hingga selesai
4. File `.exe` akan ada di folder `dist\`

#### Linux:

1. Buat script executable:
   ```bash
   chmod +x build.sh
   ```
2. Jalankan:
   ```bash
   ./build.sh
   ```
3. File executable akan ada di folder `dist/`

### Metode B: Manual Build

#### Step 1: Pastikan PyInstaller Terinstall

```bash
pip install pyinstaller
```

#### Step 2: Build Executable

**Untuk Single File (Recommended):**

```bash
pyinstaller --onefile --windowed --name="RelayController" relay_control_gui.py
```

Parameter:
- `--onefile` = Satu file saja
- `--windowed` = Tanpa console window
- `--name` = Nama aplikasi

**Dengan Custom Icon:**

```bash
pyinstaller --onefile --windowed --name="RelayController" --icon=icon.ico relay_control_gui.py
```

#### Step 3: Tunggu Proses Build

Proses build memakan waktu 1-2 menit. Anda akan melihat banyak output di terminal.

```
Building EXE from EXE-00.toc completed successfully.
```

Jika muncul pesan di atas, build **BERHASIL**!

#### Step 4: Cek Hasil

File executable ada di:
```
dist/RelayController.exe    (Windows)
dist/RelayController        (Linux)
```

#### Step 5: Test Executable

Double-click file tersebut. Aplikasi harus langsung jalan!

---

## 5. Menggunakan Aplikasi

### 🚀 Langkah Penggunaan:

#### Step 1: Hubungkan Relay Module

1. Colokkan kabel USB dari relay module ke komputer
2. Tunggu hingga driver terinstall (Windows)
3. LED power di relay module akan menyala

#### Step 2: Buka Aplikasi

- Jalankan `RelayController.exe` atau
- Jalankan `python relay_control_gui.py`

#### Step 3: Connection Settings

1. **Pilih COM Port**
   - Klik dropdown "COM Port"
   - Pilih port yang sesuai (contoh: COM3, COM4)
   - Jika tidak muncul, klik 🔄 **Refresh**

2. **Pilih Baud Rate**
   - Biarkan default: **9600**
   - Kecuali modul Anda menggunakan baud rate lain

3. **Klik "Connect"**
   - Status akan berubah menjadi **● Connected** (hijau)
   - Log akan menampilkan "Successfully connected"

#### Step 4: Kontrol Relay

**Kontrol Individual:**
1. Klik tombol **ON** di bawah relay yang diinginkan
2. LED indicator akan berubah **HIJAU**
3. Relay akan klik dan menyambung
4. Klik lagi untuk mematikan (LED menjadi **ABU-ABU**)

**Quick Controls:**
- **All ON** = Menyalakan semua relay
- **All OFF** = Mematikan semua relay  
- **Toggle All** = Membalik status (ON→OFF, OFF→ON)

#### Step 5: Monitoring

Perhatikan **Activity Log** di bagian bawah:
```
[10:23:15] [INFO] Successfully connected to COM3
[10:23:20] [INFO] Relay 1 turned ON
[10:23:22] [INFO] Relay 2 turned ON
[10:23:30] [INFO] All relays turned OFF
```

#### Step 6: Disconnect

1. Klik tombol **Disconnect**
2. Semua relay akan otomatis mati
3. Status menjadi **● Disconnected** (merah)

#### Step 7: Tutup Aplikasi

- Klik **X** di pojok kanan atas
- Jika masih connected, akan muncul konfirmasi
- Klik **OK** untuk disconnect dan keluar

---

## 6. Tips & Troubleshooting

### 💡 Tips Penggunaan:

#### 1. **Cari COM Port yang Benar**

**Windows:**
1. Buka **Device Manager**
2. Expand "Ports (COM & LPT)"
3. Cari "USB Serial Port (COMx)"
4. Catat nomor COM-nya

**Linux:**
```bash
# List semua serial port
ls /dev/ttyUSB* /dev/ttyACM*

# Atau gunakan dmesg
dmesg | grep tty
```

#### 2. **Test Koneksi Serial**

Sebelum menggunakan aplikasi, test dulu dengan serial terminal:

**Windows:** PuTTY, Tera Term  
**Linux:** minicom, screen

```bash
# Linux
screen /dev/ttyUSB0 9600
```

#### 3. **Sequencing Relay**

Untuk kontrol berurutan:
1. All OFF
2. Nyalakan Relay 1 → tunggu
3. Nyalakan Relay 2 → tunggu
4. Dan seterusnya

#### 4. **Multiple Relay Modules**

Jika punya lebih dari satu module:
- Setiap module akan muncul sebagai COM port berbeda
- Bisa jalankan multiple instance aplikasi
- Tiap instance connect ke COM berbeda

### 🔧 Troubleshooting:

#### ❌ Problem: "COM Port tidak muncul"

**Solusi:**
1. Cek kabel USB (coba kabel lain)
2. Coba port USB lain di komputer
3. Install driver CH340/FTDI
4. Restart komputer
5. Klik 🔄 Refresh di aplikasi

#### ❌ Problem: "Access Denied / Permission Denied"

**Windows:**
```
Tutup aplikasi lain yang menggunakan COM port:
- Arduino IDE
- PuTTY
- Serial Monitor lainnya
```

**Linux:**
```bash
# Tambahkan user ke grup dialout
sudo usermod -a -G dialout $USER

# Logout dan login lagi, atau:
newgrp dialout

# Cek permission
ls -l /dev/ttyUSB0
```

#### ❌ Problem: "Relay tidak merespon"

**Checklist:**
- [ ] LED power relay menyala?
- [ ] Kabel USB terpasang dengan baik?
- [ ] Baud rate benar (9600)?
- [ ] Aplikasi lain tidak menggunakan port?
- [ ] Coba disconnect dan connect ulang

**Test Manual:**
```bash
# Linux - kirim command manual
echo -ne '\x50\x51\x01\x00\x0E' > /dev/ttyUSB0
```

#### ❌ Problem: "Executable tidak jalan"

**Windows:**
```
1. Klik kanan file .exe
2. Pilih "Properties"
3. Tab "Compatibility"
4. Centang "Run as administrator"
5. Coba lagi
```

**Antivirus Issue:**
- Antivirus mungkin block file
- Add exception untuk file tersebut
- Atau disable antivirus sementara untuk test

**Missing DLL:**
- Install Visual C++ Redistributable
- Download dari Microsoft website

#### ❌ Problem: "Build Error - ModuleNotFoundError"

```bash
# Uninstall dan install ulang
pip uninstall pyserial
pip install pyserial

# Pastikan PyInstaller up to date
pip install --upgrade pyinstaller

# Clean build
rmdir /s /q build dist
del *.spec
pyinstaller --onefile --windowed relay_control_gui.py
```

### 📊 Performance Tips:

#### Mengurangi Ukuran Executable:

```bash
pyinstaller --onefile --windowed ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    relay_control_gui.py
```

#### Optimasi Startup Time:

Untuk build yang lebih cepat loading (tapi lebih banyak file):

```bash
pyinstaller --windowed relay_control_gui.py
```

Hasilnya di `dist/RelayController/` folder.

---

## 📸 Screenshot Reference

### 1. Main Window - Disconnected
```
┌────────────────────────────────────────┐
│ 4-Channel USB Relay Controller         │
│ ICSE012A Series - HwThinker                 │
├────────────────────────────────────────┤
│ Connection Settings                    │
│ COM Port: [COM3        ▼] [🔄 Refresh]│
│ Baud Rate: [9600       ▼]             │
│ [Connect] [Disconnect] ● Disconnected  │
├────────────────────────────────────────┤
│ Relay Controls                         │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│ │Relay1│ │Relay2│ │Relay3│ │Relay4│  │
│ │  ○   │ │  ○   │ │  ○   │ │  ○   │  │
│ │ [ON] │ │ [ON] │ │ [ON] │ │ [ON] │  │
│ └──────┘ └──────┘ └──────┘ └──────┘  │
│ [All ON] [All OFF] [Toggle All]       │
├────────────────────────────────────────┤
│ Activity Log                           │
│ [10:23:15] [INFO] Application started │
└────────────────────────────────────────┘
```

### 2. Main Window - Connected with Relays ON
```
┌────────────────────────────────────────┐
│ 4-Channel USB Relay Controller         │
│ ICSE012A Series - HwThinker                 │
├────────────────────────────────────────┤
│ Connection Settings                    │
│ COM Port: [COM3        ▼] [🔄 Refresh]│
│ Baud Rate: [9600       ▼]             │
│ [Connect] [Disconnect] ● Connected     │
├────────────────────────────────────────┤
│ Relay Controls                         │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│ │Relay1│ │Relay2│ │Relay3│ │Relay4│  │
│ │  ●   │ │  ●   │ │  ○   │ │  ○   │  │
│ │ [ON] │ │ [ON] │ │ [ON] │ │ [ON] │  │
│ └──────┘ └──────┘ └──────┘ └──────┘  │
│ [All ON] [All OFF] [Toggle All]       │
├────────────────────────────────────────┤
│ Activity Log                           │
│ [10:23:15] [SUCCESS] Connected COM3   │
│ [10:23:20] [INFO] Relay 1 turned ON   │
│ [10:23:22] [INFO] Relay 2 turned ON   │
└────────────────────────────────────────┘
```

---

## 🎓 Latihan Praktis

### Latihan 1: Kontrol Sequential

**Tujuan:** Menyalakan relay satu per satu dengan delay

**Langkah:**
1. Connect ke relay module
2. All OFF dulu
3. Nyalakan Relay 1, tunggu 2 detik
4. Nyalakan Relay 2, tunggu 2 detik
5. Nyalakan Relay 3, tunggu 2 detik
6. Nyalakan Relay 4, tunggu 2 detik
7. All OFF

### Latihan 2: Toggle Pattern

**Tujuan:** Membuat pattern nyala relay

**Pattern A (Alternate):**
- Relay 1 & 3 ON, Relay 2 & 4 OFF
- Tunggu 1 detik
- Relay 1 & 3 OFF, Relay 2 & 4 ON
- Ulangi

**Pattern B (Chase):**
- Only Relay 1 ON → delay
- Only Relay 2 ON → delay
- Only Relay 3 ON → delay
- Only Relay 4 ON → delay
- Ulangi

### Latihan 3: Kontrol Lampu Rumah

**Scenario:** Kontrol 4 lampu di rumah

**Setup:**
- Relay 1 → Lampu Ruang Tamu
- Relay 2 → Lampu Kamar
- Relay 3 → Lampu Dapur
- Relay 4 → Lampu Teras

**Test:**
1. Simulasi pagi hari: Semua OFF
2. Simulasi sore hari: Teras ON
3. Simulasi malam: Semua ON kecuali Kamar
4. Simulasi tidur: Semua OFF

---

## 📚 Referensi Tambahan

### Links:
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Python Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)

### Command Reference:

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Install specific version
pip install pyserial==3.5

# Upgrade package
pip install --upgrade pyserial

# Uninstall package
pip uninstall pyserial
```

---

**🎉 Selamat! Anda sudah menguasai Relay Controller!**

Jika ada pertanyaan atau masalah, silakan:
- Baca bagian Troubleshooting
- Check Activity Log untuk error messages
- Hubungi support atau maintainer

---

**Made with ❤️ by hwthinker**  
**Version:** 1.0.0  
**Last Updated:** November 2025
