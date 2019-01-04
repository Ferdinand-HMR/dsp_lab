b = 1 
a = [1 zeros(1,799) -0.8]
syms z 
H = 1 / (1 - 0.8 * z.^(-800))
N = [1 zeros(1,2000)]
y = filter(b,a,N)
plot(y)
h = iztrans(H)