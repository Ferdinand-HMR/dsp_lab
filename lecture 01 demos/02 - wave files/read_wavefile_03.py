
import wave

wf = wave.open('cat01.wav')

print 'number of channels: ', wf.getnchannels() 
print 'number of frames per second: ', wf.getframerate() 
print 'signal length: ', wf.getnframes() 
print 'number of bytes per frame:', wf.getsampwidth() 
