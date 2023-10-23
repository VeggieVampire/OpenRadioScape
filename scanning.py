"""
This script performs frequency scanning using the RTL-SDR (Software Defined Radio) device. It reads samples from the SDR, applies Fast Fourier Transform (FFT) to detect peak frequencies, and writes the detected frequencies to a file. The script filters out any detected frequencies that are already known and handles negative frequencies by taking their absolute values before writing to the file. It utilizes the RTLSDR and NumPy libraries for SDR control and signal processing, respectively.

Requirements:
- RTL-SDR device (Software Defined Radio hardware)
- rtlsdr Python package (can be installed via pip)
- NumPy Python package (can be installed via pip)

Make sure to configure the start_frequency, stop_frequency, sample_rate, and OUTPUT_FILE variables according to your requirements before running the script.
"""
import rtlsdr
import numpy as np

# Parameters
start_frequency = 100e6  # 100 MHz
stop_frequency = 200e6  # 200 MHz
sample_rate = 2.048e6  # 2.048 MHz
OUTPUT_FILE = "frequencies.txt"  # File will be created in the same folder as the script

# Create an instance of the RTLSDR class
sdr = rtlsdr.RtlSdr()

# Configure the SDR
sdr.sample_rate = sample_rate
sdr.center_freq = (start_frequency + stop_frequency) / 2

print("Frequency scanner is now running. Press Ctrl+C to stop.")

try:
    known_frequencies = set()
    # Read existing frequencies from the file
    try:
        with open(OUTPUT_FILE, "r") as file:
            known_frequencies = {float(line.strip()) for line in file}
    except FileNotFoundError:
        pass

    while True:
        samples = sdr.read_samples(256 * 1024)
        frequencies = np.fft.fftfreq(len(samples)) * sample_rate
        spectrum = np.fft.fft(samples)
        spectrum = np.abs(spectrum)
        peak_frequency_index = np.argmax(spectrum)
        peak_frequency = np.abs(frequencies[peak_frequency_index])  # Taking absolute value
        if peak_frequency != 0.0 and peak_frequency not in known_frequencies:
            print(f"Detected frequency: {peak_frequency / 1e6} MHz")
            with open(OUTPUT_FILE, "a") as file:
                file.write(f"{peak_frequency}\n")
                known_frequencies.add(peak_frequency)

except KeyboardInterrupt:
    print("Stopped.")

sdr.close()
