# play_wav_stereo_ver2.py

import pyaudio
import wave
import struct
import math

def clip16( x ):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return(x)

gain = 0.5

# wavfile = "cat01.wav"
# wavfile = 'sin01_mono.wav'       #play a mono wavefile
wavfile = 'sin01_stereo.wav'   #play a stereo wavefile

print("Play the wave file %s." % wavfile)

wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % RATE)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)


p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )

# Read first frame
input_string = wf.readframes(1)

if num_channels == 2:
    while len(input_string) > 0:
        # Convert string to numbers
        input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple

        # Compute output values
        output_value0 = int(clip16(gain * input_tuple[0]))
        output_value1 = int(clip16(gain * input_tuple[1]))

        # Convert output value to binary string
        # output_string = struct.pack('hh', output_value0, output_value1)
        # Equivalently:
        output_values = [output_value0, output_value1]
        output_string = struct.pack('hh', *output_values)

        # Write output value to audio stream
        stream.write(output_string)

        # Get next frame
        input_string = wf.readframes(1)

elif num_channels ==1:
    while len(input_string) > 0:
        # Convert string to number
        input_value = struct.unpack('h', input_string)[0]
        # ... equivalently:
        # input_tuple = struct.unpack('h', input_string)  # One-element tuple
        # input_value = input_tuple[0]                    # Number

        # Compute output value
        output_value = int(clip16(gain * input_value))  # Integer in allowed range

        # Convert output value to binary string
        output_string = struct.pack('h', output_value)

        # Write binary string to audio stream
        stream.write(output_string)

        # Get next frame
        input_string = wf.readframes(1)
else:
    print "the wavefile has more than two channels"





print("* * Finished * *")

stream.stop_stream()
stream.close()
p.terminate()
