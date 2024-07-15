import serial
import tkinter as tk
from tkinter import messagebox
from serial.tools import list_ports

def connect_serial(port, baudrate):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1
        )
        return ser
    except serial.SerialException as e:
        messagebox.showerror("Serial Connection Error", f"Error opening serial port: {e}")
        return None

def send_command(ser, command):
    try:
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")
    except serial.SerialException as e:
        messagebox.showerror("Serial Write Error", f"Error writing to serial port: {e}")

def format_display_command(page, message):
    idxx = '01'  # Adjust as needed
    return f"<ID{idxx}><P{page}>{message}\r\n"

def send_message():
    message = message_entry.get()
    if not message:
        messagebox.showwarning("Input Error", "Message cannot be empty.")
        return
    
    command = format_display_command('A', message)
    send_command(serial_connection, command)

def connect():
    global serial_connection
    port = port_var.get()
    baudrate = baudrate_entry.get()

    if not port:
        messagebox.showwarning("Input Error", "Please select a COM port.")
        return
    if not baudrate:
        messagebox.showwarning("Input Error", "Please enter a baud rate.")
        return

    serial_connection = connect_serial(port, int(baudrate))
    if serial_connection:
        messagebox.showinfo("Connection Status", "Successfully connected to the serial port.")

# Set up the tkinter UI
root = tk.Tk()
root.title("ProLite Display Controller")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Dropdown menu for COM port selection
port_label = tk.Label(frame, text="Select COM Port:")
port_label.grid(row=0, column=0, pady=5)

ports = list_ports.comports()
port_var = tk.StringVar()
port_menu = tk.OptionMenu(frame, port_var, *[port.device for port in ports])
port_menu.grid(row=0, column=1, pady=5)

# Entry for baud rate
baudrate_label = tk.Label(frame, text="Enter Baud Rate:")
baudrate_label.grid(row=1, column=0, pady=5)

baudrate_entry = tk.Entry(frame)
baudrate_entry.grid(row=1, column=1, pady=5)

# Connect button
connect_button = tk.Button(frame, text="Connect", command=connect)
connect_button.grid(row=2, column=1, pady=10)

# Entry for message
message_label = tk.Label(frame, text="Enter Message:")
message_label.grid(row=3, column=0, pady=5)

message_entry = tk.Entry(frame, width=50)
message_entry.grid(row=3, column=1, pady=5)

# Send button
send_button = tk.Button(frame, text="Send", command=send_message)
send_button.grid(row=4, column=1, pady=10)

root.mainloop()

if 'serial_connection' in globals() and serial_connection:
    serial_connection.close()
