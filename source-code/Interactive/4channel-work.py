# 4ChannelRelayApp-ICSE012A-fix.py
import sys
import time
import serial
import serial.tools.list_ports

def userManual():
    print('-----------------------------------------------------------------')
    print('\t\tPYTHON RELAY APPLICATION')
    print('-----------------------------------------------------------------')
    print('\n\tType in 1/2/3/4 to turn on a relay')
    print('\tType in 12, 13, 14, 23, 24, 34 for pairs')
    print('\tType in 123, 124, 134, 234 for triples')
    print('\tType in 1234 for all ON, 00 for all OFF')
    print('\tType in UM for user manual, Q to quit')
    print('-----------------------------------------------------------------')

def initialization(ser):
    # same init sequence, but with safer writes + flush
    seq = [b"\x50", b"\x51", b"\x01", b"\x00"]
    print("System initialization in progress. Please wait...\n")
    for cmd in seq:
        ser.write(cmd)
        ser.flush()
        time.sleep(0.3)
    userManual()

def open_port_interactive():
    # list available ports
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Tidak ada COM port terdeteksi. Cek Device Manager > Ports (COM & LPT).")
    else:
        print("Port terdeteksi:")
        for i, p in enumerate(ports, 1):
            desc = f"{p.device} — {p.description}"
            if p.vid is not None and p.pid is not None:
                desc += f" (VID:PID={p.vid:04X}:{p.pid:04X})"
            print(f"  [{i}] {desc}")

    while True:
        raw = input("\nKetik nama port (mis. COM2) atau nomor indeks di atas,\natau tekan Enter untuk coba otomatis, atau Q untuk keluar: ").strip()
        if raw.lower() == 'q':
            sys.exit(0)

        # try index selection
        candidate = None
        if raw == '':
            # try simple heuristics: pick first port that isn't Bluetooth
            if ports:
                for p in ports:
                    if "Bluetooth" not in (p.description or ""):
                        candidate = p.device
                        break
                if candidate is None:
                    candidate = ports[0].device
            else:
                print("Auto-detect gagal (tidak ada port).")
        elif raw.isdigit() and ports:
            idx = int(raw)
            if 1 <= idx <= len(ports):
                candidate = ports[idx-1].device
            else:
                print("Indeks di luar jangkauan.")
        else:
            candidate = raw  # assume user typed COMx

        if not candidate:
            continue

        try:
            ser = serial.Serial(
                candidate,
                9600,
                timeout=1,
                write_timeout=1
            )
            # opsional: toggle DTR/RTS jika dibutuhkan oleh beberapa board
            try:
                ser.dtr = True
                ser.rts = True
            except Exception:
                pass
            print(f"Berhasil membuka port: {candidate}")
            return ser
        except Exception as e:
            print(f"Gagal membuka {candidate}: {e}")
            # lanjut loop biar user bisa coba lagi

def mainLoop(ser):
    # mapping byte commands (sama seperti file asli)
    all_relays_on  = b"\x00"
    relays_432_on  = b"\x01"
    relays_431_on  = b"\x02"
    relays_43_on   = b"\x03"
    relays_421_on  = b"\x04"
    relays_42_on   = b"\x05"
    relays_41_on   = b"\x06"
    relay_4_on     = b"\x07"
    relays_321_on  = b"\x08"
    relays_32_on   = b"\x09"
    relays_31_on   = b"\x0A"
    relay_3_on     = b"\x0B"
    relays_21_on   = b"\x0C"
    relay_2_on     = b"\x0D"
    relay_1_on     = b"\x0E"
    all_relays_off = b"\x0F"

    initialization(ser)

    while True:
        inputCommand = input('\nType Y to continue, UM for manual, or Q to quit: ').strip()
        if inputCommand.lower() == 'y':
            while True:
                controlCommand = input('\nCommand: ').strip()
                table = {
                    '1': relay_1_on, '2': relay_2_on, '3': relay_3_on, '4': relay_4_on,
                    '12': relays_21_on, '13': relays_31_on, '14': relays_41_on,
                    '23': relays_32_on, '24': relays_42_on, '34': relays_43_on,
                    '123': relays_321_on, '124': relays_421_on,
                    '134': relays_431_on, '234': relays_432_on,
                    '1234': all_relays_on, '00': all_relays_off
                }

                if controlCommand.lower() == 'q':
                    print('Exit control loop.')
                    break
                elif controlCommand.lower() == 'um':
                    userManual()
                    continue
                elif controlCommand in table:
                    try:
                        ser.write(table[controlCommand])
                        ser.flush()
                        print('OK sent.')
                    except Exception as e:
                        print(f"Gagal kirim: {e}")
                else:
                    print('Wrong input! Try again.')

        elif inputCommand.lower() == 'um':
            userManual()
        elif inputCommand.lower() == 'q':
            print('Bye.')
            break
        else:
            print('Wrong input! Try again.')

if __name__ == "__main__":
    ser = open_port_interactive()
    mainLoop(ser)
    try:
        ser.close()
    except Exception:
        pass

