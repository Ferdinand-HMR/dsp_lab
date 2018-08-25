#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 19:41:39 2017

@author: KentPeng
"""
import wave
wf = wave.open('sound1.wav')

channel = wf.getnchannels() 
# number of channels

framerate = wf.getframerate() 
# frame rate (number of frames per second)

length = wf.getnframes() 
# total number of frames (length of signal)

bytesperframe = wf.getsampwidth() 
# number of bytes per frame

print "channel = ",channel, ",framerate = ", framerate, ",length = ", length, ",bytes per frame = ", bytesperframe

