[x, fs] = audioread('sin_4channels.wav');
figure(1)
plot(x)
xlim([1,50])
title('Time domain of the wave file')
x_min = min(x(x>0))
quantization = max(x) / x_min
X = fft(x);

figure(2)
plot(abs(X));
title('Spectrum of the wave file')