import serial
import time

# Configuration for the radar module
RADAR_PORT = '/dev/ttyTHS1' 
RADAR_BAUDRATE = 256000

def decode_packet(raw_data):
    """
    Decodes a single packet of raw binary data from the radar module.
    The radar packet format is assumed to include:
    - Angle (bytes 4-5, little-endian)
    - Distance (bytes 6-7, little-endian)
    - Speed/Trajectory (bytes 8-9, little-endian)
    """
    try:
        if len(raw_data) < 10:  # Ensure the packet is long enough
            return {"Angle": None, "Distance (mm)": None, "Speed (mm/s)": None}

        # Decode angle, distance, and speed
        angle = int.from_bytes(raw_data[4:6], byteorder='little', signed=False)
        distance = int.from_bytes(raw_data[6:8], byteorder='little', signed=False)
        speed = int.from_bytes(raw_data[8:10], byteorder='little', signed=False)

        return {
            "Angle": angle,
            "Distance (mm)": distance,
            "Speed (mm/s)": speed,
        }
    except Exception as e:
        print(f"Error decoding packet: {e}")
        return {"Angle": None, "Distance (mm)": None, "Speed (mm/s)": None}

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
                    # print(f"Raw Data (Hex): {hex_output}")
                    print(f"Decoded Data: {decoded_data}")

                time.sleep(0.1)  # Small delay to reduce CPU usage

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped reading data.")

if __name__ == "__main__":
    read_and_decode_data()