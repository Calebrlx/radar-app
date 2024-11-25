import serial
import time

# Configuration for the radar module
RADAR_PORT = '/dev/ttyTHS1'  # Replace with your actual UART port
RADAR_BAUDRATE = 256000      # Default baud rate for the radar module

def decode_packet(raw_data):
    """
    Decodes a single packet of raw binary data from the radar module.
    The radar packet format is assumed to include:
    - Distance (bytes 4-5, little-endian)
    - Speed (bytes 6-7, little-endian)
    - Signal strength (bytes 8-9, little-endian)
    """
    try:
        if len(raw_data) < 10:  # Ensure the packet is long enough
            return {"Distance (mm)": None, "Speed (mm/s)": None, "Signal Strength": None}

        # Decode distance, speed, and signal strength
        distance = int.from_bytes(raw_data[4:6], byteorder='little', signed=False)
        speed = int.from_bytes(raw_data[6:8], byteorder='little', signed=False)
        signal_strength = int.from_bytes(raw_data[8:10], byteorder='little', signed=False)

        return {
            "Distance (mm)": distance,
            "Speed (mm/s)": speed,
            "Signal Strength": signal_strength,
        }
    except Exception as e:
        print(f"Error decoding packet: {e}")
        return {"Distance (mm)": None, "Speed (mm/s)": None, "Signal Strength": None}

def read_and_decode_data():
    """
    Reads raw binary data from the radar and decodes it into human-readable formats.
    """
    try:
        # Open serial connection
        with serial.Serial(RADAR_PORT, RADAR_BAUDRATE, timeout=1) as ser:
            print(f"Listening on {RADAR_PORT} at {RADAR_BAUDRATE} baud...")
            print("Press Ctrl+C to stop.")

            while True:
                if ser.in_waiting:  # Check if there is data waiting to be read
                    raw_data = ser.read(ser.in_waiting)  # Read all available data
                    hex_output = ' '.join(f'{byte:02x}' for byte in raw_data)  # Format as hex

                    # Decode and print the packet in human-readable format
                    decoded_data = decode_packet(raw_data)
                    print(f"Raw Data (Hex): {hex_output}")
                    print(f"Decoded Data: {decoded_data}")

                time.sleep(0.1)  # Small delay to reduce CPU usage

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped reading data.")

if __name__ == "__main__":
    read_and_decode_data()