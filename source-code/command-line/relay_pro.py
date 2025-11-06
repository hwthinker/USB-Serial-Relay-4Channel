#!/usr/bin/env python3
"""
Professional 4-Channel USB Relay Controller (ICSE012A)
======================================================
Gaya pemakaian konsisten:
  - all-on / all-off
  - set <kombinasi angka>
  - on <channel>
  - test --repeat N --delay S
  - init (inisialisasi manual, lakukan SEKALI setelah modul dicolok)
  - interactive (REPL, ketik perintah langsung)

Contoh cepat:
  python relay_pro.py ports
  python relay_pro.py --port COM2 init
  python relay_pro.py --port COM2 interactive
  python relay_pro.py --port COM2 all-on
  python relay_pro.py --port COM2 all-off
  python relay_pro.py --port COM2 set 13
  python relay_pro.py --port COM2 on 1
  python relay_pro.py --port COM2 test --repeat 2 --delay 0.5
"""

import argparse
import sys
import time
from typing import Iterable, Optional, List

try:
    import serial
    import serial.tools.list_ports as list_ports
except Exception:
    print("PySerial belum terinstal. Jalankan: pip install pyserial", file=sys.stderr)
    sys.exit(1)


# =============================
# Peta Kombinasi ICSE012A
# =============================
BYTE_FOR_SET = {
    frozenset({1}): 0x0E,
    frozenset({2}): 0x0D,
    frozenset({3}): 0x0B,
    frozenset({4}): 0x07,
    frozenset({1, 2}): 0x0C,
    frozenset({1, 3}): 0x0A,
    frozenset({1, 4}): 0x06,
    frozenset({2, 3}): 0x09,
    frozenset({2, 4}): 0x05,
    frozenset({3, 4}): 0x03,
    frozenset({1, 2, 3}): 0x08,
    frozenset({1, 2, 4}): 0x04,
    frozenset({1, 3, 4}): 0x02,
    frozenset({2, 3, 4}): 0x01,
    frozenset({1, 2, 3, 4}): 0x00,
    frozenset(): 0x0F,
}

INIT_SEQUENCE = [0x50, 0x51, 0x01, 0x00]


def list_serial_ports() -> list[str]:
    return [p.device for p in list_ports.comports()]


