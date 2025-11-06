# 🚀 Relay Controller - Quick Start

## Cara Paling Cepat Mulai

### 📦 Yang Anda Dapat:

```
📁 Project Files
├── 📄 relay_control_gui.py      ← Source code aplikasi GUI
├── 📄 requirements.txt          ← List library yang diperlukan
├── 📄 install.bat              ← Install dependencies (Windows)
├── 📄 build.bat                ← Build executable otomatis (Windows)
├── 📄 build.sh                 ← Build executable otomatis (Linux)
├── 📘 README.md                ← Dokumentasi lengkap
├── 📗 QUICKSTART.md            ← Panduan build executable
├── 📙 TUTORIAL.md              ← Tutorial step-by-step detail
└── 📕 GETTING_STARTED.md       ← File ini
```

---

## 🎯 Pilih Metode:

### ⚡ Metode 1: Langsung Pakai (Paling Cepat!)

**Jika sudah ada file `RelayController.exe`:**
1. Double-click `RelayController.exe`
2. Selesai! Tidak perlu install apapun

---

### 🔧 Metode 2: Jalankan dari Source Code

**Untuk development atau modifikasi:**

#### Windows:

```cmd
REM 1. Install dependencies
install.bat

REM 2. Jalankan aplikasi
python relay_control_gui.py
```

#### Linux:

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Jalankan aplikasi
python3 relay_control_gui.py
```

---

### 📦 Metode 3: Build Executable Sendiri

**Untuk distribusi ke komputer lain:**

#### Windows:

```cmd
REM Otomatis - double click saja
build.bat

REM Manual
pyinstaller --onefile --windowed --name="RelayController" relay_control_gui.py
```

#### Linux:

```bash
# Otomatis
chmod +x build.sh
./build.sh

# Manual
pyinstaller --onefile --windowed --name="RelayController" relay_control_gui.py
```

**Hasil:** File executable ada di folder `dist/`

---

## 📖 Dokumentasi Lengkap

| File | Isi |
|------|-----|
| **README.md** | Dokumentasi lengkap dengan semua fitur |
| **QUICKSTART.md** | Cara build executable (ringkas) |
| **TUTORIAL.md** | Tutorial step-by-step untuk pemula |

---

## ⚙️ Spesifikasi Hardware

- **Module:** USB Relay ICSE012A 4-Channel
- **Interface:** USB Serial (CH340/FTDI)
- **Baud Rate:** 9600 bps
- **Voltage:** 5V (USB powered)
- **Relay Rating:** 250VAC/30VDC, 10A

---

## 🆘 Bantuan Cepat

### COM Port tidak muncul?
```
1. Install driver CH340/FTDI
2. Coba port USB lain
3. Restart komputer
4. Klik tombol Refresh
```

### Error "Access Denied"?
```
Windows: Tutup aplikasi serial lain (Arduino IDE, dll)
Linux: sudo usermod -a -G dialout $USER (logout & login)
```

### Build error?
```
pip install --upgrade pip
pip install pyinstaller --force-reinstall
```

---

**Made by HwThinker ** 🎓
