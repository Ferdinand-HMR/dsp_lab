# demo_01_play_wavefile.py
# Play audio from a wave file using callback 
#
# Adaptived from Play(Callback) example
# https://people.csail.mit.edu/hubert/pyaudio/

import pyaudio
import wave
import time

# Open wave file
wavfile = 'author.wav'
wf = wave.open( wavfile, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

print('Play the wave file: {0:s} \n with properties:'.format(wavfile))
print('  %d channel(s)'         % CHANNELS)
print('  %d frames/second'      % RATE)
print('  %d frames'             % LEN)
print('  %d bytes per sample'   % WIDTH)


# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):

    # Note: we do not use the input_string in this demo.

    # Read frames from wave file
    output_string = wf.readframes(block_size)	

    # print(block_size)	   # Print the number of frames if you want to

    return (output_string, pyaudio.paContinue)


# Create audio object
p = pyaudio.PyAudio()

# Set PyAudio format (depends on wave file)
PA_format = p.get_format_from_width(WIDTH)   # e.g., 16-bit integer

# Open audio stream
stream = p.open(format = PA_format,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True,
                stream_callback = my_callback_fun)

stream.start_stream()

print('(1) Is the audio stream is on?', stream.is_active())

while stream.is_active():
    time.sleep(0.1)

print('(2) Is the audio stream is on?', stream.is_active())

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

# Close wave file
wf.close()

