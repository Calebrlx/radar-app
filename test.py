import serial
import time

# Configuration for the radar module
RADAR_PORT = '/dev/ttyTHS1'  # Update with the correct UART port for the Jetson Nano
RADAR_BAUDRATE = 256000      # Default baud rate from the specifications

def read_radar_data(serial_connection):
    """
    Reads and displays radar data live from the serial connection.
    """
    try:
        while True:
            if serial_connection.in_waiting:
                raw_data = serial_connection.readline().decode('utf-8').strip()
                print(f"Raw Data: {raw_data}")

                # You can parse the raw data here if you know the format
                # For now, we'll just display the raw data
                # Example:
                # parsed_data = parse_radar_data(raw_data)
                # print(parsed_data)

            time.sleep(0.1)  # Small delay to avoid excessive CPU usage
    except KeyboardInterrupt:
        print("\nStopping radar data read.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """
    Main function to initialize the serial connection and read radar data.
    """
    try:
        # Initialize serial connection
        serial_connection = serial.Serial(
            port=RADAR_PORT,
            baudrate=RADAR_BAUDRATE,
            timeout=1,
        )
        print(f"Serial connection established on {RADAR_PORT}. Reading data...\n")
        
        # Read and display radar data
        read_radar_data(serial_connection)

    except serial.SerialException as e:
        print(f"Failed to connect to the radar module: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
