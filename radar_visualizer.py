import tkinter as tk
from tkinter import ttk
import serial
import threading
import math
import random  # Replace with actual data parsing
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Radar setup
RADAR_PORT = '/dev/ttyTHS1' 
RADAR_BAUDRATE = 256000
RANGE_MAX = 8.0  # Maximum range in meters

# Dummy data function (replace with actual parsing logic)
def parse_radar_data():
    # Simulate target data: (distance, angle, speed, trajectory)
    distance = random.uniform(0, RANGE_MAX)
    angle = random.uniform(0, 360)
    speed = random.uniform(0, 5)
    trajectory = random.choice(["Approaching", "Stationary", "Departing"])
    return {"distance": distance, "angle": angle, "speed": speed, "trajectory": trajectory}

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
        self.ax.set_ylim(-RANGE_MAX, RANGE_MAX)
        self.ax.set_aspect('equal', adjustable='datalim')
        self.ax.set_title("Radar View")
        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.grid(True)

        # Draw range circles
        for r in range(1, int(RANGE_MAX) + 1):
            self.ax.add_artist(plt.Circle((0, 0), r, color='gray', fill=False, linestyle='dashed'))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, rowspan=2, sticky='nsew')

        # Target List
        self.target_list = ttk.Treeview(self.root, columns=("ID", "Distance", "Angle", "Speed", "Trajectory"))
        self.target_list.heading("#0", text="ID")
        self.target_list.heading("Distance", text="Distance (m)")
        self.target_list.heading("Angle", text="Angle (degree)")
        self.target_list.heading("Speed", text="Speed (m/s)")
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

        # Start Data Updates
        self.targets = {}
        self.update_data()

    def update_data(self):
        # Read radar data (replace this block with actual data parsing from serial)
        target_data = parse_radar_data()  # Replace with self.read_serial_data()

        # Update radar plot
        self.ax.clear()
        self.ax.set_xlim(-RANGE_MAX, RANGE_MAX)
        self.ax.set_ylim(-RANGE_MAX, RANGE_MAX)
        self.ax.set_title("Radar View")
        self.ax.grid(True)
        for r in range(1, int(RANGE_MAX) + 1):
            self.ax.add_artist(plt.Circle((0, 0), r, color='gray', fill=False, linestyle='dashed'))

        target_id = len(self.targets) + 1
        x = target_data["distance"] * math.cos(math.radians(target_data["angle"]))
        y = target_data["distance"] * math.sin(math.radians(target_data["angle"]))
        self.ax.scatter(x, y, label=f"ID {target_id}")
        self.ax.legend()

        # Update target list
        self.target_list.insert("", "end", iid=target_id, text=str(target_id), values=(
            f"{target_data['distance']:.2f}",
            f"{target_data['angle']:.2f}",
            f"{target_data['speed']:.2f}",
            target_data['trajectory']
        ))

        # Update raw data log
        raw_data = f"ID: {target_id}, Distance: {target_data['distance']:.2f}, Angle: {target_data['angle']:.2f}, " \
                   f"Speed: {target_data['speed']:.2f}, Trajectory: {target_data['trajectory']}\n"
        self.raw_data_text.insert(tk.END, raw_data)
        self.raw_data_text.see(tk.END)

        self.canvas.draw()

        # Schedule next update
        self.root.after(100, self.update_data)

    def read_serial_data(self):
        if self.serial_connection.in_waiting:
            raw_data = self.serial_connection.readline().decode("utf-8").strip()
            # Parse and return structured data
            return parse_radar_data()  # Replace with actual parsing logic
        return None


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = RadarApp(root)
    root.mainloop()
