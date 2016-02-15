import numpy as np


def moving_average(data, window_size=5):
    """

    :param data: An array of values.
    :param window_size: Moving average window size.
    :return: Moving averaged array.
    """
    window = np.ones(int(window_size))/float(window_size)
    results = np.convolve(data, window, 'valid')

    return results