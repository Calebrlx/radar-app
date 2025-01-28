import serial
import struct

# Configure the serial connection
serial_port = '/dev/ttyTHS1' 
baud_rate = 256000

# Open serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def parse_frame(frame):
    # Verify header and tail
    if frame[:4] != b'\xAA\xFF\x03\x00' or frame[-2:] != b'\x55\xCC':
        print("Invalid frame")
        return None

    # Extract target data (max 3 targets)
    targets = []
    for i in range(3):
        offset = 4 + i * 8
        if offset + 8 > len(frame):
            break

        # Parse target data
        x, y, speed, distance = struct.unpack('<hhhi', frame[offset:offset + 8])

        # Convert values
        x = x if x < 32768 else x - 65536
        y = y if y < 32768 else y - 65536
        speed = speed if speed < 32768 else speed - 65536

        # Append parsed target
        targets.append({
            "Target ID": i + 1,
            "X (mm)": x,
            "Y (mm)": y,
            "Speed (cm/s)": speed,
            "Distance (mm)": distance
        })

    return targets

def main():
    print("Listening for RD-03D data...")
    buffer = b''

    try:
        while True:
            # Read incoming data
            buffer += ser.read(1024)

            # Look for valid frame (header and tail)
            while b'\xAA\xFF\x03\x00' in buffer and b'\x55\xCC' in buffer:
                start = buffer.find(b'\xAA\xFF\x03\x00')
                end = buffer.find(b'\x55\xCC', start) + 2
                frame = buffer[start:end]

                # Parse and display frame
                targets = parse_frame(frame)
                if targets:
                    for target in targets:
                        print(target)

                # Remove processed frame from buffer
                buffer = buffer[end:]

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()