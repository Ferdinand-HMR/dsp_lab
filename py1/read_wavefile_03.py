
import wave

wf = wave.open('sound2.wav')

print 'number of channels: ', wf.getnchannels() 
print 'number of frames per second: ', wf.getframerate() 
print 'signal length: ', wf.getnframes() 
print 'number of bytes per frame:', wf.getsampwidth() 
