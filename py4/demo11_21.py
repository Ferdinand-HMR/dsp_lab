# play_vibrato_ver2.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

# TRY BOTH WAVE FILES
wavfile = 'author.wav'
# wavfile = 'decay_cosine_mono.wav'
# wavfile = 'sin01_mono.wav'
print('Play the wave file: {0:s}.'.format(wavfile))

BLOCKSIZE = 64
# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 2
W = 0.2
# W = 0 # for no effct

# f0 = 10
# W = 0.2

# OR
# f0 = 20
# ratio = 1.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print W

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]

# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKSIZE))


# Buffer (delay line) indices
# kr = 0  # read index
# kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
# kw = buffer_MAX/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print('The buffer is {0:d} samples long.'.format(buffer_MAX))

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

# output_all = ''            # output signal in all (string)
output_all = bytes([])            # output signal in all (string)

# kr= [0 for n in range(0, BLOCKSIZE)]


print ('* Playing...')

# Loop through wave file
# for n in range(0, LEN):
#
#     # Get sample from wave file
#     input_string = wf.readframes(1)
#
#     # Convert string to number
#     input_value = struct.unpack('h', input_string)[0]
#
#     # Get previous and next buffer values (since kr is fractional)
#     kr_prev = int(math.floor(kr))
#     kr_next = kr_prev + 1
#     frac = kr - kr_prev    # 0 <= frac < 1
#     if kr_next >= buffer_MAX:
#         kr_next = kr_next - buffer_MAX
#
#     # Compute output value using interpolation
#     output_value = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]
#
#     # Update buffer (pure delay)
#     buffer[int(kw)] = input_value
#
#     # Increment read index
#     kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
#         # Note: kr is fractional (not integer!)
#
#     # Ensure that 0 <= kr < buffer_MAX
#     if kr >= buffer_MAX:
#         # End of buffer. Circle back to front.
#         kr = 0
#
#     # Increment write index
#     kw = kw + 1
#     if kw == buffer_MAX:
#         # End of buffer. Circle back to front.
#         kw = 0
#
#     # Clip and convert output value to binary string
#     output_string = struct.pack('h', int(clip16(output_value)))
#
#     # Write output to audio stream
#     stream.write(output_string)
#
#     output_all = output_all + output_string     # append new to total



kr      = range(0,BLOCKSIZE)
kr_prev = [0.0 for n in range(0, BLOCKSIZE)]
kr_next = [0.0 for n in range(0, BLOCKSIZE)]
frac = [0.0 for n in range(0, BLOCKSIZE)]
kw = range(int(0.5 * buffer_MAX),int(0.5 * buffer_MAX) + BLOCKSIZE)
# buffer = [0 for n in range(0, buffer_MAX) for x in range(0,num_blocks)]
n = 0

# print kr

for i in range(0, num_blocks):

    input_string = wf.readframes(BLOCKSIZE)     # BLOCKSIZE = number of frames read

    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)



    for j in range(0, len(kr)):
        # kr[j] += BLOCKSIZE
        kr_prev[j] = int(math.floor(kr[j]))
        kr_next[j] = kr_prev[j] + 1
        frac[j] = kr[j] - kr_prev[j]
        if kr_next[j] >= buffer_MAX:
            kr_next[j] = kr_next[j] - buffer_MAX

        output_block[j] = (1 - frac[j]) * buffer[kr_prev[j]] + frac[j] * buffer[kr_next[j]]


        # print int(kr[j])
        # output_block[j] = buffer[int(kr[j])]

        buffer[int(kw[j])] = input_tuple[j]



        print kr[j],

        # print  'before', kr[j]
        # kr[j] = kr[j] + BLOCKSIZE + W * math.sin(2 * math.pi * f0 * n / RATE)
        if j >=1:
            kr[j] = kr[j - 1] + 1 + W * math.sin(2 * math.pi * f0 * n / RATE)
        else:
            kr[j] = kr[j]
        n = n + 1
        # kr[j] = kr[j - 1] + 1 + W * math.sin(2 * math.pi * f0 * n / RATE)

        # kr[j] = kr[j-1]  + BLOCKSIZE + W * math.sin(2 * math.pi * f0 * n / RATE)

        print kr[j]




        if kr[j] >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr[j] = kr[j] % buffer_MAX

        # print  'after', kr[j]

        # print "before",kw[j]

        kw[j] = kw[j] + BLOCKSIZE

        if kw[j] >= buffer_MAX:
                # End of buffer. Circle back to front.
            kw[j] = kw[j] % buffer_MAX

        # print 'after', kr[j]
    n = n + 1
    kr[0] = kr[BLOCKSIZE-1] + 1 + W * math.sin(2 * math.pi * f0 * (n) / RATE)

        # print n


        # print kw

    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    stream.write(output_string)

    output_all = output_all + output_string

    # print buffer


    # for n in range(0, BLOCKSIZE):
    #     output_block[n] = (1 - frac[n]) * buffer[kr_prev[n]] + frac[n] * buffer[kr_next[n]]
    #     buffer[i][int(kw[n])] = input_tuple[n]




print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()

# output_wavefile = 'demo11_2.wav'
# print('Writing to wave file', output_wavefile)
# wf = wave.open(output_wavefile, 'w')      # wave file
# wf.setnchannels(1)      # one channel (mono)
# wf.setsampwidth(2)      # two bytes per sample
# wf.setframerate(RATE)   # samples per second
# wf.writeframes(output_all)
# wf.close()
# print('* Finished')

