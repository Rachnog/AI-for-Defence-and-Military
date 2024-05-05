import streamlit as st
from radar_simulation import RadarSimulation  # Ensure this is your radar simulation module
from spectrometer_simulation import SpectrometerSimulation  # Ensure this is your spectrometer simulation module
import plotly.graph_objects as go
import numpy as np
from seismic_simulation import SeismicSimulation  # Ensure this is your seismic simulation module

def main():
    st.title("Raders and Sensors Simulation")
    tab1, tab2, tab3 = st.tabs(["Radar Simulation", "Spectrometer Simulation", "Laser Simulation"])

    with tab1:
        radar_simulation()

    with tab2:
        spectrometer_simulation()

    with tab3:
        seismic_simulation()

def radar_simulation():
    st.subheader("Radar Data Simulation")
    radar_range = st.number_input("Radar Range (meters)", 50, 200, 100, key='radar_range')
    radar_frequency = st.number_input("Radar Frequency (GHz)", 1.0, 20.0, 10.0, key='radar_freq')
    time_steps = st.number_input("Number of Time Steps", min_value=10, max_value=100, value=50, key='time_steps')
    loop_frequency = st.number_input("Drone Loop Frequency", 0.01, 0.5, 0.1, key='loop_freq')

    radar = RadarSimulation(radar_position=[0, 0], radar_range=radar_range, radar_frequency=radar_frequency)
    radar.add_target("missile", [50, 80], [-2, -6], rcs=1.0)
    radar.add_target("drone", [20, -50], [-5, 0], rcs=0.5)
    radar.add_target("plane", [70, 0], [-5, 0], rcs=2.0)

    if st.button("Run Radar Simulation"):
        radar.run_simulation(time_steps, dt=1, loop_frequency=loop_frequency)
        data = radar.get_simulation_data()
        plot_radar_results(data)

def plot_radar_results(data):
    # Radar target movement plot
    fig = go.Figure()
    for name, values in data['positions'].items():
        x, y = zip(*values) if values else ([], [])
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=name))
    fig.update_layout(title='Radar Target Movement', xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', legend_title='Targets')
    st.plotly_chart(fig, use_container_width=True)

    # Additional plots for Doppler Shifts, SNR, and RSSI
    metrics = ['doppler_shifts', 'snr_values', 'rssi_values']
    titles = ["Doppler Shifts", "Signal-to-Noise Ratio (SNR)", "RSSI (dBm)"]
    units = ['Hz', '', 'dBm']
    
    for metric, title, unit in zip(metrics, titles, units):
        fig = go.Figure()
        for name, values in data[metric].items():
            fig.add_trace(go.Scatter(y=values, mode='lines+markers', name=name))
        fig.update_layout(title=title, xaxis_title="Time Step", yaxis_title=f"{title} ({unit})", legend_title="Targets")
        st.plotly_chart(fig, use_container_width=True)

def spectrometer_simulation():
    st.subheader("Spectrometer Data Simulation")
    sim = SpectrometerSimulation()

    # Pre-defined characteristics for different events
    event_types = ['APFSDS launch', 'HE projectile launch', 'RPG launch', 'TNT explosion']
    event_name = st.selectbox("Event Type", event_types, key="event_type")
    center_time = st.number_input("Center Time (ms)", 0, 100, 20, key="center_time")
    rise_time = st.number_input("Rise Time (ms)", 1, 20, 2, key="rise_time")
    fall_time = st.number_input("Fall Time (ms)", 1, 30, 10, key="fall_time")
    peak_amplitude = st.number_input("Peak Amplitude (a.u.)", 1, 100, 80, key="peak_amplitude")

    # Set the characteristics based on user inputs
    sim.set_characteristics({
        event_name: {
            'center_time': center_time,
            'rise_time': rise_time,
            'fall_time': fall_time,
            'peak_amplitude': peak_amplitude
        }
    })

    if st.button("Update and Visualize Spectrometer Characteristics"):
        time_ms, emissions = sim.generate_data()
        plot_spectrometer_results(time_ms, emissions)

def plot_spectrometer_results(time_ms, emissions):
    fig = go.Figure()
    for event, emission in emissions.items():
        fig.add_trace(go.Scatter(x=time_ms, y=emission, mode='lines', name=event))
    fig.update_layout(title='Spectrometer Emissions', xaxis_title='Time [ms]', yaxis_title='Normalized power [a.u.]', legend_title='Events')
    st.plotly_chart(fig, use_container_width=True)

def seismic_simulation():
    st.subheader("Seismic Response Simulation")
    frequencies = np.linspace(50, 1500, 1451)
    seismic = SeismicSimulation(frequencies)
    soil_impact_on = st.slider("Soil Impact on Mine", 0.0, 1.0, 0.1)
    noise_level_on = st.slider("Noise Level on Mine", 0.0, 0.01, 0.001, step=0.0001)
    soil_impact_off = st.slider("Soil Impact off Mine", 0.0, 1.0, 0.5)
    noise_level_off = st.slider("Noise Level off Mine", 0.0, 0.01, 0.002, step=0.0001)

    if st.button("Run Seismic Simulation"):
        results = seismic.generate_data(soil_impact_on, noise_level_on, soil_impact_off, noise_level_off)
        plot_seismic_results(frequencies, results)

def plot_seismic_results(frequencies, results):
    for mine, (on_response, off_response) in results.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=frequencies, y=on_response, mode='lines', name='Laser on Mine', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=frequencies, y=off_response, mode='lines', name='Laser off Mine', line=dict(dash='dash', color='black')))
        fig.update_layout(title=f'{mine} Mine Response', xaxis_title='Frequency (Hz)', yaxis_title='Velocity (nm/sec)')
        st.plotly_chart(fig, use_container_width=True)



if __name__ == "__main__":
    main()