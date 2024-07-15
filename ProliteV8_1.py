import serial
import tkinter as tk
from tkinter import messagebox
from serial.tools import list_ports

# Set a default baud rate
DEFAULT_BAUDRATE = 9600

# Global variable for the serial connection
serial_connection = None

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

def format_display_command(idxx, page, color, message):
    if color:
        return f"<ID{idxx}><P{page}><C{color}>{message}\r\n"
    else:
        return f"<ID{idxx}><P{page}>{message}\r\n"

def format_graphic_block_update(idxx, block_number, bit_pattern):
    if len(bit_pattern) > 126:
        messagebox.showwarning("Input Error", "Graphic block update must not exceed 126 bytes.")
        return ""
    
    # Format the command according to the specified format
    return f"<ID{idxx}><I{block_number}>{bit_pattern}\r\n"

def send_message():
    message = message_entry.get()
    idxx = id_var.get()
    color = color_var.get()
    if not message:
        messagebox.showwarning("Input Error", "Message cannot be empty.")
        return
    if not idxx:
        messagebox.showwarning("Input Error", "Please select an ID.")
        return
    
    command = format_display_command(idxx, 'A', color, message)
    send_command(serial_connection, command)

def update_graphic_block():
    block_number = graphic_block_var.get()
    bit_pattern = bit_pattern_entry.get()
    idxx = id_var.get()
    
    if not block_number:
        messagebox.showwarning("Input Error", "Please select a graphic block number.")
        return
    if not bit_pattern:
        messagebox.showwarning("Input Error", "Please enter a bit pattern.")
        return
    
    command = format_graphic_block_update(idxx, block_number, bit_pattern)
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

# Entry for baud rate with default value
baudrate_label = tk.Label(frame, text="Enter Baud Rate:")
baudrate_label.grid(row=1, column=0, pady=5)

baudrate_entry = tk.Entry(frame)
baudrate_entry.insert(0, str(DEFAULT_BAUDRATE))  # Set default value
baudrate_entry.grid(row=1, column=1, pady=5)

# Dropdown menu for ID selection
id_label = tk.Label(frame, text="Select ID:")
id_label.grid(row=2, column=0, pady=5)

id_var = tk.StringVar()
id_menu = tk.OptionMenu(frame, id_var, '00', '01', '02', '03', '04', '05')  # Add more IDs as needed
id_menu.grid(row=2, column=1, pady=5)

# Connect button
connect_button = tk.Button(frame, text="Connect", command=connect)
connect_button.grid(row=6, column=1, pady=10)

# Dropdown menu for graphic block selection
graphic_block_label = tk.Label(frame, text="Select Graphic Block:")
graphic_block_label.grid(row=3, column=0, pady=5)

graphic_block_var = tk.StringVar()
graphic_block_menu = tk.OptionMenu(frame, graphic_block_var, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
graphic_block_menu.grid(row=3, column=1, pady=5)

# Entry for bit pattern
bit_pattern_label = tk.Label(frame, text="Enter Bit Pattern (126 bytes):")
bit_pattern_label.grid(row=4, column=0, pady=5)

bit_pattern_entry = tk.Entry(frame, width=50)
bit_pattern_entry.grid(row=4, column=1, pady=5)

# Update graphic block button
update_block_button = tk.Button(frame, text="Update Graphic Block", command=update_graphic_block)
update_block_button.grid(row=5, column=1, pady=10)

# Dropdown menu for color selection
color_label = tk.Label(frame, text="Select Color (Optional):")
color_label.grid(row=7, column=0, pady=5)

color_var = tk.StringVar()
color_menu = tk.OptionMenu(frame, color_var, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')  # Add color codes as needed
color_menu.grid(row=7, column=1, pady=5)

# Entry for message
message_label = tk.Label(frame, text="Enter Message:")
message_label.grid(row=8, column=0, pady=5)

message_entry = tk.Entry(frame, width=50)
message_entry.grid(row=8, column=1, pady=5)

# Send button
send_button = tk.Button(frame, text="Send", command=send_message)
send_button.grid(row=9, column=1, pady=10)

root.mainloop()

if 'serial_connection' in globals() and serial_connection:
    serial_connection.close()
