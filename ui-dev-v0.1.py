import tkinter as tk
from tkinter import ttk
import math
import random

# Set up the main application window
app = tk.Tk()
app.title("Radar Display")
app.geometry("800x600")

# Colors for tracking dots
colors = ["red", "green", "blue", "yellow", "purple", "orange"]

# Sidebar for controls and target list
sidebar = tk.Frame(app, bg="lightgray", width=200)
sidebar.pack(side="left", fill="y")

# Main canvas for radar display
canvas = tk.Canvas(app, bg="black", width=600, height=600)
canvas.pack(side="right", fill="both", expand=True)

# Draw radar semi-circle grid
def draw_radar_grid():
    radar_radius = 250
    center_x, center_y = 300, 300

    # Draw arcs
    for r in range(50, radar_radius + 50, 50):
        canvas.create_arc(
            center_x - r,
            center_y - r,
            center_x + r,
            center_y + r,
            start=-90,
            extent=180,
            outline="white",
            style="arc",
        )

    # Draw lines
    for angle in range(-90, 91, 15):
        rad = math.radians(angle)
        x = center_x + radar_radius * math.cos(rad)
        y = center_y + radar_radius * math.sin(rad)
        canvas.create_line(center_x, center_y, x, y, fill="white")

draw_radar_grid()

# Function to generate random targets for simulation
def generate_random_targets():
    targets = []
    for _ in range(random.randint(1, 5)):
        distance = random.uniform(50, 250)
        angle = random.uniform(-90, 90)
        velocity = random.uniform(0, 10)
        targets.append({"distance": distance, "angle": angle, "velocity": velocity})
    return targets

# Draw targets on the radar
def draw_targets(targets):
    canvas.delete("target")  # Remove previous targets
    center_x, center_y = 300, 300

    for idx, target in enumerate(targets):
        rad = math.radians(target["angle"])
        x = center_x + target["distance"] * math.cos(rad)
        y = center_y + target["distance"] * math.sin(rad)
        canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, fill=colors[idx % len(colors)], tags="target"
        )

# Update sidebar with target list
def update_target_list(targets):
    for widget in sidebar.winfo_children():
        widget.destroy()

    # Title
    title = tk.Label(sidebar, text="Target List", bg="lightgray", font=("Arial", 14))
    title.pack(pady=10)

    # Target information
    for idx, target in enumerate(targets):
        label = tk.Label(
            sidebar,
            text=f"Target {idx + 1}\n"
                 f"Distance: {target['distance']:.2f} m\n"
                 f"Angle: {target['angle']:.2f}°\n"
                 f"Velocity: {target['velocity']:.2f} m/s",
            bg="lightgray",
            fg=colors[idx % len(colors)],
            justify="left",
            font=("Arial", 10),
        )
        label.pack(pady=5, anchor="w")

# Update radar display and target list
def update_display():
    targets = generate_random_targets()
    draw_targets(targets)
    update_target_list(targets)
    app.after(1000, update_display)  # Refresh every second

# Initialize the display
update_display()

app.mainloop()