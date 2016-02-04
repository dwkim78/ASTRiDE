import pylab as pl
import numpy as np

from astride.datasets.base import read_fits


def run():
    data = read_fits()
    plot_data = data.copy()

    cut_threshold = 1.
    med = np.median(data)
    std = np.std(data)

    plot_data[np.where(data >= med + cut_threshold * std)] = \
        med + cut_threshold * std
    plot_data[np.where(data <= med - cut_threshold * std)] = \
        med - cut_threshold * std
    pl.imshow(plot_data, origin='lower', cmap='gray')
    pl.title('Processed image')
    pl.xlabel('X/pixel')
    pl.ylabel('Y/pixel')
    pl.show()

if __name__ == '__main__':
    run()