[x, Fs] = audioread('sin_02_mono.wav');
x_min = min(x(x>0));
quantization = max(x) / x_min;
format long g;
x_min
quantization