# echo_via_append.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation does not use a circular buffer,
# it uses 'append' and 'remove'

import pyaudio
import wave
import struct
from myfunctions import clip16
import math


wavfile = 'author.wav'
print('Play the wave file %s.' % wavfile)

# Open the wave file
wf = wave.open( wavfile, 'rb')

# Read the wave file properties
num_channels    = wf.getnchannels()     # Number of channels
RATE            = wf.getframerate()     # Sampling rate (frames/second)
signal_length   = wf.getnframes()       # Signal length
width           = wf.getsampwidth()     # Number of bytes per sample

print('The file has %d channel(s).'            % num_channels)
print('The frame rate is %d frames/second.'    % RATE)
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % width)

# Set parameters of delay system
gain = 1.0
gain_delay = 0.8
delay_sec = 0.05 # 50 milliseconds
delay_samples = int( math.floor( RATE * delay_sec ) )

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))

# Create a buffer to store past values. Initialize to zero.
# buffer = [ 1 for i in range(delay_samples) ]

buffer = [1,2,3,4,5]
buffer.append(222)
buffer[0:1] = []


print buffer