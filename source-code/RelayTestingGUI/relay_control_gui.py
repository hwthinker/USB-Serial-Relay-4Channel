"""
4-Channel USB Relay Control Application (ICSE012A)
Professional GUI Version with Enhanced Features
Author: HwThinker
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime


class RelayControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Channel USB Relay Controller - Made by hwthinker@gmail.com")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        
        # Serial connection
        self.ser = None
        self.connected = False
        
        # Relay states
        self.relay_states = {1: False, 2: False, 3: False, 4: False}
        
        # Hex commands for relay control
        self.relay_commands = {
            (False, False, False, False): b"\x0F",  # All OFF
            (True, False, False, False): b"\x0E",   # R1 ON
            (False, True, False, False): b"\x0D",   # R2 ON
            (True, True, False, False): b"\x0C",    # R1,R2 ON
            (False, False, True, False): b"\x0B",   # R3 ON
            (True, False, True, False): b"\x0A",    # R1,R3 ON
            (False, True, True, False): b"\x09",    # R2,R3 ON
            (True, True, True, False): b"\x08",     # R1,R2,R3 ON
            (False, False, False, True): b"\x07",   # R4 ON
            (True, False, False, True): b"\x06",    # R1,R4 ON
            (False, True, False, True): b"\x05",    # R2,R4 ON
            (True, True, False, True): b"\x04",     # R1,R2,R4 ON
            (False, False, True, True): b"\x03",    # R3,R4 ON
            (True, False, True, True): b"\x02",     # R1,R3,R4 ON
            (False, True, True, True): b"\x01",     # R2,R3,R4 ON
            (True, True, True, True): b"\x00",      # All ON
        }
        
        self.setup_ui()
        self.refresh_ports()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="4-Channel USB Relay Controller",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="ICSE012A Series ",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Connection Frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection Settings", padding=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Port selection
        port_frame = tk.Frame(conn_frame)
        port_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(port_frame, text="COM Port:", width=12, anchor="w").pack(side=tk.LEFT)
        self.port_combo = ttk.Combobox(port_frame, state="readonly", width=20)
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(port_frame, text="🔄 Refresh", command=self.refresh_ports).pack(side=tk.LEFT, padx=5)
        
        # Baud rate selection
        baud_frame = tk.Frame(conn_frame)
        baud_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(baud_frame, text="Baud Rate:", width=12, anchor="w").pack(side=tk.LEFT)
        self.baud_combo = ttk.Combobox(baud_frame, state="readonly", width=20, 
                                        values=["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.set("9600")
        self.baud_combo.pack(side=tk.LEFT, padx=5)
        
        # Connection buttons
        btn_frame = tk.Frame(conn_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.connect_btn = ttk.Button(btn_frame, text="Connect", command=self.connect_device)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = ttk.Button(btn_frame, text="Disconnect", 
                                          command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(btn_frame, text="● Disconnected", 
                                      fg="red", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Relay Control Frame
        relay_frame = ttk.LabelFrame(self.root, text="Relay Controls", padding=10)
        relay_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Individual relay controls
        self.relay_buttons = {}
        self.relay_indicators = {}
        
        controls_frame = tk.Frame(relay_frame)
        controls_frame.pack(pady=10)
        
        for i in range(1, 5):
            frame = tk.Frame(controls_frame, relief=tk.RIDGE, borderwidth=2, bg="#ecf0f1")
            frame.grid(row=0, column=i-1, padx=10, pady=5, sticky="nsew")
            
            # Relay label
            tk.Label(frame, text=f"Relay {i}", font=("Arial", 12, "bold"), 
                    bg="#ecf0f1").pack(pady=5)
            
            # Indicator
            indicator = tk.Canvas(frame, width=40, height=40, bg="#ecf0f1", highlightthickness=0)
            indicator.pack(pady=5)
            circle = indicator.create_oval(5, 5, 35, 35, fill="gray", outline="black", width=2)
            self.relay_indicators[i] = (indicator, circle)
            
            # Toggle button
            btn = ttk.Button(frame, text="ON", width=8,
                           command=lambda x=i: self.toggle_relay(x))
            btn.pack(pady=5, padx=10)
            self.relay_buttons[i] = btn
            
        # Quick control buttons
        quick_frame = tk.Frame(relay_frame)
        quick_frame.pack(pady=10)
        
        ttk.Button(quick_frame, text="All ON", command=self.all_on, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="All OFF", command=self.all_off, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Toggle All", command=self.toggle_all, width=12).pack(side=tk.LEFT, padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, 
                                                   font=("Consolas", 9), 
                                                   state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Label(self.root, text="© 2025 HwThinker", 
                         font=("Arial", 8), bg="#ecf0f1", fg="#7f8c8d")
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Initialize button states
        self.update_button_states()
        
    def log(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def refresh_ports(self):
        """Refresh available COM ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
            self.log(f"Found {len(port_list)} COM port(s)")
        else:
            self.log("No COM ports found", "WARNING")
            
    def connect_device(self):
        """Connect to the relay device"""
        if not self.port_combo.get():
            messagebox.showerror("Error", "Please select a COM port")
            return
            
        try:
            port = self.port_combo.get()
            baud = int(self.baud_combo.get())
            
            self.log(f"Connecting to {port} at {baud} baud...")
            
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(0.5)
            
            # Initialize the relay module
            self.initialize_relay()
            
            self.connected = True
            self.status_label.config(text="● Connected", fg="green")
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.update_button_states()
            
            self.log(f"Successfully connected to {port}", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect:\n{str(e)}")
            self.log(f"Connection failed: {str(e)}", "ERROR")
            
    def initialize_relay(self):
        """Initialize the relay module"""
        try:
            self.log("Initializing relay module...")
            commands = [b"\x50", b"\x51", b"\x01", b"\x00"]
            
            for cmd in commands:
                self.ser.write(cmd)
                time.sleep(0.1)
                
            # Turn all relays off
            self.ser.write(b"\x0F")
            time.sleep(0.1)
            
            self.log("Relay module initialized", "SUCCESS")
            
        except Exception as e:
            self.log(f"Initialization failed: {str(e)}", "ERROR")
            raise
            
    def disconnect_device(self):
        """Disconnect from the relay device"""
        if self.ser and self.ser.is_open:
            try:
                # Turn all relays off before disconnecting
                self.ser.write(b"\x0F")
                time.sleep(0.1)
                
                self.ser.close()
                self.connected = False
                
                self.status_label.config(text="● Disconnected", fg="red")
                self.connect_btn.config(state=tk.NORMAL)
                self.disconnect_btn.config(state=tk.DISABLED)
                
                # Reset relay states
                for i in range(1, 5):
                    self.relay_states[i] = False
                    self.update_indicator(i)
                    
                self.update_button_states()
                self.log("Disconnected from device", "INFO")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error during disconnect:\n{str(e)}")
                self.log(f"Disconnect error: {str(e)}", "ERROR")
                
    def send_relay_command(self):
        """Send relay command based on current states"""
        if not self.connected or not self.ser:
            return
            
        try:
            state_tuple = (self.relay_states[1], self.relay_states[2], 
                          self.relay_states[3], self.relay_states[4])
            command = self.relay_commands.get(state_tuple, b"\x0F")
            
            self.ser.write(command)
            time.sleep(0.05)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send command:\n{str(e)}")
            self.log(f"Command error: {str(e)}", "ERROR")
            
    def toggle_relay(self, relay_num):
        """Toggle individual relay"""
        if not self.connected:
            messagebox.showwarning("Warning", "Please connect to device first")
            return
            
        self.relay_states[relay_num] = not self.relay_states[relay_num]
        state = "ON" if self.relay_states[relay_num] else "OFF"
        
        self.send_relay_command()
        self.update_indicator(relay_num)
        
        self.log(f"Relay {relay_num} turned {state}")
        
    def all_on(self):
        """Turn all relays on"""
        if not self.connected:
            messagebox.showwarning("Warning", "Please connect to device first")
            return
            
        for i in range(1, 5):
            self.relay_states[i] = True
            self.update_indicator(i)
            
        self.send_relay_command()
        self.log("All relays turned ON")
        
    def all_off(self):
        """Turn all relays off"""
        if not self.connected:
            messagebox.showwarning("Warning", "Please connect to device first")
            return
            
        for i in range(1, 5):
            self.relay_states[i] = False
            self.update_indicator(i)
            
        self.send_relay_command()
        self.log("All relays turned OFF")
        
    def toggle_all(self):
        """Toggle all relays"""
        if not self.connected:
            messagebox.showwarning("Warning", "Please connect to device first")
            return
            
        for i in range(1, 5):
            self.relay_states[i] = not self.relay_states[i]
            self.update_indicator(i)
            
        self.send_relay_command()
        self.log("All relays toggled")
        
    def update_indicator(self, relay_num):
        """Update visual indicator for relay state"""
        indicator, circle = self.relay_indicators[relay_num]
        color = "#2ecc71" if self.relay_states[relay_num] else "gray"
        indicator.itemconfig(circle, fill=color)
        
    def update_button_states(self):
        """Update button states based on connection status"""
        state = tk.NORMAL if self.connected else tk.DISABLED
        
        for btn in self.relay_buttons.values():
            btn.config(state=state)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = RelayControlGUI(root)
    
    # Handle window close event
    def on_closing():
        if app.connected:
            if messagebox.askokcancel("Quit", "Disconnect and quit application?"):
                app.disconnect_device()
                root.destroy()
        else:
            root.destroy()
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
