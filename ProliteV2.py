import serial
import tkinter as tk
from tkinter import messagebox

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

# Replace with your serial port and baud rate
port = 'COM3'  # Example for Windows, replace with your actual port
# port = '/dev/ttyUSB0'  # Example for Linux, replace with your actual port
baudrate = 9600  # Replace with the correct baud rate for your ProLite display

serial_connection = connect_serial(port, baudrate)
if serial_connection is None:
    exit()

# Set up the tkinter UI
root = tk.Tk()
root.title("ProLite Display Controller")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

message_label = tk.Label(frame, text="Enter Message:")
message_label.pack(side=tk.LEFT)

message_entry = tk.Entry(frame, width=50)
message_entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

root.mainloop()

serial_connection.close()
