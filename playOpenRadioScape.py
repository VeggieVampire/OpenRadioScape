import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg
from scipy import signal
from sklearn import preprocessing
from rtlsdr import RtlSdr
import pygame
import pygame.freetype
import tkinter as tk

# Initialize pygame
pygame.init()

# Set the window size and title
window_size = (600, 400)
window_title = 'Signal Analyzer'

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_title)

# Set the font and font size
font = pygame.freetype.Font(None, 24)

# Set the SDR sample rate and frequency
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # 2.4 MHz
sdr.center_freq = 100e6  # 100 MHz

# Set the number of samples to capture
num_samples = 2**15

def main():
    # Set the background color
    screen.fill((255, 255, 255))

    # Draw the signal type selection buttons
    fsk_button = pygame.Rect(50, 50, 200, 50)
    qam_button = pygame.Rect(300, 50, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), fsk_button)
    pygame.draw.rect(screen, (200, 200, 200), qam_button)
    font.render_to(screen, (80, 70), 'FSK', (0, 0, 0))
    font.render_to(screen, (330, 70), 'QAM', (0, 0, 0))

    # Update the display
    pygame.display.flip()

    # Wait for a button to be clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Check if the FSK button was clicked
                if fsk_button.collidepoint(mouse_pos):
                    # Read samples from the SDR
                    samples = sdr.read_samples(num_samples)

                    # Estimate the symbol rate of the FSK signal using the autocorrelation function
                    autocorr = signal.correlate(samples, samples, mode='full')
                    autocorr = autocorr[autocorr.size//2:]
                    autocorr /= np.max(autocorr)
                    symbols_per_second = sdr.sample_rate / signal.argmax(autocorr)
                    print(f'Estimated symbol rate: {sy
