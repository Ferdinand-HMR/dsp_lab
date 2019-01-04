b = [1 zeros(1,799) 0.8]
a = [1]

N = [1 zeros(1,1000)]
[x,Fs] = audioread('author.wav')
y = filter(b,a,x)
zplane(b,a)
soundsc(y,Fs)