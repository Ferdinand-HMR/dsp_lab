# play_sine_slider.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use slider to adjust the frequency.

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

def fun_quit():
  global PLAY
  print('QUIT')
  PLAY = False

Fs = 8000     # rate (samples/second)
gain = 0.5 * 2**15

# Define Tkinter root
top = Tk.Tk()

# Define Tk variable
f1 = Tk.DoubleVar()

# Initialize Tk variable
f1.set(200)   # f1 : frequency of sinusoid (Hz)

# Define buttons
S1 = Tk.Scale(top, label = 'Frequency', variable = f1, from_ = 100, to = 400, tickinterval = 100)
Bquit = Tk.Button(top, text = 'Quit', command = fun_quit)

# Place buttons
S1.pack()
Bquit.pack(fill = Tk.X)

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

BLOCKSIZE = 256
output_block = [0 for n in range(BLOCKSIZE)]
theta = 0
PLAY = True

while PLAY:
  top.update()   # update GUI
  om1 = 2.0 * pi * f1.get() / Fs
  for i in range(BLOCKSIZE):
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
