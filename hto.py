import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Gravitational Parameters for common planets (in km³/s²)
GRAVITATIONAL_PARAMS = {
    "Sun": 1.32712440018e11,
    "Mercury": 2.20320e4,
    "Venus": 3.24859e5,
    "Earth": 3.986004418e5,
    "Moon": 4.9048695e3,
    "Mars": 4.282837e4,
    "Ceres": 6.26325e1,
    "Jupiter": 1.26686534e8,
    "Saturn": 3.7931187e7,
    "Uranus": 5.793939e6,
    "Neptune": 6.836529e6,
    "Pluto": 8.71e2,
    "Eris": 1.108e3
}

def calculate_and_plot():
    try:
        # Get user inputs
        central_body = central_body_var.get()
        mu = GRAVITATIONAL_PARAMS[central_body]
        R1 = float(entry_r1.get())
        R2 = float(entry_r2.get())
        unit = unit_var.get()

        # Conversion factor
        AU_to_km = 1.496e8  # 1 AU in km

        if unit == "AU":
            R1_km = R1 * AU_to_km
            R2_km = R2 * AU_to_km
        else:
            R1_km = R1
            R2_km = R2

        # Semi-major axis of the transfer orbit
        a_transfer = (R1_km + R2_km) / 2

        # Time of flight (Hohmann transfer time)
        T_transfer = np.pi * np.sqrt(a_transfer ** 3 / mu)
        T_transfer_days = T_transfer / (60 * 60 * 24)

        # Display time of flight
        result_label.config(text=f"Time of flight: {T_transfer_days:.2f} days")

        # Generate orbits for visualization
        theta = np.linspace(0, 2 * np.pi, 500)
        x_inner = R1_km / AU_to_km * np.cos(theta) if unit == "AU" else R1 * np.cos(theta)
        y_inner = R1_km / AU_to_km * np.sin(theta) if unit == "AU" else R1 * np.sin(theta)

        x_outer = R2_km / AU_to_km * np.cos(theta) if unit == "AU" else R2 * np.cos(theta)
        y_outer = R2_km / AU_to_km * np.sin(theta) if unit == "AU" else R2 * np.sin(theta)

        r_transfer = a_transfer * (1 - (R2_km - R1_km) / (R2_km + R1_km) * np.cos(theta))
        x_transfer = r_transfer / AU_to_km * np.cos(theta) if unit == "AU" else r_transfer * np.cos(theta)
        y_transfer = r_transfer / AU_to_km * np.sin(theta) if unit == "AU" else r_transfer * np.sin(theta)

        ax.clear()
        ax.plot(x_inner, y_inner, label="Inner Orbit (R1)", color="blue")
        ax.plot(x_outer, y_outer, label="Outer Orbit (R2)", color="green")
        ax.plot(x_transfer, y_transfer, label="Hohmann Transfer", color="red")
        ax.scatter(0, 0, color="yellow", label=f"Central Body ({central_body})", s=100)

        ax.set_xlabel("X (AU)" if unit == "AU" else "X (km)")
        ax.set_ylabel("Y (AU)" if unit == "AU" else "Y (km)")
        ax.set_title(f"Hohmann Transfer Orbit around {central_body}")

        max_radius = max(R1, R2)
        buffer_factor = 0.05
        buffer = max_radius * buffer_factor
        ax.set_xlim(-max_radius - buffer, max_radius + buffer)
        ax.set_ylim(-max_radius - buffer, max_radius + buffer)
        ax.set_aspect('equal')

        ax.legend(loc='upper right', fontsize=5)

        canvas.draw()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for R1 and R2.")

# Create the main window
root = tk.Tk()
root.title("Hohmann Transfer Orbit Calculator")

# Input fields for central body and its gravitational parameter
tk.Label(root, text="Select Central Body:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
central_body_var = tk.StringVar(value="Sun")
central_body_selector = ttk.Combobox(root, textvariable=central_body_var, values=list(GRAVITATIONAL_PARAMS.keys()))
central_body_selector.grid(row=0, column=1, padx=10, pady=5)

# Input fields for radii and unit selection
tk.Label(root, text="Radius of Inner Orbit:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_r1 = tk.Entry(root)
entry_r1.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Radius of Outer Orbit:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_r2 = tk.Entry(root)
entry_r2.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Unit:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
unit_var = tk.StringVar(value="AU")
unit_selector = ttk.Combobox(root, textvariable=unit_var, values=["AU", "km"])
unit_selector.grid(row=3, column=1, padx=10, pady=5)

# Result label
result_label = tk.Label(root, text="Time of flight: N/A", font=("Arial", 12), fg="blue")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Button to calculate and plot
btn_calculate = tk.Button(root, text="Calculate and Visualize", command=calculate_and_plot)
btn_calculate.grid(row=5, column=0, columnspan=2, pady=10)

fig, ax = plt.subplots(figsize=(4, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()