class Relay:
    def __init__(self, port: str, baud: int = 9600, timeout: float = 1.0):
        self.port = port
        try:
            self.ser = serial.Serial(port, baudrate=baud, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Gagal membuka port {port}: {e}")

    def init_device(self):
        """Kirim urutan inisialisasi sekali setelah modul dicolok."""
        print("Mengirim urutan inisialisasi ke modul...")
        time.sleep(0.2)
        for b in INIT_SEQUENCE:
            self.ser.write(bytes([b]))
            time.sleep(0.2)
        print("Inisialisasi selesai.")

    def write_byte(self, value: int):
        self.ser.write(bytes([value & 0xFF]))

    def set_combination(self, relays: Iterable[int]):
        s = frozenset(relays)
        if not all(r in {1, 2, 3, 4} for r in s):
            raise ValueError("Nomor relay harus 1..4")
        byte = BYTE_FOR_SET.get(s)
        if byte is None:
            raise ValueError("Kombinasi tidak dikenali")
        self.write_byte(byte)

    def all_on(self):
        self.write_byte(0x00)

    def all_off(self):
        self.write_byte(0x0F)

    def on(self, channel: int):
        if channel not in {1, 2, 3, 4}:
            raise ValueError("Channel harus 1..4")
        self.set_combination({channel})

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass


def parse_combo_string(s: str) -> List[int]:
    """Terima input seperti '13', '1,3', atau '1 3 4'."""
    s = s.replace(",", " ").strip()
    parts = [p for p in s.split() if p]
    if len(parts) == 1 and parts[0].isdigit() and len(parts[0]) <= 4:
        return [int(ch) for ch in parts[0]]
    nums: List[int] = []
    for p in parts:
        if not p.isdigit():
            raise ValueError(f"Token bukan angka: {p}")
        nums.append(int(p))
    return nums


def do_interactive(relay: Relay):
    """Mode interaktif REPL."""
    print("Masuk mode interaktif. Ketik 'help' untuk bantuan, 'exit' untuk keluar.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue

        cmd = line.split()
        op = cmd[0].lower()

        if op in {"exit", "quit", "q"}:
            break
        if op in {"help", "h", "?"}:
            print("""
Perintah:
  on N          -> Nyalakan channel N (1..4)
  set COMBO     -> Contoh: 13  |  1,3  |  1 3 4
  all-on        -> Semua ON
  all-off       -> Semua OFF
  test [delay] [repeat]
  help          -> Tampilkan bantuan
  exit          -> Keluar
            """)
            continue
        try:
            if op == "on" and len(cmd) >= 2:
                n = int(cmd[1])
                relay.on(n)
                print(f"Relay {n} ON (yang lain OFF).")
            elif op == "set" and len(cmd) >= 2:
                combo = parse_combo_string(" ".join(cmd[1:]))
                relay.set_combination(combo)
                print(f"Kombinasi aktif: {combo}")
            elif op == "all-on":
                relay.all_on()
                print("Semua relay ON.")
            elif op == "all-off":
                relay.all_off()
                print("Semua relay OFF.")
            elif op == "test":
                delay = float(cmd[1]) if len(cmd) > 1 else 0.4
                repeat = int(cmd[2]) if len(cmd) > 2 else 1
                for _ in range(repeat):
                    for ch in (1, 2, 3, 4):
                        relay.set_combination([ch])
                        print(f"Channel {ch} ON")
                        time.sleep(delay)
                    relay.all_off()
                    print("All OFF")
                    time.sleep(delay)
            else:
                print("Perintah tidak dikenali. Ketik 'help' untuk daftar.")
        except Exception as e:
            print(f"Error: {e}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="relay_pro.py",
        description="Kontrol modul USB 4-channel relay (ICSE012A)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--port", "-p", help="Nama port serial (mis. COM3)")
    p.add_argument("--baud", type=int, default=9600, help="Baud rate")

    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ports", help="Tampilkan daftar port serial")
    sub.add_parser("init", help="Inisialisasi modul relay (jalankan sekali setelah colok USB)")

    sp_on = sub.add_parser("on", help="Nyalakan satu channel (yang lain OFF)")
    sp_on.add_argument("channel", type=int, choices=[1, 2, 3, 4], help="Nomor channel")

    sp_set = sub.add_parser("set", help="Set kombinasi ON (mis. 13 → channel 1 & 3 ON)")
    sp_set.add_argument("combo", help="Kombinasi channel, contoh: 13 atau '1 3 4'")

    sub.add_parser("all-on", help="Semua relay ON")
    sub.add_parser("all-off", help="Semua relay OFF")

    sp_test = sub.add_parser("test", help="Uji semua channel secara berurutan")
    sp_test.add_argument("--delay", type=float, default=0.4, help="Delay antar channel (detik)")
    sp_test.add_argument("--repeat", type=int, default=1, help="Jumlah pengulangan urutan")

    sub.add_parser("interactive", help="Mode interaktif (REPL)")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "ports":
        ports = list_serial_ports()
        print("\n".join(ports) if ports else "(tidak ada port)")
        return 0

    if not args.port:
        raise SystemExit("Error: --port wajib digunakan (contoh: --port COM3)")

    try:
        r = Relay(port=args.port, baud=args.baud)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 2

    try:
        if args.cmd == "init":
            r.init_device()
            print("Init selesai.")
        elif args.cmd == "on":
            r.on(args.channel)
            print(f"Relay {args.channel} ON (yang lain OFF).")
        elif args.cmd == "set":
            combo = parse_combo_string(args.combo)
            r.set_combination(combo)
            print(f"Kombinasi aktif: {combo}")
        elif args.cmd == "all-on":
            r.all_on()
            print("Semua relay ON.")
        elif args.cmd == "all-off":
            r.all_off()
            print("Semua relay OFF.")
        elif args.cmd == "test":
            for _ in range(args.repeat):
                for ch in (1, 2, 3, 4):
                    r.set_combination([ch])
                    print(f"Channel {ch} ON")
                    time.sleep(args.delay)
                r.all_off()
                print("All OFF")
                time.sleep(args.delay)
        elif args.cmd == "interactive":
            print("Masuk mode REPL. (Pastikan sudah 'init' sebelumnya jika modul baru dicolok.)")
            do_interactive(r)
        else:
            parser.print_help()
            return 1
    finally:
        r.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

