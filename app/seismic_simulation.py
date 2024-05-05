import numpy as np

class SeismicSimulation:
    def __init__(self, frequencies):
        self.frequencies = frequencies
        self.mine_characteristics = {
            'M19': [(300, 0.02, 100), (450, 0.01, 150)],
            'VS2.2': [(250, 0.015, 120)],
            'VS50': [(1000, 0.03, 50), (1250, 0.025, 80)],
            'TS50': [(850, 0.035, 90), (950, 0.02, 100)]
        }

    def simulate_seismic_response(self, mine_info, soil_impact):
        response = np.zeros_like(self.frequencies)
        for resonance_freq, intrinsic_amplitude, intrinsic_width in mine_info:
            affected_amplitude = intrinsic_amplitude * (1 - soil_impact)
            response += affected_amplitude * np.exp(-((self.frequencies - resonance_freq) ** 2) / (2 * intrinsic_width ** 2))
        return response

    def add_environmental_noise(self, signal, noise_level):
        return signal + np.random.normal(0, noise_level, len(signal))

    def generate_data(self, soil_impact_on, noise_level_on, soil_impact_off, noise_level_off):
        results = {}
        for mine, characteristics in self.mine_characteristics.items():
            on_mine_response = self.simulate_seismic_response(characteristics, soil_impact_on)
            off_mine_response = self.simulate_seismic_response([(freq, amp*0.1, width) for freq, amp, width in characteristics], soil_impact_off)

            on_mine_response = self.add_environmental_noise(on_mine_response, noise_level_on)
            off_mine_response = self.add_environmental_noise(off_mine_response, noise_level_off)
            results[mine] = (on_mine_response, off_mine_response)
        return results
