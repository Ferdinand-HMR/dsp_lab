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
from scipy import signal
import numpy as np
import wave

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
plt.ylim(-10000, 10000)        # set y-axis limits

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Time (n)')
t = range(0, BLOCKSIZE)

wf = wave.open('complex_am_module.wav', 'w')
wf.setnchannels(CHANNELS)			# one channel (mono)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], label = 'Complex AM Output',color = 'blue')  # Create empty line
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
#######################################################
K = 7
[b_lpf,a_lpf] = signal.ellip(K,0.2,50,0.48)
I = 1j

b = []
a = []

for i in range(K+1):
    cache = complex(a_lpf[i])
    cache2 = complex(b_lpf[i])

    cache1 = cache * I ** i
    cache3 = cache2 * I ** i
    a.append(cache1)
    b.append(cache3)

# print b

f1 = 400
MAXVALUE = 2**15-1
ORDER = 7   # filter is fourth order
states = np.zeros(ORDER)
AM_module = np.arange(BLOCKSIZE,dtype=complex)

AM_module = np.exp(I * 2 * math.pi * f1 * AM_module)

output_all = bytes([])


# for n in range(0, BLOCKSIZE):
#     AM_module[i] =

#########################################################

for i in range(1, NumBlocks):
    # input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_string = stream.read(BLOCKSIZE, exception_on_overflow = False)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert

#############################################################
    input_block = struct.unpack('h' * BLOCKSIZE, input_string)
    output_block, states = signal.lfilter(b, a, input_block, zi = states)

    # print output_block.shape, type(output_block)

    # clipping


    # output_block = output_block * AM_module



    ###################################################################
    for n in range(0, BLOCKSIZE):
        # theta = theta + om
        # output_block[n] = int(input_tuple[n] * math.cos(theta))
        output_block[n] = output_block[n] * np.exp(I * 2 * math.pi * f1 * (i * BLOCKSIZE + n) / RATE)
        # print i * BLOCKSIZE + n
        # r. * exp(I * 2 * pi * f1 * t)


    output_block = np.real(output_block)

    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    output_block = output_block.astype(int)



    # wf.writeframes(output_string)


    # while theta > math.pi:
    #     theta = theta - 2*math.pi
    #



    line.set_ydata(output_block)
    line1.set_ydata(input_tuple)
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    output_all = output_all + output_string


    stream.write(output_string)
    # Update y-data of plot
    # # Print block number:
    # if i % 20 == 0:
    #     print i,
    plt.pause(0.001)
    plt.draw()
plt.close()

wf.writeframes(output_all)
wf.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')



