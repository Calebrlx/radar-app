import tkinter as tk
from tkinter import ttk
import math
import random

# Set up the main application window
app = tk.Tk()
app.title("Advanced Radar Display")
app.geometry("1000x800")
app.configure(bg="#2b2b2b")

# Colors for radar and elements
radar_bg_color = "#1e1e1e"
line_color = "#001f3f"  # Navy blue
tracked_area_color = "#00ffff"  # Cyan
fog_color = "#444444"  # Lighter gray 
target_colors = ["red", "green", "blue", "yellow", "purple", "orange"]

# Sidebar for controls
sidebar = tk.Frame(app, bg="black", width=125)
sidebar.pack(side="left", fill="y")

# Top bar for target list and status
topbar = tk.Frame(app, bg="black", height=125)
topbar.pack(side="top", fill="x")

# Main canvas for radar display
canvas_frame = tk.Frame(app, bg="black")
canvas_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

canvas = tk.Canvas(canvas_frame, bg=radar_bg_color, width=800, height=600)
canvas.pack(expand=True)

# Draw radar semi-circle grid
def draw_radar_grid():
    radar_radius = 300
    center_x, center_y = 400, 300

    # Draw foggy and tracked areas
    canvas.create_arc(
        center_x - radar_radius,
        center_y - radar_radius,
        center_x + radar_radius,
        center_y + radar_radius,
        start=0,
        extent=150,
        outline="",
        fill=fog_color,
    )
    canvas.create_arc(
        center_x - radar_radius,
        center_y - radar_radius,
        center_x + radar_radius,
        center_y + radar_radius,
        start=150,
        extent=30,
        outline="",
        fill=tracked_area_color,
    )

    # Draw arcs
    for r in range(50, radar_radius + 50, 50):
        canvas.create_arc(
            center_x - r,
            center_y - r,
            center_x + r,
            center_y + r,
            start=0,
            extent=180,
            outline=line_color,
            style="arc",
            width=1,
        )

    # Draw lines
    for angle in range(0, 181, 15):
        rad = math.radians(angle)
        x = center_x + radar_radius * math.cos(rad)
        y = center_y + radar_radius * math.sin(rad)
        canvas.create_line(center_x, center_y, x, y, fill=line_color, width=1)

draw_radar_grid()

# Function to generate random targets
def generate_random_targets():
    targets = []
    for _ in range(random.randint(1, 5)):
        distance = random.uniform(50, 300)
        angle = random.uniform(0, 180)
        velocity = random.uniform(0, 10)
        targets.append({"distance": distance, "angle": angle, "velocity": velocity})
    return targets

# Draw targets on the radar
def draw_targets(targets):
    center_x, center_y = 400, 300

    for idx, target in enumerate(targets):
        rad = math.radians(target["angle"])
        x = center_x + target["distance"] * math.cos(rad)
        y = center_y + target["distance"] * math.sin(rad)
        target_circle = canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, fill=target_colors[idx % len(target_colors)], tags="target"
        )
        fade_target(target_circle)

# Fade effect for targets
def fade_target(target_circle):
    for alpha in range(255, 0, -15):
        color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
        canvas.itemconfig(target_circle, fill=color)
        canvas.update()
        app.after(30)

# Update target list and status
def update_target_list(targets):
    for widget in topbar.winfo_children():
        widget.destroy()

    # Target boxes
    for idx, target in enumerate(targets):
        target_frame = tk.Frame(topbar, bg="gray", padx=5, pady=5)
        target_frame.pack(side="left", padx=5, pady=5)

        target_label = tk.Label(
            target_frame,
            text=f"Target {idx + 1}\n"
                 f"Dist: {target['distance']:.1f}m\n"
                 f"Angle: {target['angle']:.1f}°\n"
                 f"Vel: {target['velocity']:.1f}m/s",
            bg="lightgray",
            fg=target_colors[idx % len(target_colors)],
            justify="center",
        )
        target_label.pack()

# Update radar display and targets
def update_display():
    targets = generate_random_targets()
    canvas.delete("target")  # Clear previous targets
    draw_targets(targets)
    update_target_list(targets)
    if running:
        app.after(1000, update_display)

# Start/Stop functionality
running = True

def toggle_simulation():
    global running
    running = not running
    if running:
        update_display()

# Add control buttons
start_button = tk.Button(sidebar, text="Start/Stop", command=toggle_simulation, bg="lightgray")
start_button.pack(pady=10, fill="x")

quit_button = tk.Button(sidebar, text="Quit", command=app.quit, bg="lightgray")
quit_button.pack(pady=10, fill="x")

# Initialize display
update_display()
app.mainloop()
