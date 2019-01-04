# play_sine_no_callback.py
# Play a sinusoid using Pyaudio.
# Write the signal in blocks.
# This program does not use pyaudio callback functions

from math import cos, pi 
import pyaudio, struct
import time
import sys

if sys.version_info[0] < 3:
  # for Python 2
  import Tkinter as Tk
else:
  # for Python 3
  import tkinter as Tk    

Fs = 8000   # sampling rate (samples/second)
T = 4       # duration (seconds)
f1 = 200    # frequency of sinusoid (Hz)
N = T*Fs    # number of samples
om1 = 2.0 * pi * f1 / Fs
gain = 0.5 * 2**15

# Define pyaudio callback function
# Play sin(2 * pi * f1 * n / Fs)
def my_callback_fun(input_binary, BLOCKSIZE, time_info, status):
  # Note: we do not use the input in this demo.

  global theta, om1

  om1 = 2.0 * pi * f1 / Fs

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
    stream_callback = my_callback_fun)

theta = 0

def fun_up():
  global f1
  print('UP')
  f1 = f1 + 20

def fun_dn():
  global f1
  print('DOWN')
  f1 = f1 - 20

def fun_quit():
  # global PLAY
  print('QUIT')
  PLAY = False

# Define TK root
top = Tk.Tk()

# Define widgets
Lab1 = Tk.Label(top, text = 'Frequency adjustment')
Bup = Tk.Button(top, text = 'Increase', command = fun_up)
Bdn = Tk.Button(top, text = 'Decrease', command = fun_dn)
Bquit = Tk.Button(top, text = 'Quit', command = top.quit)

# Place buttons
Lab1.pack()
Bup.pack()
Bdn.pack()
Bquit.pack()

top.mainloop()    # Start GUI

stream.stop_stream()
stream.close()
p.terminate()
