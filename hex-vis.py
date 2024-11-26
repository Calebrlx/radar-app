import tkinter as tk
from tkinter import ttk
import serial
import threading
import math
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Radar setup
RADAR_PORT = '/dev/ttyTHS1' 
RADAR_BAUDRATE = 256000
RANGE_MAX = 8.0  # Maximum range in meters

# Conversion factors based on measurements
ANGLE_MAX_VALUE_LEFT = 34000  # Maximum value representing left 60 degrees boundary
ANGLE_MIN_VALUE_LEFT = 32770  # Minimum value representing 0 degrees from left
ANGLE_MAX_VALUE_RIGHT = 2000  # Maximum value representing right 60 degrees
DISTANCE_CONVERSION_FACTOR = 33900  # Value representing 1 meter away
ADDITIONAL_DISTANCE_FACTOR = 800  # Approximate value increment per meter after 1 meter

# Decode packet function
def decode_packet(raw_data):
    """
    Decodes a single target packet of raw binary data from the radar module.
    The radar packet format is assumed to include:
    - Angle (bytes 4-5, little-endian)
    - Distance (bytes 6-7, little-endian)
    - Speed/Trajectory (bytes 8-9, little-endian)
    """
    try:
        if len(raw_data) < 10:
            return None

        # Decode angle, distance, and speed
        angle = int.from_bytes(raw_data[4:6], byteorder='little', signed=False)
        distance = int.from_bytes(raw_data[6:8], byteorder='little', signed=False)
        speed = int.from_bytes(raw_data[8:10], byteorder='little', signed=False)

        # If all values are zero, there's no target
        if angle == 0 and distance == 0 and speed == 0:
            return None

        return {
            "angle": angle,
            "distance": distance,
            "speed": speed,
        }
    except Exception as e:
        print(f"Error decoding packet: {e}")
        return None

