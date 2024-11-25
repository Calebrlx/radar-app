import serial
import struct
import time
import curses


# Radar constants
RADAR_PORT = '/dev/ttyTHS1'  # Update with your Jetson Nano UART port
RADAR_BAUDRATE = 256000

# Frame markers
FRAME_HEADER = b'\xF1\xF2\xF3\xF4'  # Data frame header
FRAME_TRAILER = b'\xF5\xF6\xF7\xF8'  # Data frame trailer


def parse_frame(data):
    """
    Parse the incoming radar frame.
    """
    try:
        if data.startswith(FRAME_HEADER) and data.endswith(FRAME_TRAILER):
            # Extract frame data (example structure, adjust based on documentation)
            target_state = data[6]
            target_range = struct.unpack('<H', data[7:9])[0]
            range_energy = struct.unpack('<16H', data[9:41])

            return {
                "target_state": target_state,
                "target_range": target_range,
                "range_energy": range_energy,
            }
        else:
            return None
    except Exception as e:
        return {"error": str(e)}


def radar_read_loop(serial_connection, stdscr):
    """
    Main loop to read data from the radar and display it in a TUI.
    """
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.border(0)

    stdscr.addstr(1, 2, "Ai-Thinker RD-03 Radar TUI")
    stdscr.addstr(2, 2, f"Listening on {RADAR_PORT} at {RADAR_BAUDRATE} baud")
    stdscr.refresh()

    while True:
        try:
            # Check for user input to exit
            key = stdscr.getch()
            if key == ord('q'):
                break

            if serial_connection.in_waiting:
                raw_data = serial_connection.read(43)  # Example length of frame
                frame_data = parse_frame(raw_data)

                stdscr.clear()
                stdscr.border(0)
                stdscr.addstr(1, 2, "Ai-Thinker RD-03 Radar TUI")
                stdscr.addstr(2, 2, f"Listening on {RADAR_PORT} at {RADAR_BAUDRATE} baud")

                if frame_data:
                    if "error" in frame_data:
                        stdscr.addstr(4, 2, f"Error: {frame_data['error']}")
                    else:
                        stdscr.addstr(4, 2, f"Target State: {frame_data['target_state']}")
                        stdscr.addstr(5, 2, f"Target Range: {frame_data['target_range']} cm")
                        stdscr.addstr(6, 2, f"Range Energy: {frame_data['range_energy']}")
                else:
                    stdscr.addstr(4, 2, "No valid frame received.")

                stdscr.addstr(8, 2, "Press 'q' to quit.")
                stdscr.refresh()

            time.sleep(0.1)

        except Exception as e:
            stdscr.addstr(10, 2, f"Error: {str(e)}")
            stdscr.refresh()
            time.sleep(1)


def main():
    """
    Entry point for the TUI application.
    """
    try:
        # Initialize serial connection
        serial_connection = serial.Serial(
            port=RADAR_PORT,
            baudrate=RADAR_BAUDRATE,
            timeout=1
        )
        curses.wrapper(radar_read_loop, serial_connection)

    except serial.SerialException as e:
        print(f"Failed to connect to the radar module: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
