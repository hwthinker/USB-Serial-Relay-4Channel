
# 4-Channel USB Relay Controller (ICSE012A/HW-034)

Skrip ini digunakan untuk mengendalikan **modul USB relay 4-channel ICSE012A** menggunakan Python melalui port serial (misalnya `COM3`, `COM2`, atau `/dev/ttyUSB0` di Linux).

Dibuat agar perintah terminal lebih **konsisten, profesional, dan stabil**, dengan dukungan:
- Inisialisasi manual (`init`)
- Pengendalian per channel
- Kombinasi ON/OFF fleksibel
- Pengujian otomatis (test mode)

---

## ⚠️ Peringatan Penting: Jalankan `init` Terlebih Dahulu

Sebelum menggunakan perintah lain seperti `on`, `set`, atau `all-on`, **Anda harus menjalankan perintah inisialisasi (`init`) satu kali setiap kali modul relay dicolokkan atau setelah sistem direset.**

Tanpa perintah `init`, **modul tidak akan merespons** perintah ON/OFF apa pun.

---

## 🔧 Instalasi Awal

1. Pastikan Python 3 sudah terpasang (versi 3.7 atau lebih baru).
2. Instal pustaka **PySerial**:
   ```bash
   pip install pyserial
   ```
3. Unduh file [`relay_pro.py`](relay_pro.py) ke dalam folder kerja Anda.

---

## 🚀 Cara Penggunaan

### 1. Lihat daftar port serial yang tersedia
Gunakan perintah ini untuk memastikan port tempat modul relay terdeteksi.
```bash
python relay_pro.py ports
```

Contoh output:
```
COM2
COM4
```

---

### 2. Inisialisasi Modul Relay (WAJIB)
Perintah ini **harus dijalankan sekali** setelah modul USB relay baru dicolokkan.  
Inisialisasi akan mengirim urutan khusus `[0x50, 0x51, 0x01, 0x00]` ke perangkat.

```bash
python relay_pro.py --port COM2 init
```

Output:
```
Init selesai.
```

> 💡 Jika Anda tidak menjalankan `init`, semua perintah berikut tidak akan direspons oleh modul relay.

---

### 3. Nyalakan semua relay
```bash
python relay_pro.py --port COM2 all-on
```
Output:
```
Semua relay ON.
```

---

### 4. Matikan semua relay
```bash
python relay_pro.py --port COM2 all-off
```
Output:
```
Semua relay OFF.
```

---

### 5. Nyalakan satu channel tertentu
```bash
python relay_pro.py --port COM2 on 1
```
Artinya:
- Channel 1 → ON  
- Channel 2, 3, 4 → OFF

Output:
```
Relay 1 ON (yang lain OFF).
```

---

### 6. Nyalakan kombinasi channel tertentu
Gunakan `set` diikuti angka channel yang ingin ON.

```bash
python relay_pro.py --port COM2 set 13
```
Artinya:
- Channel 1 dan 3 → ON  
- Channel 2 dan 4 → OFF

Output:
```
Kombinasi aktif: [1, 3]
```

Format lain yang juga valid:
```bash
python relay_pro.py --port COM2 set "1 3 4"
python relay_pro.py --port COM2 set "1,3"
```

---

### 7. Uji seluruh channel secara otomatis
Perintah ini akan menyalakan relay 1–4 secara berurutan dengan jeda waktu antar channel.

```bash
python relay_pro.py --port COM2 test --repeat 2 --delay 0.5
```

Artinya:
- Jalankan siklus nyala berurutan **sebanyak 2 kali**
- Delay antar channel **0.5 detik**

Output:
```
Channel 1 ON
Channel 2 ON
Channel 3 ON
Channel 4 ON
All OFF
(ulang 2x)
```

---

## 🧪 Urutan Penggunaan Lengkap (Disarankan)

1️⃣ **Deteksi port:**
```bash
python relay_pro.py ports
```

2️⃣ **Inisialisasi modul (WAJIB):**
```bash
python relay_pro.py --port COM2 init
```

3️⃣ **Gunakan perintah kontrol:**
```bash
python relay_pro.py --port COM2 all-on
python relay_pro.py --port COM2 all-off
python relay_pro.py --port COM2 set 13
python relay_pro.py --port COM2 on 1
python relay_pro.py --port COM2 test --repeat 2 --delay 0.5
```

---

## 🧩 Troubleshooting

| Masalah | Penyebab | Solusi |
|----------|-----------|---------|
| `Gagal membuka port COMx` | Port salah atau sudah dipakai program lain | Cek Device Manager dan pastikan port sesuai |
| Relay tidak merespons sama sekali | Belum menjalankan `init` | Jalankan `python relay_pro.py --port COMx init` |
| Hanya sebagian relay menyala | Kombinasi `set` salah atau urutan byte tidak sesuai | Pastikan nomor channel 1–4 dan gunakan format benar (`13`, `1 3`, atau `1,3`) |

---

## 📜 Catatan Teknis

- **Protokol init**: `[0x50, 0x51, 0x01, 0x00]`
- **Baudrate default**: `9600`
- **Jumlah channel**: 4
- **Byte encoding** mengikuti tabel kombinasi ICSE012A

---

## 👨‍💻 Contoh Otomatisasi Batch (Windows)
Buat file `run_relay.bat`:
```bat
@echo off
python relay_pro.py --port COM2 init
python relay_pro.py --port COM2 set 13
timeout /t 5 >nul
python relay_pro.py --port COM2 all-off
```

