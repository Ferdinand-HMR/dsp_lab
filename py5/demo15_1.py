# play_keys.py

"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
Gerald Schuller, March 2015
Modified - Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import pygame
import numpy as np
from math import sin, cos, pi



BLOCKSIZE = BLOCKSIZE1 = BLOCKSIZE2 = 64  # Number of frames per block
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Mono
RATE = 16000  # Frames per second

alpha = float(2 ** (1/float(12)))
# f0 = 440
# print alpha

MAXVALUE = 2 ** 15 - 1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2  # Decay time (seconds)
# f1 = 300  # Frequency (Hz)

# Pole radius and angle
# r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
# om0 = om1 = om2 = om3 = om4 = om5 = om6 = om7 = 2.0 * pi * float(f1) / RATE
# # Filter coefficients (second-order IIR)
# a10 = a11 = a12 =a13 =a14 =a15 =a16 = a17 = -2 * r0 * cos(om0)
# a20 = a21 = a22 = a23 = a24 = a25 = a26 = a27 = r0 ** 2
# b00 =b01 =b02 =b03 =b04 =b05 =b06 =b07 = sin(om0)

r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0 # 0.01 for 1 percent amplitude
om0 = om1 = om2 = om3 = om4 = om5 = om6 = om7 = 0
# Filter coefficients (second-order IIR)
a10 = a11 = a12 =a13 =a14 =a15 =a16 = a17 = 0
a20 = a21 = a22 = a23 = a24 = a25 = a26 = a27 = 0
b00 =b01 =b02 =b03 =b04 =b05 =b06 =b07 = 0
#
# r1 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
# om1 = 2.0 * pi * float(f1) / RATE
#
# # Filter coefficients (second-order IIR)
# a11 = -2 * r1 * cos(om1)
# a21 = r1 ** 2
# b01 = sin(om1)



# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
    format=PA_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=128)
# specify low frames_per_buffer to reduce latency

# w = 0

pygame.init()  # Initializes pygame

print("Press keys for sound. Press 'q' to quit.")
print("OK go...")
# y0 = y1 = y2 = y3 = y4 = y5 = y6 = y7 = np.zeros(BLOCKSIZE)


# x0 = x1 = x2 = x3 = x4 = x5 = x6 = x7 = np.zeros(BLOCKSIZE)
x0 = np.zeros(BLOCKSIZE)
x1 = np.zeros(BLOCKSIZE)
x2 = np.zeros(BLOCKSIZE)
x3 = np.zeros(BLOCKSIZE)
x4 = np.zeros(BLOCKSIZE)
x5 = np.zeros(BLOCKSIZE)
x6 = np.zeros(BLOCKSIZE)
x7 = np.zeros(BLOCKSIZE)

y0 = np.zeros(BLOCKSIZE)
y1 = np.zeros(BLOCKSIZE)
y2 = np.zeros(BLOCKSIZE)
y3 = np.zeros(BLOCKSIZE)
y4 = np.zeros(BLOCKSIZE)
y5 = np.zeros(BLOCKSIZE)
y6 = np.zeros(BLOCKSIZE)
y7 = np.zeros(BLOCKSIZE)



stop = False

