# write_sin_02
# 
# Make a wave file (.wav) consisting of a sine wave
# Adapted from http://www.swharden.com

from struct import pack
from math import sin, pi
import wave

Fs = 8000

# Write a mono wave file 

wf = wave.open('sin_02_mono.wav', 'w')		# wf : wave file
wf.setnchannels(1)		# one channel (mono)
wf.setsampwidth(4)		# four bytes per sample
wf.setframerate(Fs)		# samples per second
maxAmp = 2**31 - 1.0 	# maximum amplitude
f = 261.625565  		# Hz (middle C)
for n in range(0, int(0.5*Fs)):	# 1 second duration
	binary_string = pack('i', maxAmp * sin(n*2*pi*f/Fs)) 
    # i indicate 'integer'  ('<i' or '>i' for different Endians)
	wf.writeframesraw(binary_string)
wf.close()

# Write a stereo wave file

wf = wave.open('sin_02_stereo.wav', 'w')
wf.setnchannels(2)		# two channels (stereo)
wf.setsampwidth(4)		# four bytes per sample
wf.setframerate(Fs)		# samples per second
maxAmp = 2**31-1.0 		# maximum amplitude
f1 = 261.625565  		# 261.625565 Hz (middle C)
f2 = 440.0  			# note A4
for n in range(0, int(0.5*Fs)):	# 1 second duration
	binary_string = pack('i', maxAmp * sin(n*2*pi*f1/Fs)) # left channel
	binary_string += pack('i', maxAmp * sin(n*2*pi*f2/Fs)) # right channel
	wf.writeframesraw(binary_string)
wf.close()
