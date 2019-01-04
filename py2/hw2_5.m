A = [1 -1.9 0.998]
B = [1 -0.95 0]

x = [1 zeros(1,999)]
Y = filter(B,A,x)
figure(1)
plot(Y)
xlabel('n')
title('impulse response')

Y(1)