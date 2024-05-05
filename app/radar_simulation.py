import numpy as np

class Target:
    def __init__(self, position, velocity, rcs):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.rcs = rcs  # Radar Cross Section

class RadarSimulation:
    def __init__(self, radar_position, radar_range, radar_frequency, c=3e8):
        self.radar_position = np.array(radar_position)
        self.radar_range = radar_range
        self.radar_frequency = radar_frequency * 1e9  # Convert GHz to Hz
        self.c = c  # Speed of light in m/s
        self.targets = {}
        self.positions = {}
        self.doppler_shifts = {}
        self.snr_values = {}
        self.rssi_values = {}

    def add_target(self, name, position, velocity, rcs):
        target = Target(position, velocity, rcs)
        self.targets[name] = target
        self.positions[name] = []
        self.doppler_shifts[name] = []
        self.snr_values[name] = []
        self.rssi_values[name] = []

    def run_simulation(self, time_steps, dt, loop_frequency=0.1):
        for step in range(time_steps):
            # Example specific behavior: Drone makes loops
            if "drone" in self.targets:
                self.targets["drone"].velocity[1] = 10 * np.sin(loop_frequency * step)

            for name, target in self.targets.items():
                target.position += target.velocity * dt
                distance = np.linalg.norm(target.position - self.radar_position)

                if distance != 0:
                    relative_velocity = np.dot(target.velocity, target.position - self.radar_position) / distance
                    doppler_shift = self.radar_frequency * (relative_velocity / self.c)
                    signal_strength = target.rcs / (distance ** 2)
                else:
                    relative_velocity = 0
                    doppler_shift = 0
                    signal_strength = np.inf

                noise = 1e-3
                snr = signal_strength / noise if distance != 0 else np.inf
                rssi = (target.rcs * signal_strength * self.radar_frequency) / (distance ** 2) if distance != 0 else np.inf
                rssi_dBm = 10 * np.log10(rssi / 1e-3) if rssi > 0 else -np.inf

                self.positions[name].append(target.position.tolist() if distance <= self.radar_range else [np.nan, np.nan])
                self.doppler_shifts[name].append(doppler_shift if distance <= self.radar_range else np.nan)
                self.snr_values[name].append(snr if distance <= self.radar_range else np.nan)
                self.rssi_values[name].append(rssi_dBm if distance <= self.radar_range else np.nan)

    def get_simulation_data(self):
        return {
            "positions": self.positions,
            "doppler_shifts": self.doppler_shifts,
            "snr_values": self.snr_values,
            "rssi_values": self.rssi_values
        }