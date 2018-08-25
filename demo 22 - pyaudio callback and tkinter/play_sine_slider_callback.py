# play_sine_buttons_callback.py
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


Fs = 8000     # rate (samples/second)
gain = 0.5 * 2**15

# Set up GUI
top = Tk.Tk()         # Define Tkinter root
f1 = Tk.DoubleVar()   # Define Tk variable f1 : frequency of sinusoid (Hz)
f1.set(200)           # Initialize 

# Define buttons
S1 = Tk.Scale(top, label = 'Frequency', variable = f1, from_ = 100, to = 400, tickinterval = 100)
Bquit = Tk.Button(top, text = 'Quit', command = top.quit)

# Place buttons
S1.pack()
Bquit.pack(fill = Tk.X)


# Define pyaudio callback function
# sin(2 * pi * f1 * n / Fs)
def my_callback_fun(input_binary, BLOCKSIZE, time_info, status):
  # Note: we do not use the input in this demo.

  global theta, om1

  om1 = 2.0 * pi * f1.get() / Fs
  output_block = [0 for n in range(BLOCKSIZE)]
  for i in range(BLOCKSIZE):
    output_block[i] = int( gain * cos(theta) ) 
    theta = theta + om1
  while theta > pi:
    theta = theta - 2.0 * pi
  # Convert output values to binary string
  output_binary = struct.pack('h' * BLOCKSIZE, *output_block)

  return (output_binary, pyaudio.paContinue)    # Return data and status


# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = 1, 
    rate = Fs,
    input = False, 
    output = True,
    frames_per_buffer = 128,
    stream_callback = my_callback_fun)
  
    # specify low frames_per_buffer to reduce latency

theta = 0

top.mainloop()    # Start GUI

stream.stop_stream()
stream.close()
p.terminate()
