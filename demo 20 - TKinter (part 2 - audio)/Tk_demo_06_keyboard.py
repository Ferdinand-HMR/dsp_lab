# Tk_demo_06_keyboard.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use keyboard to adjust the frequency.
# Display frequency as label text.

from math import cos, pi 
import pyaudio
import struct
import sys

if sys.version_info[0] < 3:
	# for Python 2
	import Tkinter as Tk
else:
	# for Python 3
	import tkinter as Tk   	

Fs = 8000           # rate (samples/second)
f1 = 200            # f1 : frequency of sinusoid (Hz)
gain = 0.2 * 2**15

def my_function(event):
    global PLAY
    global f1
    print('You pressed ' + event.char)
    if event.char == 'q':
      print('Quit')
      PLAY = False
    if event.char == 'i':
      f1 = f1 + 20
    if event.char == 'd':
      f1 = f1 - 20
    f1_str.set('Frequency = ' + str(f1))

# Define Tkinter root
top = Tk.Tk()
top.bind("<Key>", my_function)

f1_str = Tk.StringVar()
f1_str.set('Frequency = ' + str(f1))
label_freq = Tk.Label(top, textvariable = f1_str)
label_freq.pack()

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = 1, 
    rate = Fs,
    input = False, 
    output = True,
    frames_per_buffer = 128)            
    # specify low frames_per_buffer to reduce latency

print('Switch to Python window.')
print('Use i to increase frequency.')
print('Use d to decrease frequency.')
print('Press q to quit.')

BLOCKSIZE = 512
output_block = [0 for n in range(0, BLOCKSIZE)]
theta = 0
PLAY = True

while PLAY:
  top.update()
  om1 = 2.0 * pi * f1 / Fs
  for i in range(0, BLOCKSIZE):
    output_block[i] = int( gain * cos(theta) )
    theta = theta + om1
  while theta > pi:
  	theta = theta - 2.0 * pi
  output_string = struct.pack('h' * BLOCKSIZE, *output_block)   # 'h' for 16 bits
  stream.write(output_string)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