while stop == False:

    # for i in range(8):
    #     ('x' + str(i)) = 0

    x0[0] = x1[0] = x2[0] = x3[0] = x4[0] = x5[0] = x6[0] = x7[0] = 0.0

    # r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0  # 0.01 for 1 percent amplitude
    # om0 = om1 = om2 = om3 = om4 = om5 = om6 = om7 = 0
    # # Filter coefficients (second-order IIR)
    # a10 = a11 = a12 = a13 = a14 = a15 = a16 = a17 = 0
    # a20 = a21 = a22 = a23 = a24 = a25 = a26 = a27 = 0
    # b00 = b01 = b02 = b03 = b04 = b05 = b06 = b07 = 0




    for event in pygame.event.get():

        # Any key press counts as playing a note
        if event.type == pygame.KEYDOWN:

            if event.key > 100:
                locate = event.key - 110
            else:
                locate = event.key - 49

            if event.key == 49:
                # locate = event.key - 50
                x0[0] = 15000
                # f0 = 440 * (locate)  # Frequency (Hz)
                f0 = float(alpha ** locate * 440)
                r0 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om0 = 2.0 * pi * float(f0) / RATE

                a10 = -2 * r0 * cos(om0)
                a20 = r0 ** 2
                b00 = sin(om0)
                print f0
                #break
                # print f0,om0,a10,a20,b00

            elif event.key == 50:
                # locate = event.key - 50
                x1[0] = 15000
                # f1 = 440 * (locate)  # Frequency (Hz)
                f1 = float(alpha ** locate * 440 )

                r1 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om1 = 2.0 * pi * float(f1) / RATE

                a11 = -2 * r1 * cos(om1)
                a21 = r1 ** 2
                b01 = sin(om1)
                print f1
                #break
                # print f1,om1,a11,a21,b01
            #
            #
            elif event.key == 51:
                # locate = event.key - 50
                x2[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f2 = float(alpha ** locate * 440 )

                r2 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om2 = 2.0 * pi * float(f2) / RATE

                a12 = -2 * r2 * cos(om2)
                a22 = r2 ** 2
                b02 = sin(om2)
                print f2
                #break

            elif event.key == 52:
                x3[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f3 = float(alpha ** locate * 440)

                r3 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om3 = 2.0 * pi * float(f3) / RATE

                a13 = -2 * r3 * cos(om3)
                a23 = r3 ** 2
                b03 = sin(om3)
                print f3

            elif event.key == 53:
                x4[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f4 = float(alpha ** locate * 440)

                r4 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om4 = 2.0 * pi * float(f4) / RATE

                a14 = -2 * r4 * cos(om4)
                a24 = r4 ** 2
                b04 = sin(om4)
                print f4

            elif event.key == 54:

                x5[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f5 = float(alpha ** locate * 440)

                r5 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om5 = 2.0 * pi * float(f5) / RATE

                a15 = -2 * r5 * cos(om5)
                a25 = r5 ** 2
                b05 = sin(om5)
                print f5

            elif event.key == 55:
                x6[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f6 = float(alpha ** locate * 440)

                r6 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om6 = 2.0 * pi * float(f6) / RATE

                a16 = -2 * r6 * cos(om6)
                a26 = r6 ** 2
                b06 = sin(om6)
                print f6

            elif event.key == 56:
                x7[0] = 15000
                # f2 = 440 * (locate)  # Frequency (Hz)
                f7 = float(alpha ** locate * 440)

                r7 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om7 = 2.0 * pi * float(f7) / RATE

                a17 = -2 * r7 * cos(om7)
                a27 = r7 ** 2
                b07 = sin(om7)
                print f7

            else:
                x7[0] = 15000
                locate = 6
                f7 = float(alpha ** locate * 440)

                r7 = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
                om7 = 2.0 * pi * float(f7) / RATE

                a17 = -2 * r7 * cos(om7)
                a27 = r7 ** 2
                b07 = sin(om7)
                print f7

                print "please press the a key in range 1 to 8"



            # x[0] = 15000
            # f1 = 440 * (locate)  # Frequency (Hz)
            # f1 = float(alpha ** locate * 440)
            # print locate
            # print "sound frequency: ",f1


            # Pole radius and angle
            # r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
            # om1 = 2.0 * pi * float(f1) / RATE
            #
            # a1 = -2 * r * cos(om1)
            # a2 = r ** 2
            # b0 = sin(om1)

            # print om1
            # w = 2 * pi * alpha ** (event.key) * f0/RATE
            # x[0] = 15000 * cos(w)
        # Quit if user presses 'q'
        if event.key == pygame.K_q:
            stop = True

    # Do difference equation for block
    # print b02

    # print x0

    for n in range(BLOCKSIZE):


        # w = 2 * pi * alpha ** (pygame.event.key) * f0 / RATE
        # print w
        # x[n] = 15000 * cos(w)
        y0[n] = b00 * x0[n] - a10 * y0[n - 1] - a20 * y0[n - 2]
        y1[n] = b01 * x1[n] - a11 * y1[n - 1] - a21 * y1[n - 2]
        y2[n] = b02 * x2[n] - a12 * y2[n - 1] - a22 * y2[n - 2]

        # print x0
        y3[n] = b03 * x3[n] - a13 * y3[n - 1] - a23 * y3[n - 2]
        y4[n] = b04 * x4[n] - a14 * y4[n - 1] - a24 * y4[n - 2]
        y5[n] = b05 * x5[n] - a15 * y5[n - 1] - a25 * y5[n - 2]
        y6[n] = b06 * x6[n] - a16 * y6[n - 1] - a26 * y6[n - 2]
        y7[n] = b07 * x7[n] - a17 * y7[n - 1] - a27 * y7[n - 2]
        # y[n] = alpha ** (event.key) * f0
        # What happens when n = 0?
        # In Python negative indices cycle to end, so it works..
    y = y0 + y1 + y2 + y3 + y4 + y5 + y6 + y7
    # for i in range(BLOCKSIZE1):
        # y1[i] = b01 * x1[i] - a11 * y1[i - 1] - a21 * y1[i - 2]
    #
    #
    # for n in range(BLOCKSIZE2):
    #     y2[n] = b02 * x2[n] - a12 * y2[n - 1] - a22 * y2[n - 2]


    # y = y0 + y1 + y2

    # print y1

    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)

    # y0 = np.clip(y0.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
    # y1 = np.clip(y1.astype(int), -MAXVALUE, MAXVALUE)
    # # y = y0 + y1
    # # y = np.clip((y0 + y1).astype(int) ,-MAXVALUE, MAXVALUE )
    #
    # # Convert numeric list to binary string
    #
    # data0 = struct.pack('h' * BLOCKSIZE, *y0);
    # data1 = struct.pack('h' * BLOCKSIZE, *y1);
    # data2 = struct.pack('h' * BLOCKSIZE, *y2);

    # y = data0 + data1

    data = struct.pack('h' * BLOCKSIZE, *y);


    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)


print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

pygame.quit()
