import pylab as pl
import numpy as np

from skimage import measure
from photutils.background import Background

from astride.datasets.base import read_fits
from astride.edge import EDGE


def run():
    data = read_fits().astype(np.float64)

    # Get background map and subtract.
    bkg = Background(data, (30, 30), filter_shape=(3, 3), method='median')
    data -= bkg.background

    # Plot.
    cut_threshold = 0.5
    med = np.median(data)
    std = np.std(data)
    plot_data = data.copy()
    plot_data[np.where(data > med + cut_threshold * std)] = \
        med + cut_threshold * std
    plot_data[np.where(data < med - cut_threshold * std)] = \
        med - cut_threshold * std
    pl.figure(figsize=(14,12))
    pl.imshow(plot_data, origin='lower', cmap='gray')

    # Find contours.
    contours = measure.find_contours(
            data, bkg.background_rms_median * 3.,
            fully_connected='high'
                                     )

    # Quantify shapes of the contours.
    edge = EDGE(contours)
    edge.quantify()
    edges = edge.get_edges()

    # Plot all contours found.
    for n, edge in enumerate(edges):
        pl.plot(edge['positions'][::, 1], edge['positions'][::, 0])
        #pl.text(edge['positions'][::, 1][0], edge['positions'][::, 0][0],
        #        '%.2f' % (edge['shape_factor']))

    pl.xlabel('X/pixel')
    pl.ylabel('Y/pixel')
    pl.axis([0, data.shape[0], 0, data.shape[1]])
    pl.show()

    shape_factors = [edge['shape_factor'] for edge in edges]
    pl.hist(shape_factors, bins=30)
    pl.show()

if __name__ == '__main__':
    run()