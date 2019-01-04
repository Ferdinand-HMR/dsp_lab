# play_randomly_ver2_plots.py
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
WIDTH = 2           # Bytes per sample
CHANNELS = 1
RATE = 8000        # Sampling Rate in Hz

# Parameters
T = 10       # Total play time (seconds)
Ta = 0.4    # Decay time (seconds)
f1 = 600    # Frequency (Hz)

# Pole radius and angle
r1 = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

r2 = 0.95 * r1           # smaller pole radius for section 2

# r2 = r1

# Filter coefficients - SOS 1
a11 = -2*r1*cos(om1)
a12 = r1**2
b10 = sin(om1)

# Filter coefficients - SOS 2
a21 = -2*r2*cos(om1)
a22 = r2**2
b20 = sin(om1)

# Cancel SOS 2
# a21 = 0
# a22 = 0
# b20 = 1

NumBlocks = int( T * RATE / BLOCKSIZE )

y1 = [0 for i in range(BLOCKSIZE)]
y2 = [0 for i in range(BLOCKSIZE)]
output = [0 for i in range(BLOCKSIZE)]

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = False,
    output = True,
    frames_per_buffer = BLOCKSIZE)

print('Playing for {0:f} seconds ...'.format(T))

plt.ion()           # Turn on interactive mode so plot gets updated

fig = plt.figure(1)
line, = plt.plot(y2)
plt.ylim(-32000, 32000)
plt.xlim(0, BLOCKSIZE)
plt.show()


# Loop through blocks
for i in range(0, NumBlocks):
    # print i

    # Do difference equation for block
    for n in range(BLOCKSIZE):

        rand_val = random.random()
        if rand_val < 0.0005:
            x = 5000 * (random.random() - 0.5)
        else:
            x = 0

        # Easy way: define two vectors y1 and y2
        y1[n] = b10 * x - a11 * y1[n-1] - a12 * y1[n-2]
        y2[n] = b20 * y1[n] - a21 * y2[n-1] - a22 * y2[n-2]

    for n in range(BLOCKSIZE):
        output[n] = int( clip16( y2[n] ))

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *output);

    line.set_ydata(output)
    plt.pause(0.001)
    plt.draw()

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *output);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print('* Finished.')

stream.stop_stream()
stream.close()
p.terminate()

