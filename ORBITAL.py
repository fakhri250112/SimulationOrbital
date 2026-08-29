import math
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import numpy as np
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "ORBITAL - Missing dependency",
        "Program membutuhkan numpy dan matplotlib.\n\n"
        "Jalankan:\n"
        "pip install -r requirements.txt\n\n"
        f"Detail: {e}"
    )
    raise


class OrbitalSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("ORBITAL 3D Satellite Energy Simulation")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)

        # Simulation state
        self.running = True
        self.angle = 0.0
        self.total_orbits = 0.0
        self.internal_rotation = 0.0
        self.battery = 42.0
        self.beaming = False
        self.last_time = time.perf_counter()

        # User controls
        self.speed_var = tk.DoubleVar(value=1.0)
        self.field_var = tk.BooleanVar(value=True)
        self.auto_laser_var = tk.BooleanVar(value=True)

        self.orbit_radius = 5.0
        self.earth_radius = 2.2
        self.orbit_tilt = math.radians(18)

        self._build_ui()
        self._build_scene()
        self._update_loop()

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=(10, 8))
        top.pack(fill="x")

        title = ttk.Label(
            top,
            text="ORBITAL — 3D Satellite Energy Simulation",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(side="left")

        ttk.Button(
            top,
            text="Reset",
            command=self.reset
        ).pack(side="right", padx=4)

        self.run_button = ttk.Button(
            top,
            text="Pause",
            command=self.toggle_run
        )
        self.run_button.pack(side="right", padx=4)

        main = ttk.Frame(
            self.root,
            padding=(10, 0, 10, 10)
        )
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(main, width=260)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        self.fig = Figure(
            figsize=(8, 7),
            dpi=100
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=left
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # Metric cards
        metrics = ttk.LabelFrame(
            right,
            text="Telemetry",
            padding=10
        )
        metrics.pack(
            fill="x",
            pady=(0, 10)
        )

        self.orbit_label = ttk.Label(
            metrics,
            text="Orbit: 0.00×",
            font=("Segoe UI", 11, "bold")
        )
        self.orbit_label.pack(
            anchor="w",
            pady=2
        )

        self.magnet_label = ttk.Label(
            metrics,
            text="Magnet rotation: 0.00×"
        )
        self.magnet_label.pack(
            anchor="w",
            pady=2
        )

        self.battery_label = ttk.Label(
            metrics,
            text="Battery: 42%",
            font=("Segoe UI", 11, "bold")
        )
        self.battery_label.pack(
            anchor="w",
            pady=2
        )

        self.laser_label = ttk.Label(
            metrics,
            text="Laser: OFF"
        )
        self.laser_label.pack(
            anchor="w",
            pady=2
        )

        self.source_label = ttk.Label(
            metrics,
            text="Power: Solar + Dynamo"
        )
        self.source_label.pack(
            anchor="w",
            pady=2
        )

        # Controls
        controls = ttk.LabelFrame(
            right,
            text="Controls",
            padding=10
        )
        controls.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            controls,
            text="Simulation speed"
        ).pack(anchor="w")

        speed = ttk.Scale(
            controls,
            from_=0.0,
            to=3.0,
            variable=self.speed_var,
            orient="horizontal"
        )

        speed.pack(
            fill="x",
            pady=(2, 4)
        )

        self.speed_label = ttk.Label(
            controls,
            text="1.0×"
        )
        self.speed_label.pack(
            anchor="w",
            pady=(0, 8)
        )

        ttk.Checkbutton(
            controls,
            text="Show magnetic field",
            variable=self.field_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Checkbutton(
            controls,
            text="Auto laser at full battery",
            variable=self.auto_laser_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Button(
            controls,
            text="Set battery to 100%",
            command=self.full_battery
        ).pack(
            fill="x",
            pady=(10, 3)
        )

        # Concept flow
        explanation = ttk.LabelFrame(
            right,
            text="Concept flow",
            padding=10
        )
        explanation.pack(
            fill="x",
            pady=(0, 10)
        )

        text = (
            "1. Satellite orbits Earth.\n"
            "2. Internal magnet is visualized as rotating 1× per orbit.\n"
            "3. Rotation drives a conceptual dynamo.\n"
            "4. Two solar panels add charging power.\n"
            "5. At 100%, laser beams energy to a ground receiver."
        )

        ttk.Label(
            explanation,
            text=text,
            justify="left",
            wraplength=220
        ).pack(anchor="w")

        # Physics note
        note = ttk.LabelFrame(
            right,
            text="Physics note",
            padding=10
        )
        note.pack(fill="x")

        ttk.Label(
            note,
            text=(
                "This is a concept visualization. Earth's magnetic field does "
                "not automatically guarantee one mechanical rotation per orbit. "
                "A real design needs torque, attitude-control, generator-loss, "
                "thermal, laser-pointing, and total energy-balance analysis."
            ),
            justify="left",
            wraplength=220
        ).pack(anchor="w")

    def _build_scene(self):
        self.ax.set_facecolor("#080d17")
        self.fig.patch.set_facecolor("#080d17")

        self.ax.set_xlim(-7, 7)
        self.ax.set_ylim(-7, 7)
        self.ax.set_zlim(-6, 6)

        self.ax.set_box_aspect(
            (1, 1, 0.85)
        )

        self.ax.view_init(
            elev=25,
            azim=40
        )

        self.ax.set_axis_off()

        # Earth
        u = np.linspace(
            0,
            2 * np.pi,
            60
        )

        v = np.linspace(
            0,
            np.pi,
            35
        )

        x = self.earth_radius * np.outer(
            np.cos(u),
            np.sin(v)
        )

        y = self.earth_radius * np.outer(
            np.sin(u),
            np.sin(v)
        )

        z = self.earth_radius * np.outer(
            np.ones_like(u),
            np.cos(v)
        )

        self.ax.plot_surface(
            x,
            y,
            z,
            color="#2e6fb6",
            alpha=0.92,
            linewidth=0,
            antialiased=True,
            shade=True
        )

        # Simple "continents"
        land_pts = [
            (-0.8, 0.7, 1.85),
            (0.6, 1.0, 1.75),
            (1.5, 0.5, 1.2),
            (-1.6, -0.3, 1.25),
            (0.4, -1.35, 1.5)
        ]

        for px, py, pz in land_pts:
            self.ax.scatter(
                [px],
                [py],
                [pz],
                s=180,
                c="#65a15d",
                alpha=0.9
            )

        # N / S labels and dipole axis
        self.ax.text(
            0,
            0,
            2.75,
            "N",
            color="#ff6b6b",
            fontsize=12,
            fontweight="bold",
            ha="center"
        )

        self.ax.text(
            0,
            0,
            -2.85,
            "S",
            color="#6ca5ff",
            fontsize=12,
            fontweight="bold",
            ha="center"
        )

        self.ax.plot(
            [0, 0],
            [0, 0],
            [-2.55, 2.55],
            color="#d9d9d9",
            linewidth=1.0,
            alpha=0.35
        )

        # Orbit
        t = np.linspace(
            0,
            2 * np.pi,
            240
        )

        xo = self.orbit_radius * np.cos(t)
        yo = self.orbit_radius * np.sin(t)
        zo = np.zeros_like(t)

        # Rotate orbit plane around x
        y2 = yo * math.cos(self.orbit_tilt)
        z2 = yo * math.sin(self.orbit_tilt)

        self.ax.plot(
            xo,
            y2,
            z2,
            "--",
            color="#aeb8c6",
            alpha=0.45,
            linewidth=1.1
        )

        # Magnetic field lines
        self.field_lines = []

        for phi in np.linspace(
            0,
            2 * np.pi,
            8,
            endpoint=False
        ):
            tt = np.linspace(
                -1.2,
                1.2,
                100
            )

            rr = 2.65 + 1.65 * (
                np.cos(tt) ** 2
            )

            xf = (
                rr *
                np.cos(phi) *
                np.cos(tt)
            )

            yf = (
                rr *
                np.sin(phi) *
                np.cos(tt)
            )

            zf = 3.1 * np.sin(tt)

            line, = self.ax.plot(
                xf,
                yf,
                zf,
                color="#7aa2ff",
                alpha=0.20,
                linewidth=0.9
            )

            self.field_lines.append(line)

        # Ground receiver
        rv = np.array(
            [1.6, 0.7, 1.45],
            dtype=float
        )

        rv = (
            rv /
            np.linalg.norm(rv) *
            (self.earth_radius + 0.10)
        )

        self.receiver_pos = rv

        self.ax.scatter(
            [rv[0]],
            [rv[1]],
            [rv[2]],
            s=100,
            c="#f4f4f4",
            marker="^",
            depthshade=False
        )

        self.ax.text(
            rv[0],
            rv[1],
            rv[2] + 0.35,
            "Receiver",
            color="white",
            fontsize=8,
            ha="center"
        )

        # Satellite objects
        self.sat_body = self.ax.scatter(
            [],
            [],
            [],
            s=120,
            c="#d0d4da",
            marker="s",
            depthshade=False
        )

        self.panel_left, = self.ax.plot(
            [],
            [],
            [],
            color="#4d75aa",
            linewidth=7
        )

        self.panel_right, = self.ax.plot(
            [],
            [],
            [],
            color="#4d75aa",
            linewidth=7
        )

        self.rotor_line, = self.ax.plot(
            [],
            [],
            [],
            color="#f0bf4a",
            linewidth=4
        )

        self.mag_n = self.ax.scatter(
            [],
            [],
            [],
            s=50,
            c="#e45d5d",
            depthshade=False
        )

        self.mag_s = self.ax.scatter(
            [],
            [],
            [],
            s=50,
            c="#5f8ee4",
            depthshade=False
        )

        self.laser_line, = self.ax.plot(
            [],
            [],
            [],
            color="#ff2b2b",
            linewidth=2.2,
            alpha=0.0
        )

        self.ax.text(
            5.9,
            4.4,
            4.6,
            "☀",
            color="#ffd166",
            fontsize=28
        )

        self.ax.text(
            5.2,
            4.0,
            4.1,
            "Sun",
            color="#ffd166",
            fontsize=8
        )

        self.fig.tight_layout()

    def satellite_position(self, ang):
        x = self.orbit_radius * math.cos(ang)

        y0 = (
            self.orbit_radius *
            math.sin(ang)
        )

        y = (
            y0 *
            math.cos(self.orbit_tilt)
        )

        z = (
            y0 *
            math.sin(self.orbit_tilt)
        )

        return np.array(
            [x, y, z],
            dtype=float
        )

    def _set_scatter_xyz(self, artist, xyz):
        artist._offsets3d = (
            [xyz[0]],
            [xyz[1]],
            [xyz[2]]
        )

    def _update_satellite_artists(self, pos):
        # Satellite tangent direction in orbit
        tangent = np.array([
            -math.sin(self.angle),
            math.cos(self.angle) * math.cos(self.orbit_tilt),
            math.cos(self.angle) * math.sin(self.orbit_tilt)
        ], dtype=float)

        tangent /= np.linalg.norm(tangent)

        radial = (
            pos /
            np.linalg.norm(pos)
        )

        panel_dir = np.cross(
            tangent,
            radial
        )

        if np.linalg.norm(panel_dir) < 1e-6:
            panel_dir = np.array(
                [0, 1, 0],
                dtype=float
            )

        panel_dir /= np.linalg.norm(panel_dir)

        self._set_scatter_xyz(
            self.sat_body,
            pos
        )

        p1 = pos - panel_dir * 1.65
        p2 = pos - panel_dir * 0.55
        p3 = pos + panel_dir * 0.55
        p4 = pos + panel_dir * 1.65

        self.panel_left.set_data(
            [p1[0], p2[0]],
            [p1[1], p2[1]]
        )

        self.panel_left.set_3d_properties(
            [p1[2], p2[2]]
        )

        self.panel_right.set_data(
            [p3[0], p4[0]],
            [p3[1], p4[1]]
        )

        self.panel_right.set_3d_properties(
            [p3[2], p4[2]]
        )

        # Internal magnet
        rot_axis_a = panel_dir
        rot_axis_b = tangent

        r = 0.35

        off = (
            math.cos(self.internal_rotation) *
            rot_axis_a +
            math.sin(self.internal_rotation) *
            rot_axis_b
        ) * r

        mn = pos + off
        ms = pos - off

        self._set_scatter_xyz(
            self.mag_n,
            mn
        )

        self._set_scatter_xyz(
            self.mag_s,
            ms
        )

        self.rotor_line.set_data(
            [mn[0], ms[0]],
            [mn[1], ms[1]]
        )

        self.rotor_line.set_3d_properties(
            [mn[2], ms[2]]
        )

        if self.beaming:
            rv = self.receiver_pos

            self.laser_line.set_data(
                [pos[0], rv[0]],
                [pos[1], rv[1]]
            )

            self.laser_line.set_3d_properties(
                [pos[2], rv[2]]
            )

            self.laser_line.set_alpha(0.95)

        else:
            self.laser_line.set_alpha(0.0)

    def _update_loop(self):
        now = time.perf_counter()

        dt = min(
            now - self.last_time,
            0.05
        )

        self.last_time = now

        speed = self.speed_var.get()

        self.speed_label.config(
            text=f"{speed:.1f}×"
        )

        if self.running:
            d_angle = (
                dt *
                0.50 *
                speed
            )

            self.angle = (
                self.angle +
                d_angle
            ) % (2 * np.pi)

            self.total_orbits += (
                d_angle /
                (2 * np.pi)
            )

            # Concept:
            # 1 magnet rotation per 1 orbit.
            self.internal_rotation += d_angle

            # Conceptual energy model
            solar_factor = max(
                0.0,
                0.55 +
                0.45 *
                math.cos(
                    self.angle - 0.35
                )
            )

            solar_rate = (
                1.0 *
                solar_factor *
                max(speed, 0.15)
            )

            dynamo_rate = (
                0.45 *
                max(speed, 0.15)
            )

            charge_rate = (
                solar_rate +
                dynamo_rate
            )

            # Hysteresis for auto power-beaming
            if (
                self.auto_laser_var.get()
                and not self.beaming
                and self.battery >= 99.8
            ):
                self.beaming = True

            if (
                self.beaming
                and self.battery <= 10.0
            ):
                self.beaming = False

            if self.beaming:
                self.battery -= (
                    dt *
                    5.0 *
                    max(speed, 0.25)
                )
            else:
                self.battery += (
                    dt *
                    charge_rate
                )

            self.battery = min(
                100.0,
                max(0.0, self.battery)
            )

        for line in self.field_lines:
            line.set_visible(
                self.field_var.get()
            )

        pos = self.satellite_position(
            self.angle
        )

        self._update_satellite_artists(
            pos
        )

        self.orbit_label.config(
            text=f"Orbit: {self.total_orbits:.2f}×"
        )

        self.magnet_label.config(
            text=f"Magnet rotation: {self.total_orbits:.2f}×"
        )

        self.battery_label.config(
            text=f"Battery: {self.battery:.0f}%"
        )

        self.laser_label.config(
            text=(
                "Laser: ON → Earth"
                if self.beaming
                else "Laser: OFF"
            )
        )

        self.canvas.draw_idle()

        self.root.after(
            33,
            self._update_loop
        )

    def toggle_run(self):
        self.running = not self.running

        self.run_button.config(
            text=(
                "Pause"
                if self.running
                else "Resume"
            )
        )

        self.last_time = time.perf_counter()

    def reset(self):
        self.angle = 0.0
        self.total_orbits = 0.0
        self.internal_rotation = 0.0
        self.battery = 42.0
        self.beaming = False

        self.speed_var.set(1.0)

        self.running = True

        self.run_button.config(
            text="Pause"
        )

        self.last_time = time.perf_counter()

    def full_battery(self):
        self.battery = 100.0


if __name__ == "__main__":
    root = tk.Tk()
    app = OrbitalSimulation(root)
    root.mainloop()
