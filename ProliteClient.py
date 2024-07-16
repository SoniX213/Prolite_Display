import socket
import tkinter as tk
from tkinter import messagebox

#Set Defaults
DEFAULT_ID = '01'
DEFAULT_PORT = '9999'
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
    
    message = f"{idxx}|{color}|{message}"
    client_socket.send(message.encode())

def connect_to_server():
    global client_socket
    host = host_entry.get()
    port = int(port_entry.get())
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        messagebox.showinfo("Connection Status", "Successfully connected to the server.")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Error connecting to server: {e}")

# Set up the tkinter UI
root = tk.Tk()
root.title("ProLite Display Client")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Entry for server host
host_label = tk.Label(frame, text="Server Host:")
host_label.grid(row=0, column=0, pady=5)

host_entry = tk.Entry(frame)
host_entry.grid(row=0, column=1, pady=5)

# Entry for server port
port_label = tk.Label(frame, text="Server Port:")
port_label.grid(row=1, column=0, pady=5)

port_entry = tk.Entry(frame)
port_entry.insert(0, str(DEFAULT_PORT))
port_entry.grid(row=1, column=1, pady=5)

# Connect button
connect_button = tk.Button(frame, text="Connect", command=connect_to_server)
connect_button.grid(row=2, column=1, pady=10)

# Dropdown menu for ID selection
id_label = tk.Label(frame, text="Select ID:")
id_label.grid(row=3, column=0, pady=5)

id_var = tk.StringVar(value=DEFAULT_ID)
id_menu = tk.OptionMenu(frame, id_var, '00', '01', '02', '03', '04', '05')  # Add more IDs as needed
id_menu.grid(row=3, column=1, pady=5)

# Dropdown menu for color selection
color_label = tk.Label(frame, text="Select Color (Optional):")
color_label.grid(row=4, column=0, pady=5)

color_var = tk.StringVar()
color_menu = tk.OptionMenu(frame, color_var, '0', '1', '2', '3', '4', '5', '6', '7')  # Add color codes as needed
color_menu.grid(row=4, column=1, pady=5)

# Entry for message
message_label = tk.Label(frame, text="Enter Message:")
message_label.grid(row=5, column=0, pady=5)

message_entry = tk.Entry(frame, width=50)
message_entry.grid(row=5, column=1, pady=5)

# Send button
send_button = tk.Button(frame, text="Send", command=send_message)
send_button.grid(row=6, column=1, pady=10)

root.mainloop()
