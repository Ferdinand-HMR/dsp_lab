l0 = 6
A =1 
fr = 0.1
n = 1 : 100000
T = 1/8000



ln = l0 * (1 + A * sin(2 * pi * fr * n * T))
% ln = (A * sin(2 * pi * fr * n * T))

plot(ln)