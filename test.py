import serial
import time

# Replace with your actual serial port
RADAR_PORT = '/dev/ttyTHS1'  # Update this to the correct serial port
RADAR_BAUDRATE = 256000      # Use the baud rate specified by your radar

def read_radar_data(serial_connection):
    while True:
        if serial_connection.in_waiting:
            raw_data = serial_connection.readline()
            try:
                # Decode and strip any whitespace
                raw_data = raw_data.decode("utf-8").strip()
                print(f"Raw Data: {raw_data}")

                # Parse the raw data based on radar's data format
                # For example purposes, we will just print it
                # You will need to implement parsing logic here

            except UnicodeDecodeError:
                print("Received non-UTF-8 data. Skipping...")
        else:
            # No data waiting
            pass
        time.sleep(0.1)  # Adjust the interval as needed

if __name__ == "__main__":
    try:
        serial_connection = serial.Serial(RADAR_PORT, RADAR_BAUDRATE, timeout=1)
        print(f"Serial connection established on {RADAR_PORT}. Reading data...\n")
        read_radar_data(serial_connection)
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
