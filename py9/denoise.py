from stft import stft
from stft_inverse import  stft_inverse

import pyaudio
import wave
import math
import struct
import numpy as np

from Threshold import threshold_function

R = 512
Nfft = 1024
BLOCKSIZE = R


wavefile = 'noisy_speech.wav'


wf = wave.open(wavefile, 'rb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(WIDTH)
# wf.setframerate(RATE)
LEN = wf.getnframes()
WIDTH = wf.getsampwidth()
CHANNELS = wf.getnchannels()
RATE = wf.getframerate()

num_blocks = int(math.floor(LEN / BLOCKSIZE))
output_block = [0 for n in range(0,BLOCKSIZE)]


p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,
    channels = CHANNELS,
    rate = RATE,
    input = False,
    output = True,)

output_all = bytes([])

for i in range(0,num_blocks):
    input_string = wf.readframes(BLOCKSIZE)
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)

    input_list = list(input_tuple)
    input_array = np.array(input_list).reshape(1,-1)

    STFT = stft(input_array,R,Nfft)

    STFT_filtred = threshold_function(STFT, 112000)





    STFT_inverse = stft_inverse(STFT_filtred,R,R)

    inverse_list = np.ndarray.tolist(STFT_inverse[0,:])
    output_block = tuple(inverse_list)

    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_string)
    output_all = output_all + output_string

stream.stop_stream()
stream.close()
p.terminate()
wf.close()

output_wavefile = 'output_denoised.wav'
print('Writing to wave file', output_wavefile)
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(CHANNELS)      # one channel (mono)
wf.setsampwidth(WIDTH)      # two bytes per sample
wf.setframerate(RATE)   # samples per second
wf.writeframes(output_all)
wf.close()
print('* Finished')