# Main App Class
class RadarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radar Visualizer")

        # Setup Serial Connection
        self.serial_connection = serial.Serial(RADAR_PORT, RADAR_BAUDRATE, timeout=1)

        # Radar Plot
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_xlim(-RANGE_MAX, RANGE_MAX)
        self.ax.set_ylim(0, RANGE_MAX)
        self.ax.set_aspect('equal', adjustable='datalim')
        self.ax.set_title("Radar View")
        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.grid(True)

        # Draw range circles
        for r in range(1, int(RANGE_MAX) + 1):
            self.ax.add_artist(plt.Circle((0, 0), r, color='gray', fill=False, linestyle='dashed'))

        # Draw FOV lines
        fov_left = math.radians(-60)
        fov_right = math.radians(60)
        self.ax.plot([0, RANGE_MAX * math.cos(fov_left)], [0, RANGE_MAX * math.sin(fov_left)], color='blue', linestyle='dotted')
        self.ax.plot([0, RANGE_MAX * math.cos(fov_right)], [0, RANGE_MAX * math.sin(fov_right)], color='blue', linestyle='dotted')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, rowspan=2, sticky='nsew')

        # Target List
        self.target_list = ttk.Treeview(self.root, columns=("ID", "Distance", "Angle", "Speed", "Trajectory"))
        self.target_list.heading("#0", text="ID")
        self.target_list.heading("Distance", text="Distance (m)")
        self.target_list.heading("Angle", text="Angle (degree)")
        self.target_list.heading("Speed", text="Speed (units)")
        self.target_list.heading("Trajectory", text="Trajectory")
        self.target_list.column("#0", width=50)
        self.target_list.column("Distance", width=100)
        self.target_list.column("Angle", width=100)
        self.target_list.column("Speed", width=100)
        self.target_list.column("Trajectory", width=150)
        self.target_list.grid(row=0, column=1, sticky='nsew')

        # Raw Data Log
        self.raw_data_text = tk.Text(self.root, wrap=tk.WORD, height=10)
        self.raw_data_text.grid(row=1, column=1, sticky='nsew')

        # Layout Config
        self.root.grid_rowconfigure(0, weight=3)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        # Store target dots
        self.target_dots = []

        # Start Data Updates
        self.update_data_thread = threading.Thread(target=self.update_data)
        self.update_data_thread.daemon = True
        self.update_data_thread.start()

    def update_data(self):
        while True:
            # Read radar data from serial
            if self.serial_connection.in_waiting:
                raw_data = self.serial_connection.read(self.serial_connection.in_waiting)
                target_data = decode_packet(raw_data)

                # Clear existing targets
                self.ax.clear()
                self.ax.set_xlim(-RANGE_MAX, RANGE_MAX)
                self.ax.set_ylim(0, RANGE_MAX)
                self.ax.set_title("Radar View")
                self.ax.grid(True)
                for r in range(1, int(RANGE_MAX) + 1):
                    self.ax.add_artist(plt.Circle((0, 0), r, color='gray', fill=False, linestyle='dashed'))

                # Draw FOV lines
                fov_left = math.radians(-60)
                fov_right = math.radians(60)
                self.ax.plot([0, RANGE_MAX * math.cos(fov_left)], [0, RANGE_MAX * math.sin(fov_left)], color='blue', linestyle='dotted')
                self.ax.plot([0, RANGE_MAX * math.cos(fov_right)], [0, RANGE_MAX * math.sin(fov_right)], color='blue', linestyle='dotted')

                self.target_list.delete(*self.target_list.get_children())

                if target_data:
                    # Convert angle and distance to meters and degrees
                    if target_data["angle"] >= ANGLE_MIN_VALUE_LEFT:
                        angle_proportion = (ANGLE_MAX_VALUE_LEFT - target_data["angle"]) / (ANGLE_MAX_VALUE_LEFT - ANGLE_MIN_VALUE_LEFT)
                        angle_degrees = -60 + (angle_proportion * 60)
                    elif target_data["angle"] <= ANGLE_MAX_VALUE_RIGHT:
                        angle_proportion = target_data["angle"] / ANGLE_MAX_VALUE_RIGHT
                        angle_degrees = angle_proportion * 60
                    else:
                        angle_degrees = 0  # Default to 0 if angle is not in expected range

                    distance_meters = (target_data["distance"] - DISTANCE_CONVERSION_FACTOR) / ADDITIONAL_DISTANCE_FACTOR + 1

                    x = distance_meters * math.cos(math.radians(angle_degrees))
                    y = distance_meters * math.sin(math.radians(angle_degrees))

                    # Add target to list and update plot
                    self.target_dots.append({"x": x, "y": y, "timestamp": time.time()})

                    # Update target list
                    self.target_list.insert("", "end", iid=1, text="1", values=(
                        f"{distance_meters:.2f}",
                        f"{angle_degrees:.2f}",
                        f"{target_data['speed']}",
                        "Approaching" if target_data['speed'] > 0 else "Stationary"
                    ))

                    # Update raw data log
                    raw_data = f"ID: 1, Distance: {distance_meters:.2f} m, Angle: {angle_degrees:.2f} degrees, " \
                               f"Speed: {target_data['speed']}, Trajectory: {'Approaching' if target_data['speed'] > 0 else 'Stationary'}\n"
                    self.raw_data_text.insert(tk.END, raw_data)
                    self.raw_data_text.see(tk.END)

                # Draw fading dots
                current_time = time.time()
                new_target_dots = []
                for dot in self.target_dots:
                    age = current_time - dot["timestamp"]
                    if age < 3:  # Keep dots for 3 seconds
                        alpha = max(0, 1 - age / 3)  # Fade over time
                        self.ax.scatter(dot["x"], dot["y"], color='red', alpha=alpha)
                        new_target_dots.append(dot)
                self.target_dots = new_target_dots

                self.canvas.draw()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = RadarApp(root)
    root.mainloop()
