import pyaudio
import struct
from matplotlib import pyplot as plt
import math
from scipy import signal

[x,Fs] =

K = 7
[b_lpf,a_lpf] = signal.ellip(K,0.2,50,0.48)
I = 1j

# b = b_lpf
# a = a_lpf

b = []
a = []

for i in range(K+1):
    cache = complex(a_lpf[i])
    cache2 = complex(b_lpf[i])

    cache1 = cache * I ** i
    cache3 = cache2 * I ** i
    a.append(cache1)
    b.append(cache3)

print b


r = signal.lfilter(b,a,x)