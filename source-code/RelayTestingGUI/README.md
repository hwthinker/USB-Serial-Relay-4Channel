# 4-Channel USB Relay Controller - ICSE012A

Aplikasi GUI profesional untuk mengontrol USB Relay Module 4-Channel ICSE012A Series menggunakan Python.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)

## 📋 Daftar Isi

- [Fitur](#fitur)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Membuat File Executable](#membuat-file-executable)
- [Troubleshooting](#troubleshooting)
- [Spesifikasi Hardware](#spesifikasi-hardware)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## ✨ Fitur

- **GUI Modern & Intuitif** - Interface yang mudah digunakan dengan visual feedback
- **Auto-Detect COM Port** - Otomatis mendeteksi port USB yang tersedia
- **Visual Indicators** - LED indicator untuk status setiap relay (ON/OFF)
- **Activity Logging** - Real-time log dengan timestamp untuk monitoring
- **Quick Controls** - Tombol cepat untuk All ON, All OFF, dan Toggle All
- **Safety Features** - Auto turn off relay saat disconnect
- **Error Handling** - Penanganan error yang comprehensive

## 💻 Persyaratan Sistem

### Hardware
- Windows 7/8/10/11 atau Linux (Ubuntu, Debian, dll)
- USB Port tersedia
- USB Relay Module ICSE012A 4-Channel
- RAM minimal 512 MB
- Storage minimal 50 MB

### Software
- Python 3.7 atau lebih baru (untuk development)
- Driver USB-to-Serial (biasanya sudah built-in di Windows 10/11)

## 📦 Instalasi

### Metode 1: Menjalankan dari Source Code

1. **Install Python**
   
   Download Python dari [python.org](https://www.python.org/downloads/)
   
   Pastikan centang "Add Python to PATH" saat instalasi!

2. **Install Dependencies**
   
   Buka Command Prompt atau Terminal, lalu jalankan:
   
   ```bash
   pip install pyserial
   ```

3. **Download Source Code**
   
   Download file `relay_control_gui.py` ke folder yang diinginkan

4. **Jalankan Aplikasi**
   
   ```bash
   python relay_control_gui.py
   ```

### Metode 2: Menggunakan File Executable (.exe)

**Untuk pengguna yang tidak ingin install Python!**

1. Download file `RelayController.exe` dari folder `dist/`
2. Double-click file tersebut untuk menjalankan
3. Tidak perlu install Python atau library apapun!

## 🎯 Cara Penggunaan

### 1. Koneksi ke Device

1. **Hubungkan USB Relay Module** ke komputer
2. **Buka aplikasi** Relay Controller
3. **Pilih COM Port** dari dropdown (contoh: COM3, COM4)
4. **Pilih Baud Rate** (default: 9600)
5. **Klik tombol "Connect"**
6. Tunggu hingga status berubah menjadi **● Connected** (hijau)

![Connection Screenshot](docs/images/connection.png)

### 2. Mengontrol Relay

#### Kontrol Individual
- Klik tombol **ON** di bawah relay yang ingin diaktifkan
- LED indicator akan berubah menjadi **hijau** saat relay ON
- Klik lagi untuk mematikan (LED menjadi **abu-abu**)

#### Quick Controls
- **All ON** - Menyalakan semua relay sekaligus
- **All OFF** - Mematikan semua relay sekaligus
- **Toggle All** - Membalik status semua relay (ON→OFF, OFF→ON)

### 3. Monitoring

- Perhatikan **Activity Log** di bagian bawah
- Log menampilkan semua aktivitas dengan timestamp
- Level log: INFO, SUCCESS, ERROR, WARNING

### 4. Disconnect

1. Klik tombol **Disconnect**
2. Semua relay akan otomatis mati
3. Aplikasi siap untuk reconnect atau ditutup

### 5. Menutup Aplikasi

- Klik tombol **X** di pojok kanan atas
- Jika masih terkoneksi, akan muncul konfirmasi
- Klik **OK** untuk disconnect dan keluar

## 🔧 Membuat File Executable

Ikuti langkah-langkah berikut untuk membuat file `.exe` yang bisa dijalankan tanpa Python:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Buat File Executable

#### Opsi A: Single File (Recommended)

**File tunggal, mudah didistribusikan:**

```bash
pyinstaller --onefile --windowed --name="RelayController" --icon=icon.ico relay_control_gui.py
```

Parameter:
- `--onefile` : Membuat satu file exe saja
- `--windowed` : Tidak menampilkan console window
- `--name` : Nama file executable
- `--icon` : Icon aplikasi (opsional)

#### Opsi B: Multiple Files

**Lebih cepat loading, tapi banyak file:**

```bash
pyinstaller --windowed --name="RelayController" relay_control_gui.py
```

### Step 3: Hasil Executable

Setelah proses selesai, file executable akan berada di:

```
dist/
└── RelayController.exe  (untuk --onefile)

atau

dist/
└── RelayController/
    ├── RelayController.exe
    └── (file-file dependency lainnya)
```

### Step 4: Testing

1. Buka folder `dist/`
2. Double-click `RelayController.exe`
3. Aplikasi harus langsung jalan tanpa install Python!

### Step 5: Distribusi

**Untuk single file:**
- Copy `RelayController.exe` ke komputer lain
- Langsung bisa dijalankan!

**Untuk multiple files:**
- Copy seluruh folder `RelayController` dari dalam `dist/`
- Jalankan `RelayController.exe` di dalam folder tersebut

## 🎨 Membuat Custom Icon (Opsional)

1. **Buat atau download icon** format `.ico` (ukuran 256x256 pixel)
2. **Simpan** dengan nama `icon.ico` di folder yang sama dengan script
3. **Tambahkan parameter** `--icon=icon.ico` saat build

Contoh membuat icon dari gambar PNG menggunakan Python:

```python
from PIL import Image

# Buka gambar
img = Image.open('logo.png')

# Resize ke 256x256
img = img.resize((256, 256), Image.Resampling.LANCZOS)

# Simpan sebagai .ico
img.save('icon.ico', format='ICO')
```

Install Pillow dulu: `pip install Pillow`

## 🔧 Advanced Build Options

### Mengurangi Ukuran File

```bash
pyinstaller --onefile --windowed --name="RelayController" ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    relay_control_gui.py
```

### Menambahkan Data Files

Jika ada file tambahan (gambar, config, dll):

```bash
pyinstaller --onefile --windowed --name="RelayController" ^
    --add-data "images;images" ^
    --add-data "config.ini;." ^
    relay_control_gui.py
```

### Build dengan Spec File

1. Generate spec file:
```bash
pyi-makespec --onefile --windowed relay_control_gui.py
```

2. Edit `relay_control_gui.spec` sesuai kebutuhan

3. Build dari spec:
```bash
pyinstaller relay_control_gui.spec
```

## 📱 Troubleshooting

### 1. COM Port Tidak Muncul

**Penyebab:**
- Driver USB-to-Serial belum terinstall
- Kabel USB rusak atau tidak terhubung dengan baik
- Port USB bermasalah

**Solusi:**
- Install driver CH340 atau FTDI (sesuai chip USB relay)
- Coba kabel USB lain
- Coba port USB lain
- Klik tombol **🔄 Refresh** untuk update list port
- Cek di Device Manager (Windows) atau `dmesg` (Linux)

### 2. Gagal Connect

**Error: "Access Denied" atau "Permission Denied"**

**Windows:**
```
Tutup aplikasi lain yang menggunakan COM port tersebut
(Arduino IDE, PuTTY, Tera Term, dll)
```

**Linux:**
```bash
# Tambahkan user ke grup dialout
sudo usermod -a -G dialout $USER

# Logout dan login lagi, atau:
newgrp dialout
```

### 3. Relay Tidak Merespon

**Solusi:**
- Pastikan LED power di relay board menyala
- Cek koneksi USB
- Coba disconnect dan connect ulang
- Restart aplikasi
- Pastikan baud rate benar (default: 9600)

### 4. Executable Error

**Error: "Failed to execute script"**

**Solusi:**
- Rebuild executable dengan PyInstaller versi terbaru
- Cek antivirus (mungkin blocking file)
- Jalankan sebagai Administrator
- Build ulang dengan opsi `--debug all` untuk troubleshooting:
  ```bash
  pyinstaller --onefile --debug all relay_control_gui.py
  ```

### 5. Import Error saat Build

**Error: "ModuleNotFoundError"**

**Solusi:**
```bash
# Install ulang dependencies
pip uninstall pyserial
pip install pyserial

# Rebuild
pyinstaller --onefile --windowed relay_control_gui.py
```

## 📋 Spesifikasi Hardware

### USB Relay Module ICSE012A

| Spesifikasi | Detail |
|------------|--------|
| Model | ICSE012A 4-Channel |
| Voltage | 5V DC (USB Powered) |
| Relay Voltage | 250VAC / 30VDC |
| Relay Current | 10A Max |
| Interface | USB (CH340 / FT232) |
| Protocol | UART Serial |
| Baud Rate | 9600 bps (default) |
| Channels | 4 |

### Hex Command Reference

| Command | Hex Code | Function |
|---------|----------|----------|
| All OFF | 0x0F | Mematikan semua relay |
| Relay 1 ON | 0x0E | Hanya relay 1 nyala |
| Relay 2 ON | 0x0D | Hanya relay 2 nyala |
| Relay 3 ON | 0x0B | Hanya relay 3 nyala |
| Relay 4 ON | 0x07 | Hanya relay 4 nyala |
| All ON | 0x00 | Menyalakan semua relay |

Lihat kode lengkap untuk kombinasi relay lainnya.

## 📝 Command Line Version

Jika ingin menggunakan versi command-line (script original):

```bash
python 4ChannelRelayApp-ICSE012A-Python3_5_64bit.py
```

Ikuti instruksi di layar untuk kontrol manual via keyboard.

## 🚀 Tips & Tricks

### 1. Auto-Start Application

**Windows:**
1. Buat shortcut file `.exe`
2. Tekan `Win + R`, ketik `shell:startup`
3. Copy shortcut ke folder Startup

### 2. Multiple Relay Modules

Jika punya lebih dari satu relay module:
- Setiap module akan muncul sebagai COM port berbeda
- Bisa menjalankan multiple instance aplikasi
- Setiap instance connect ke COM port berbeda

### 3. Automation Script

Buat script Python untuk kontrol otomatis:

```python
import time
from relay_control_gui import RelayControlGUI

# Connect
relay = RelayControlGUI()
relay.connect_device("COM3")

# Sequencing
for i in range(1, 5):
    relay.toggle_relay(i)
    time.sleep(1)

# Disconnect
relay.disconnect_device()
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` file for more information.

