[x, fs] = audioread('danshengdaosin.wav');
figure(1);
plot(x);
xlim([1,200]);
title('Verifaction of the sine wave');

x_min = min(x(x>0));
quantization = 1 / x_min;
X = fft(x);
% 
figure(2);
plot(abs(X));
title('Spectrum of x');