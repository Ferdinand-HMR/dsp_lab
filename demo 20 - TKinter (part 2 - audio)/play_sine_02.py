# play_sine_02.py
# Play a sinusoid using Pyaudio.
# Write the signal in blocks.

from math import cos, pi 
import pyaudio
import struct

Fs = 8000   # sampling rate (samples/second)
T = 4       # duration (seconds)
N = T*Fs    # number of samples
f1 = 200    # frequency of sinusoid (Hz)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = 1, 
    rate = Fs,
    input = False, 
    output = True)


gain = 0.2 * 2**15
theta = 0
om1 = 2.0 * pi * f1 / Fs

BLOCKSIZE = 512
output_block = [0 for n in range(0, BLOCKSIZE)]

# Play sin(2 * pi * f1 * n / Fs)

print('* Playing for %d seconds' % T)
for n in range(0, int(N/BLOCKSIZE)):
  for i in range(0, BLOCKSIZE):
    output_block[i] = int( gain * cos(theta) )
    theta = theta + om1
  while theta > pi:
    theta = theta - 2.0 * pi
  output_string = struct.pack('h' * BLOCKSIZE, *output_block)   # 'h' for 16 bits
  stream.write(output_string)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
