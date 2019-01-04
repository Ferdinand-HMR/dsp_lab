def threshold_function(input,threshold):


    import numpy as np

    for i in range(0,input.shape[0]):
        for j in range(0,input.shape[1]):
            if np.abs(input[i,j]) < threshold:
                input[i,j] = 0
            else:
                input[i,j] = input[i,j]

    output = input
    return output
