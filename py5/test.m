% 
% 
% BLOCKSIZE = 64  # Number of frames per block
% WIDTH = 2  # Bytes per sample
% CHANNELS = 1  # Mono
RATE = 16000  
% 
% alpha = float(2 ** (1/12))
% f0 = 440
% 
% 
% MAXVALUE = 2 ** 15 - 1  # Maximum allowed output signal value (because WIDTH = 2)
% 
% # Parameters
Ta = 2 
f1 = 300  

% # Pole radius and angle
r = 0.01.^(1.0 / (Ta * RATE))  
om1 = 2.0 * pi * double(f1) / RATE

% # Filter coefficients (second-order IIR) 
a1 = -2 * r * cos(om1)
a2 = r.^2
b0 = sin(om1)
a = [1 a1 a2]
b = [b0]
x = [15000 zeros(1,100)]
y = filter(b,a,x)


stem(y)