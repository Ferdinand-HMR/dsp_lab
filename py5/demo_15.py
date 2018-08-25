# play_keys.py

"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
Gerald Schuller, March 2015
Modified - Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import pygame
import numpy as np
from math import sin, cos, pi

BLOCKSIZE = 16  # Number of frames per block
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Mono
RATE = 16000  # Frames per second

alpha = float(2 ** (1/float(12)))
f0 = 440
# print alpha

MAXVALUE = 2 ** 15 - 1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 10  # Decay time (seconds)
f1 = 300  # Frequency (Hz)

# Pole radius and angle
r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1) / RATE

# Filter coefficients (second-order IIR)
a1 = -2 * r * cos(om1)
a2 = r ** 2
b0 = sin(om1)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
    format=PA_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=128)
# specify low frames_per_buffer to reduce latency

# w = 0

pygame.init()  # Initializes pygame

print("Press keys for sound. Press 'q' to quit.")
print("OK go...")

y = np.zeros(BLOCKSIZE)
x = np.zeros(BLOCKSIZE)

stop = False

while stop == False:

    x[0] = 0.0

    for event in pygame.event.get():

        # Any key press counts as playing a note
        if event.type == pygame.KEYDOWN:

            if event.key > 100:
                locate = event.key - 110
            else:
                locate = event.key - 50


            x[0] = 15000
            # f1 = 440 * (locate)  # Frequency (Hz)
            f1 = float(alpha ** locate * 440)
            print locate
            print "sound frequency: ",f1


            # Pole radius and angle
            r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
            om1 = 2.0 * pi * float(f1) / RATE

            a1 = -2 * r * cos(om1)
            a2 = r ** 2
            b0 = sin(om1)

            # print om1
            # w = 2 * pi * alpha ** (event.key) * f0/RATE
            # x[0] = 15000 * cos(w)
        # Quit if user presses 'q'
        if event.key == pygame.K_q:
            stop = True

    # Do difference equation for block
    # print x
    for n in range(BLOCKSIZE):


        # w = 2 * pi * alpha ** (pygame.event.key) * f0 / RATE
        # print w
        # x[n] = 15000 * cos(w)
        print x[n]
        y[n] = b0 * x[n] - a1 * y[n - 1] - a2 * y[n - 2]
        # y[n] = alpha ** (event.key) * f0
        # What happens when n = 0?
        # In Python negative indices cycle to end, so it works..

    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)  # Clipping

    # Convert numeric list to binary string

    data = struct.pack('h' * BLOCKSIZE, *y);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

pygame.quit()
