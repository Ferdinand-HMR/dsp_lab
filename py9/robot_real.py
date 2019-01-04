from stft import stft
from stft_inverse import stft_inverse

import pyaudio
import wave
import math
import struct
import numpy as np

R = 256
Nfft = 1024
BLOCKSIZE = R
DURATION = 5


RATE = 16000
CHANNELS = 1
WIDTH = 2


LEN = DURATION * RATE


# wavefile = 'author.wav'


wf = wave.open('output_robot_real1.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)
# LEN = wf.getnframes()
# WIDTH = wf.getsampwidth()
# CHANNELS = wf.getnchannels()
# RATE = wf.getframerate()

num_blocks = int(math.floor(LEN / BLOCKSIZE))
output_block = [0 for n in range(0,BLOCKSIZE)]


p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = 128)

output_all = bytes([])

for i in range(0,num_blocks):
    input_string = stream.read(BLOCKSIZE, exception_on_overflow = False)
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)

    input_list = list(input_tuple)
    input_array = np.array(input_list).reshape(1,-1)

    STFT = stft(input_array,R,Nfft)

    STFT_abs = np.absolute(STFT)

    STFT_inverse = stft_inverse(STFT_abs,R,R) * 5



    inverse_list = np.ndarray.tolist(STFT_inverse[0,:])
    output_block = tuple(inverse_list)

    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_string)
    output_all = output_all + output_string

stream.stop_stream()
stream.close()
p.terminate()
wf.writeframes(output_all)
wf.close()

# output_wavefile = 'output_robot.wav'
# print('Writing to wave file', output_wavefile)
# wf = wave.open(output_wavefile, 'w')      # wave file
# wf.setnchannels(CHANNELS)      # one channel (mono)
# wf.setsampwidth(WIDTH)      # two bytes per sample
# wf.setframerate(RATE)   # samples per second
# wf.writeframes(output_all)
# wf.close()
# print('* Finished')