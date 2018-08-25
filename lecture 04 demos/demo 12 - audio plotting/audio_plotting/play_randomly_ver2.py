# play_randomly_ver2.py
# Like play_randomly.py, but uses 4th order filter insead of 2nd order filter
"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
It sounds like pings from a Sonar or from a Geiger Counter.
Gerald Schuller, March 2015 
"""

import pyaudio
import struct
import random
from math import sin, cos, pi
from myfunctions import clip16
from matplotlib import pyplot as plt

BLOCKSIZE = 1024    # Blocksize
WIDTH = 2       # Bytes per sample
CHANNELS = 1
RATE = 44100    # Sampling Rate in Hz
RATE = 8000

# Parameters
T = 10       # Total play time (seconds)
Ta = 1.4    # Decay time (seconds)
f1 = 300    # Frequency (Hz)

# Pole radius and angle
r1 = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

r2 = 0.8 * r1           # smaller pole radius for section 2

# Filter coefficients - SOS 1
a11 = -2*r1*cos(om1)
a12 = r1**2;

# Filter coefficients - SOS 2
a21 = -2*r2*cos(om1)
a22 = r2**2;

NumBlocks = int(T * RATE / BLOCKSIZE)

y1 = [0 for i in range(BLOCKSIZE)]
y2 = [0 for i in range(BLOCKSIZE)]
output = [0 for i in range(BLOCKSIZE)]

# Open the audio output stream
p = pyaudio.PyAudio()
stream = p.open(
    format = p.get_format_from_width(WIDTH),
    channels = CHANNELS,
    rate = RATE,
    input = False,
    output = True,
    frames_per_buffer = BLOCKSIZE)

print('Playing for {0:f} seconds ...'.format(T))

# Loop through blocks
for i in range(0, NumBlocks):
    # print i

    # Do difference equation for block
    for n in range(BLOCKSIZE):

        rand_val = random.random()
        if rand_val < 0.0004:
            x = 300
        else:
            x = 0

        # Easy way: define two vectors y1 and y2
        y1[n] = x - a11 * y1[n-1] - a12 * y1[n-2]
        y2[n] = y1[n] - a21 * y2[n-1] - a22 * y2[n-2]

    for n in range(BLOCKSIZE):
        output[n] = int( clip16( y2[n] ))

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *output);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print('* Finished.')

stream.stop_stream()
stream.close()
p.terminate()

