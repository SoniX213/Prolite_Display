import serial
import socket
import threading
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
        print(f"Error opening serial port: {e}")
        return None

def send_command(ser, command):
    try:
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")
    except serial.SerialException as e:
        print(f"Error writing to serial port: {e}")

def format_display_command(idxx, page, color, message):
    if color:
        return f"<ID{idxx}><P{page}><C{color}>{message}\r\n"
    else:
        return f"<ID{idxx}><P{page}>{message}\r\n"

def handle_client(client_socket, serial_connection):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message.strip()}")
            idxx, color, text = message.split('|')
            command = format_display_command(idxx, 'A', color, text)
            send_command(serial_connection, command)
    finally:
        client_socket.close()

def start_server(port, baudrate, com_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    serial_connection = connect_serial(com_port, baudrate)
    if not serial_connection:
        print("Failed to connect to serial port")
        return

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket, serial_connection)
            )
            client_handler.start()
    finally:
        server_socket.close()
        if serial_connection:
            serial_connection.close()

if __name__ == "__main__":
    COM_PORT = 'COM1'  # Replace with your COM port
    BAUD_RATE = 9600  # Replace with your baud rate
    SERVER_PORT = 9999  # Replace with your server port

    start_server(SERVER_PORT, BAUD_RATE, COM_PORT)
