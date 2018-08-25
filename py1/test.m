n = 1:100
f = 261.625565
maxAmp = 2^7 - 1.0 
Fs = 8000
y =maxAmp * sin(n*2*pi*f/Fs)
plot(y)