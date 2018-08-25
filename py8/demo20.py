# Tk_demo_03_slider.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use two sliders to adjust the frequency and gain.

from math import cos, pi
import pyaudio
import struct
import sys
import math
import matplotlib as plt
import numpy as np

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
gain = 0.2 * 2**15

# Define Tkinter root
top = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
gain = Tk.DoubleVar()

# Initialize Tk variables
f1.set(200)   # f1 : frequency of sinusoid (Hz)
gain.set(0.2 * 2**15)

# Define buttons
S_freq = Tk.Scale(top, label = 'Frequency', variable = f1, from_ = 100, to = 400, tickinterval = 100)
S_gain = Tk.Scale(top, label = 'Gain', variable = gain, from_ = 0, to = 2**15-1)
Bquit = Tk.Button(top, text = 'Quit', command = fun_quit)

# Place buttons
Bquit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_gain.pack(side = Tk.LEFT)

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
output_block = [0 for n in range(0, BLOCKSIZE)]
output_block_real = output_block
theta = 0
theta_cache = 0
PLAY = True
cache = [0 for n in range(0, BLOCKSIZE)]
alpha = 0
alpha_n = 0

print('* Start')
while PLAY:
  gain_cache = gain.get()
  top.update()

  gain_use = (gain.get() + gain.get())/2

  om1 = 2.0 * pi * f1.get() / Fs
  print 'f1: ', f1.get()
  T = f1.get() / 5
  for i in range(0, BLOCKSIZE):

      output_block[i] = int(gain.get() * cos(theta))
      k = (gain.get() * cos(theta_cache) - cache[BLOCKSIZE - 1]) / float(T)
      b = cache[BLOCKSIZE - 1]
      print k
      # theta = theta + om1

      if i < T:
          output_block[i] = (k * i + b) * gain.get() * cos(theta)
      else:
          output_block[i] = output_block[i]

      theta = theta + om1
      cache[i] = output_block[i]


  print '========================='
  theta_cache = theta

  # cache = output_block
  output_block = np.clip(output_block,-32767,32767)
  if theta > pi:
  	theta = theta - 2.0 * pi
  output_string = struct.pack('h' * BLOCKSIZE, *output_block)   # 'h' for 16 bits
  stream.write(output_string)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
