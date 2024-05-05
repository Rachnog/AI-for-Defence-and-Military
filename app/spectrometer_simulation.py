import numpy as np

class SpectrometerSimulation:
    def __init__(self):
        self.time_ms = np.linspace(0, 100, 1000)

    def set_characteristics(self, characteristics):
        self.characteristics = characteristics

    def simulate_emission(self, time, center_time, rise_time, fall_time, peak_amplitude):
        rise_phase = np.exp(-((time - center_time + rise_time / 2)**2 / (2 * rise_time**2)))
        fall_phase = np.exp(-((time - center_time - fall_time / 2) / fall_time))
        emission = np.where(time < center_time, peak_amplitude * rise_phase, peak_amplitude * fall_phase)
        emission = np.clip(emission / np.max(emission) * peak_amplitude, 0, None)
        return emission

    def generate_data(self):
        emissions = {event: self.simulate_emission(self.time_ms, **params) for event, params in self.characteristics.items()}
        return self.time_ms, emissions