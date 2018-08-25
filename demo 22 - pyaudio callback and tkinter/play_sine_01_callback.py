# play_sine_01_callback.py
# Play a sinusoid using Pyaudio.
# Write the signal in blocks.
# This program does not use pyaudio callback functions

from math import cos, pi 
import pyaudio, struct
import time

Fs = 8000   # sampling rate (samples/second)
T = 4       # duration (seconds)
f1 = 200    # frequency of sinusoid (Hz)
N = T*Fs    # number of samples
om1 = 2.0 * pi * f1 / Fs
gain = 0.5 * 2**15

# Define callback function
# Play sin(2 * pi * f1 * n / Fs)
def my_callback_fun(input_binary, BLOCKSIZE, time_info, status):

  # Note: we do not use the input in this demo.
  global theta 

  output_block = [0 for n in range(BLOCKSIZE)]

  for i in range(BLOCKSIZE):
    output_block[i] = int( gain * cos(theta) ) 
    theta = theta + om1
  while theta > pi:
    theta = theta - 2.0 * pi

  # Convert output values to binary string
  output_binary = struct.pack('h' * BLOCKSIZE, *output_block)

  return (output_binary, pyaudio.paContinue)    # Return data and status


# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = 1, 
    rate = Fs,
    input = False, 
    output = True,
    stream_callback = my_callback_fun)

theta = 0

stream.start_stream()

print('* Playing for %d seconds' % T)

# print('The wire will be on for 6 seconds')
# Keep the stream active for 6 seconds by sleeping here
time.sleep(T)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
