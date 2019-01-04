def stft_inverse(X, R, N):
    # Inverse Short_time Fourier Transform with 50% overlap

    import numpy as np
    from stft import stft
    from math import pi

    # x = np.ones([1, 4001])
    # R = 512
    # Nfft1 = 1024

    # X = stft(x, R, Nfft1)
    # print X[10, :]

    print "=========start to inverse========="
    [Nfft, Nc] = X.shape
    # N = 4001
    n = np.linspace(1, R, R) - 0.5
    n = n.reshape(1, n.shape[0])

    # print n.shape
    window = np.cos(pi * n / R - pi / 2)

    print "window shape: ", window.shape

    Y = np.fft.ifft(X, Nfft, axis=0)
    # print Y[0,:]

    Y = Y[0: R, :]

    y = np.zeros((1, R / 2 * (Nc + 1)))

    # print Y.shape
    # print y.shape

    i = 0
    for k in range(0, Nc):
        y[0, i: i + R] = y[0, i: i + R] + window * Y[:, k].T
        i = i + R / 2

    # print y.dtype

    y[0, 0: R / 2] = y[0, 0: R / 2] / (window[0, 0: R / 2] ** 2)

    # y(end-R/2+(1:R/2)) = y(end-R/2+(1:R/2)) ./ (window(R/2+1:R).^2);

    y[0, y.shape[1] - R / 2 + 0: y.shape[1] - R / 2 + R / 2] = y[0,
                                                               y.shape[1] - R / 2 + 0: y.shape[1] - R / 2 + R / 2] / (
                                                               window[0, R / 2: window.shape[1]] ** 2)

    y = y[0, R + 0: R + N]

    # print y.shape

    y = y.reshape(1, y.shape[0])
    print "shape of y:", y.shape
    print "=========inverse finished========="

    return y





