# play_randomly_plots.py
"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
It sounds like pings from a Sonar or from a Geiger Counter.
Gerald Schuller, March 2015 
Modified - Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import random
from math import sin, cos, pi
from matplotlib import pyplot as plt
from myfunctions import clip16

BLOCKSIZE   = 1024      # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Number of channels
RATE        = 8000      # Sampling rate in Hz

# Parameters
T = 10       # Total play time (seconds)
Ta = 0.2    # Decay time (seconds)
f1 = 350    # Frequency (Hz)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)

NumBlocks = int( T * RATE / BLOCKSIZE )

y = [0 for i in range(BLOCKSIZE)]
output = [0 for i in range(BLOCKSIZE)]

plt.ion()           # Turn on interactive mode so plot can be updated
fig = plt.figure(1)
line, = plt.plot(y)
plt.ylim(-32000, 32000)
plt.xlim(0, BLOCKSIZE)
plt.xlabel('Time (n)')
plt.show()

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format      = PA_FORMAT,
                channels    = CHANNELS,
                rate        = RATE,
                input       = False,
                output      = True)

print('Playing for {0:f} seconds ...'.format(T))

THRESHOLD = 2.5 / RATE          # Rate of impulses per second

# Loop through blocks
for i in range(0, NumBlocks):

    # Run difference equation for block
    for n in range(BLOCKSIZE):

        rand_val = random.random()
        if rand_val < THRESHOLD:
            x = 15000
        else:
            x = 0

        y[n] = b0 * x - a1 * y[n-1] - a2 * y[n-2]  
              # What happens when n = 0?
              # In Python negative indices cycle to end, so it works..

        output[n] = int(clip16(y[n]))

    line.set_ydata(output)
    plt.title('Block {0:d}'.format(i))
    plt.pause(0.001)
    plt.draw()

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *output);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
