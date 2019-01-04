def stft(x,R,Nfft):
    import numpy as np
    from math import pi,ceil




    # R = 512
    # Nfft = 1024
    # x = np.array([[1, 1, 1, 1, 1]])
    # x = np.array([[1], [1], [1]])
    # x = np.zeros([1, 4001])
    # x = np.ones((1, 5))
    # print 'x:', x
    print "=========start STFT========="
    if x.shape[0] != 1:
        x = x.T
    print "shape of x:",x.shape

    n = np.linspace(1, R, R) - 0.5
    n = n.reshape(1, n.shape[0])
    # print n.shape

    window = np.cos(pi * n / R - pi / 2)
    print 'window shape: ',window.shape

    cache1 = np.zeros([1, R])

    x = np.concatenate((cache1, x, cache1), axis=1)
    # print x.shape

    Nx = x.shape[1]

    Nc = (2 * float(Nx) / R)
    # print  float(Nx) / R * 2
    Nc = int(ceil(Nc) - 1)
    # print x.dtype

    L = R / 2 * (Nc + 1)

    if Nx < L:
        x = np.concatenate((x, np.zeros((1, L - Nx), dtype=np.float64)), axis=1)

    X = np.zeros((R, Nc))
    i = 0

    # print x[0][i:R + i].shape

    #
    # for k in range(0,Nc):
    #     for j in range(0,R ):
    #         X[:,k] = window * x[0,i: i +  R]
    #
    #     i = i + R / 2

    for k in range(0, Nc):
        X[:, k] = window * x[0, i: i + R]
        i = i + R / 2

    print 'Number of blocks: ',Nc
    print 'Output shape before FFT:', X.shape

    X = np.fft.fft(X, Nfft, axis=0)
    print 'Output shape:', X.shape
    print "=========STFT finished========"



    return X




