# plot_micinput.py
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014
Modified: Ivan Selesnick, September 2015
"""

import pyaudio
import struct
from matplotlib import pyplot as plt
import math
import numpy as np

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
# RATE = 16000
RATE = 8000
BLOCKSIZE = 1024
DURATION = 10        # Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)

# Initialize plot window:
plt.figure(1)
# plt.ylim(-10000, 10000)        # set y-axis limits
# plt.xlim(-BLOCKSIZE,BLOCKSIZE)
plt.ylim(0, 15)        # set y-axis limits



plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Frequency')
plt.ylabel('Amplitude of FFT(dB)')

t = range(0, BLOCKSIZE)

# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], label = 'AM Output',color = 'blue')  # Create empty line
line1, = plt.plot([], [], label = 'Input Voice',color = 'red')
line.set_xdata(t)                         # x-data of plot (time)
line1.set_xdata(t)

plt.legend()

# Open audio device:
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

f0 = 400
om = 2*math.pi*f0/RATE
theta = 0
output_block = [0 for n in range(0, BLOCKSIZE)]


for i in range(1, NumBlocks):
    # input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_string = stream.read(BLOCKSIZE, exception_on_overflow = False)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert

    for n in range(0, BLOCKSIZE):
        theta = theta + om
        output_block[n] = int(input_tuple[n] * math.cos(theta))

    input_tuple_fft = np.abs(np.fft.fft(input_tuple))
    output_block_fft = np.abs(np.fft.fft(output_block))

    input_tuple_fft = np.log(input_tuple_fft)
    output_block_fft = np.log(output_block_fft)

    while theta > math.pi:
        theta = theta - 2*math.pi




    line.set_ydata(output_block_fft)
    line1.set_ydata(input_tuple_fft)
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    stream.write(output_string)
    # Update y-data of plot
    # # Print block number:
    # if i % 20 == 0:
    #     print i,
    plt.pause(0.001)
    plt.draw()
plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
