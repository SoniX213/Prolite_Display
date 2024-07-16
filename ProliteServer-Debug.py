import serial
import socket
import threading
import time
import requests
from datetime import datetime

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

def get_weather():
    API_KEY = '49fbfa35d9b60f2327f6f46618305bc3'
    CITY = 'Longview'
    URL = f"http://api.openweathermap.org/data/2.0/weather?q={CITY}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if 'main' in data and 'temp' in data['main']:
            temperature = data['main']['temp']
            print(f"Fetched temperature: {temperature}°C")
            return temperature
        else:
            print(f"Unexpected response format: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def update_display_with_weather(serial_connection, idxx, color):
    temperature = get_weather()
    if temperature is not None:
        current_time = datetime.now().strftime('%H:%M')
        message = f"Temp: {temperature}C Time: {current_time}"
        command = format_display_command(idxx, 'A', color, message)
        send_command(serial_connection, command)

def handle_client(client_socket, serial_connection, idxx, color):
    global last_message_time, displaying_message
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message.strip()}")
            idxx, color, text = message.split('|')
            command = format_display_command(idxx, 'A', color, text)
            send_command(serial_connection, command)
            last_message_time = time.time()
            displaying_message = True
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

    global last_message_time, displaying_message
    last_message_time = 0
    displaying_message = False

    def weather_update_loop():
        global last_message_time, displaying_message
        while True:
            if not displaying_message or (time.time() - last_message_time > 60):
                update_display_with_weather(serial_connection, '00', '0')
                displaying_message = False
            time.sleep(60)

    weather_thread = threading.Thread(target=weather_update_loop)
    weather_thread.daemon = True
    weather_thread.start()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket, serial_connection, '00', '0')
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
