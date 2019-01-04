function filter_gui_example_ver1

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + randn(1, N);        % Input signal
a = 0
b = 0

figure(1)
subplot(2,1,2)

f1 = 0.5
[b, a] = butter(2, f1)
[H,w] = freqz(b,a)
impulse_response = filter(b,a,[1 zeros(1,499)])
% clf

% xx = x * 5
xx = plot(w,abs(H));
title('Frequency response', 'fontsize', 12 )
xlabel('Frequency')
box off
% xlim([0, N]);
% ylim([-3 3])

subplot(2,1,1)
% clf

line_handle = stem(n, impulse_response);
title('Impulses response', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, 50]);
% ylim([-3 3])
suptitle('Impulse response and frequency response of a second order lowpass butterworth filter')
drawnow;

slider_handle = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle, xx, x}    );

% subplot(2,1,2)

end


function fun1(hObject, eventdata, line_handle,xx, x)

fc = get(hObject, 'Value');  % fc : cut-off frequency

fc = max(0.01, fc);         % minimum value
fc = min(0.99, fc);         % maximum value

[b, a] = butter(2, fc);     % Order-2 Butterworth filter

[H,w] = freqz(b,a)

impulse_response = filter(b,a,[1 zeros(1,499)])
y = filtfilt(b, a, x);

% set(line_handle, 'ydata',  y);        % Update data in figure

set(line_handle, 'ydata', impulse_response)

% set(xx, 'ydata',y)

set(xx , 'ydata' , abs(H))

% title( sprintf('LPF. Cut-off frequency = %.3f', fc), 'fontsize', 12 )

suptitle( sprintf('LPF: Cut-off frequency = %.3f', fc))

end

