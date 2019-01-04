from struct import pack
from math import sin, pi
import wave

Fs = 8000

# Write a mono wave file

wf = wave.open('danshengdaosin.wav', 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(1)			# two bytes per sample
wf.setframerate(Fs)			# samples per second
maxAmp = 2**7 - 1.0 		# maximum amplitude
f = 261.625565  			# Hz (middle C)
for n in range(0, int(0.5*Fs)):	# half second duration
	binary_string = pack('B', maxAmp * sin(n*2*pi*f/Fs) + maxAmp )
	# 'h' indicates 'short'
	wf.writeframes(binary_string)
wf.close()
