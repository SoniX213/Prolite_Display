import serial
import time

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

def format_display_command(page, message):
    # IDXX is 01 for this example; adjust as needed
    idxx = '01'
    return f"<ID{idxx}><P{page}>{message}\r\n"

def main():
    # Replace with your serial port and baud rate
    port = 'COM1'  # Example for Windows, replace with your actual port
    # port = '/dev/ttyUSB0'  # Example for Linux, replace with your actual port
    baudrate = 9600  # Replace with the correct baud rate for your ProLite display
    
    ser = connect_serial(port, baudrate)
    if ser is None:
        return

    try:
        while True:
            # Replace this with the actual logic to retrieve the data you want to display
            data_to_display = time.strftime("%Y-%m-%d %H:%M:%S")  # Example: current date and time
            
            # Format the command according to your ProLite display's protocol
            command = format_display_command('A', data_to_display)
            
            send_command(ser, command)
            
            # Sleep for a while before sending the next update
            time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Exiting script.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
