import serial
import time

# Configuration for the radar module
RADAR_PORT = '/dev/ttyTHS1'  # Replace with your actual UART port
RADAR_BAUDRATE = 256000      # Default baud rate for the radar module

def read_raw_data():
    """
    Reads raw binary data from the radar and prints it in hex format.
    """
    try:
        # Open serial connection
        with serial.Serial(RADAR_PORT, RADAR_BAUDRATE, timeout=1) as ser:
            print(f"Listening on {RADAR_PORT} at {RADAR_BAUDRATE} baud...")
            print("Press Ctrl+C to stop.")

            while True:
                if ser.in_waiting:  # Check if there is data waiting to be read
                    raw_data = ser.read(ser.in_waiting)  # Read all available data
                    print(f"Raw Data (Hex): {raw_data.hex(' ')}")  # Print in hex format

                time.sleep(0.1)  # Small delay to reduce CPU usage

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped reading data.")

if __name__ == "__main__":
    read_raw_data()
