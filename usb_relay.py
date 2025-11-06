#!/usr/bin/env python3
import argparse, sys, serial, time

# Peta perintah (HEX) sesuai protokol
CMD_MAP = {
    ("on",  1): bytes.fromhex("A0 01 01 A2"),
    ("off", 1): bytes.fromhex("A0 01 00 A1"),
    ("on",  2): bytes.fromhex("A0 02 01 A3"),
    ("off", 2): bytes.fromhex("A0 02 00 A2"),
    ("on",  3): bytes.fromhex("A0 03 01 A4"),
    ("off", 3): bytes.fromhex("A0 03 00 A3"),
    ("on",  4): bytes.fromhex("A0 04 01 A5"),
    ("off", 4): bytes.fromhex("A0 04 00 A4"),
    # status check semua relay (berdasar fitur #4: 0xFF)
    ("status", 0): bytes.fromhex("FF"),
}

def open_serial(port, baud=9600, timeout=0.3):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        # Beberapa modul butuh jeda setelah open
        time.sleep(0.1)
        return ser
    except Exception as e:
        print(f"Gagal buka port {port}: {e}")
        sys.exit(1)

def send_cmd(ser, data: bytes, read_expected=True):
    ser.write(data)
    ser.flush()
    # Banyak modul merespons 1–4 byte. Kita coba baca sebentar.
    time.sleep(0.05)
    resp = ser.read(64) if read_expected else b""
    return resp

def parse_status(resp: bytes):
    # Modul berbeda-beda formatnya. Jika modulmu membalas 1 byte bitmask,
    # contoh: bit0..bit3 untuk CH1..CH4 (1=ON).
    # Kalau respons kosong, tampilkan apa adanya.
    if not resp:
        return "tidak ada respons"
    # Coba heuristik: kalau hanya 1 byte, tampilkan bitnya.
    if len(resp) == 1:
        b = resp[0]
        bits = [(b >> i) & 1 for i in range(4)]  # [CH1,CH2,CH3,CH4]
        return f"raw=0x{b:02X}  -> CH1={bits[0]} CH2={bits[1]} CH3={bits[2]} CH4={bits[3]}"
    # Selain itu, tampilkan hex mentah.
    return "raw=" + resp.hex(" ").upper()

def main():
    ap = argparse.ArgumentParser(
        description="CLI kontrol USB 4-Channel Relay (CH340, 9600 bps)."
    )
    ap.add_argument("--port", required=True, help="Nama port serial (contoh: COM5 di Windows, /dev/ttyUSB0 di Linux).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # on/off
    for c in ("on", "off"):
        sp = sub.add_parser(c, help=f"{c} <channel>")
        sp.add_argument("channel", type=int, choices=[1,2,3,4])

    # status
    sub.add_parser("status", help="Cek status semua relay (command 0xFF).")

    args = ap.parse_args()

    ser = open_serial(args.port, baud=9600, timeout=0.3)

    try:
        if args.cmd in ("on", "off"):
            payload = CMD_MAP[(args.cmd, args.channel)]
            resp = send_cmd(ser, payload, read_expected=True)
            print(f"kirim: {payload.hex(' ').upper()}")
            print(f"balik: {resp.hex(' ').upper() if resp else '(kosong)'}")
        elif args.cmd == "status":
            payload = CMD_MAP[("status", 0)]
            resp = send_cmd(ser, payload, read_expected=True)
            print(f"kirim: {payload.hex(' ').upper()}")
            print(f"balik: {resp.hex(' ').upper() if resp else '(kosong)'}")
            print(parse_status(resp))
    finally:
        ser.close()

if __name__ == "__main__":
    main()

