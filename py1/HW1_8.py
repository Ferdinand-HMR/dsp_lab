

from struct import pack
from math import sin, pi
import wave

Fs = 8000


wf = wave.open('sin_4channels.wav', 'w')
wf.setnchannels(4)			# four channels (stereo)
wf.setsampwidth(2)			# two bytes per sample`
wf.setframerate(Fs)			# samples per second
maxAmp = 2**15-1.0 			# maximum amplitude
f1 = 261.625565  			# 261.625565 Hz (middle C)
f2 = 440 				# note A4
f3 = 800
f4 = 1600
for n in range(0, int(0.5*Fs)):	# half second duration
	binary_string = pack('h', maxAmp * sin(n*2*pi*f1/Fs)) # left channel
	binary_string += pack('h', maxAmp * sin(n*2*pi*f2/Fs)) # right channel
	binary_string += pack('h', maxAmp * sin(n*2*pi*f3/Fs))
	binary_string += pack('h', maxAmp * sin(n*2*pi*f4/Fs))
	# 'h' indicates 'short'
	wf.writeframes(binary_string)
wf.close()
