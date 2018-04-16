import os

import numpy as np
import pylab as pl

from skimage import measure
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.stats import SigmaClip
from photutils import Background2D, MedianBackground

from astride.utils.edge import EDGE


class Streak:
    """
    Detect streaks using several morphological values.

    Parameters
    ----------
    filename : str
        Fits filename.
    remove_bkg : {'constant', 'map'}, optional.
        Which method to remove image background. 'constant' uses sigma-clipped
        statistics of the image to calculate the constant background value.
        'map' derives a background map of the image.Default is 'constant'.
        If your image has varing background, use 'map'.
    bkg_box_size : int, optional
        Box size for background estimation.
    contour_threshold : float, optional
        Threshold to search contours (i.e. edges of an input image)
    min_points: int, optional
        The number of minimum data points in each edge.
    shape_cut : float, optional
        An empirical shape factor cut.
    area_cut : float, optional
        An empirical area cut.
    radius_dev_cut : float, optional
        An empirical radius deviation cut.
    connectivity_angle: float, optional
        An maximum angle to connect each separated edge.
    fully_connected: str, optional
        See skimage.measure.find_contours for details.
    output_path: str, optional
        Path to save figures and output files. If None, the input folder name
        and base filename is used as the output folder name.
    """
    def __init__(self, filename, remove_bkg='constant', bkg_box_size=50,
                 contour_threshold=3., min_points=10, shape_cut=0.2,
                 area_cut=10., radius_dev_cut=0.5, connectivity_angle=3.,
                 fully_connected='high', output_path=None):
        hdulist = fits.open(filename)
        raw_image = hdulist[0].data.astype(np.float64)
        hdulist.close()

        # Raw image.
        self.raw_image = raw_image
        # Background structure and background map
        self._bkg = None
        self.background_map = None
        # Background removed image.
        self.image = None
        # Raw edges
        self.raw_borders = None
        # Filtered edges, so streak, by their morphologies and
        # also connected (i.e. linked) by their slope.
        self.streaks = None
        # Statistics for the image data.
        self._med = None
        self._std = None

        # Other variables.
        remove_bkg_options = ('constant', 'map')
        if remove_bkg not in remove_bkg_options:
            raise RuntimeError('"remove_bkg" must be the one among: %s' %
                               ', '.join(remove_bkg_options))
        self.remove_bkg = remove_bkg
        self.bkg_box_size = bkg_box_size
        self.contour_threshold = contour_threshold

        # These variables for the edge detections and linking.
        self.min_points = min_points
        self.shape_cut = shape_cut
        self.area_cut = area_cut
        self.radius_dev_cut = radius_dev_cut
        self.connectivity_angle = connectivity_angle
        self.fully_connected = fully_connected

        # Set output path.
        if output_path is None:
            output_path = '%s' % \
                          (filename[:filename.rfind('.')])
        if output_path[-1] != '/':
            output_path += '/'
        self.output_path = output_path

        # For plotting.
        pl.rcParams['figure.figsize'] = [12, 9]

    def detect(self):
        """Run the pipeline to detect streaks."""
        # Remove background.
        if self.remove_bkg is 'map':
            self._remove_background()
        elif self.remove_bkg is 'constant':
            _mean, self._med, self._std = \
                sigma_clipped_stats(self.raw_image)
            self.image = self.raw_image - self._med

        # Detect sources. Test purpose only.
        # self._detect_sources()

        # Detect streaks.
        self._detect_streaks()

    def _remove_background(self):
        # Get background map and subtract.
        sigma_clip = SigmaClip(sigma=3., iters=10)
        bkg_estimator = MedianBackground()
        self._bkg = Background2D(self.raw_image,
                           (self.bkg_box_size, self.bkg_box_size),
                           filter_size=(3, 3),
                           sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
        self.background_map = self._bkg.background
        self.image = self.raw_image - self.background_map

        self._med = self._bkg.background_median
        self._std = self._bkg.background_rms_median

    def _detect_streaks(self):
        # Find contours.
        # Returned contours is the list of [row, columns] (i.e. [y, x])
        contours = measure.find_contours(
            self.image, self._std * self.contour_threshold,
            fully_connected=self.fully_connected)

        # Quantify shapes of the contours and save them as 'edges'.
        edge = EDGE(contours, min_points=self.min_points,
                    shape_cut=self.shape_cut, area_cut=self.area_cut,
                    radius_dev_cut=self.radius_dev_cut,
                    connectivity_angle=self.connectivity_angle)
        edge.quantify()
        self.raw_borders = edge.get_edges()

        # Filter the edges, so only streak remains.
        edge.filter_edges()
        edge.connect_edges()

        # Set streaks variable.
        self.streaks = edge.get_edges()

    def _detect_sources(self):
        from photutils import DAOStarFinder

        fwhm = 3.
        detection_threshold = 3.
        daofind = DAOStarFinder(threshold=(self._med + self._std *
                                detection_threshold), fwhm=fwhm)
        sources = daofind.find_stars(self.image)
        pl.plot(sources['xcentroid'], sources['ycentroid'], 'r.')

    def _find_box(self, n, edges, xs, ys):
        """
        Connect edges by their "connectivity" values.

        Recursive function that defines a box surrounding one or more
        edges that are connected to each other.

        Parameters
        ----------
        n : int
            Index of edge currently checking.
        edges: array_like
            An array containing information of all edges.
        xs : array_like
            X min and max coordinates. (N,2) matrix.
        ys : array_like
            Y min and max coordinates. (N,2) matrix.

        Returns
        -------
        x_mins : array_like
            X min and max coordinates.
        y_mins : array_like
            Y min and max coordinates.
        """
        # Add current coordinates.
        current_edge = [edge for edge in edges if edge['index'] == n][0]
        current_edge['box_plotted'] = True
        xs.append([current_edge['x_min'], current_edge['x_max']])
        ys.append([current_edge['y_min'], current_edge['y_max']])

        # If connected with other edge.
        if current_edge['connectivity'] != -1:
            self._find_box(current_edge['connectivity'], edges, xs, ys)
        # Otherwise.
        else:
            return xs, ys

    def plot_figures(self, cut_threshold=3.):
        """
        Save figures of detected streaks.

        Parameters
        ----------
        cut_threshold: float, optional
            Threshold to cut image values to make it more visible.
        """
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # Plot the image.
        plot_data = self.image.copy()

        # Background subtracted image,
        # so the median value should be close to zero.
        med = 0.
        std = self._std

        plot_data[np.where(self.image > med + cut_threshold * std)] = \
            med + cut_threshold * std
        plot_data[np.where(self.image < med - cut_threshold * std)] = \
            med - cut_threshold * std
        pl.clf()
        pl.imshow(plot_data, origin='lower', cmap='gray')

        # Plot all raw borders. Test purpose only.
        #edges = self.raw_borders
        #for n, edge in enumerate(edges):
        #    pl.plot(edge['x'], edge['y'])
        #    pl.text(edge['x'][0], edge['y'][1],
        #            '%.2f' % (edge['shape_factor']), color='b', fontsize=10)
        #pl.axis([0, self.image.shape[0], 0, self.image.shape[1]])
        #pl.savefig('%sall.png' % self.output_path)
        #return 0

        edges = self.streaks
        # Plot all contours.
        for n, edge in enumerate(edges):
            pl.plot(edge['x'], edge['y'])
            pl.text(edge['x'][0], edge['y'][1],
                    '%d' % (edge['index']), color='b', fontsize=15)

        # Plot boxes.
        # Box margin in pixel.
        box_margin = 10
        for n, edge in enumerate(edges):
            # plot boxes around the edge.
            if not edge['box_plotted']:
                # Define the box to plot.
                xs = []
                ys = []
                self._find_box(edge['index'], edges, xs, ys)
                x_min = max(np.min(xs) - box_margin, 0)
                x_max = min(np.max(xs) + box_margin, self.image.shape[0])
                y_min = max(np.min(ys) - box_margin, 0)
                y_max = min(np.max(ys) + box_margin, self.image.shape[1])
                box_x = [x_min, x_min, x_max, x_max]
                box_y = [y_min, y_max, y_max, y_min]
                pl.fill(box_x, box_y, ls='--', fill=False, ec='r', lw=2)
                edge['box_plotted'] = True

        pl.xlabel('X/pixel')
        pl.ylabel('Y/pixel')
        pl.axis([0, self.image.shape[1], 0, self.image.shape[0]])
        pl.savefig('%sall.png' % self.output_path)

        # Plot all individual edges (connected).
        for n, edge in enumerate(edges):
            # Reset.
            edge['box_plotted'] = False

        for n, edge in enumerate(edges):
            if not edge['box_plotted']:
                # Define the box to plot.
                xs = []
                ys = []
                self._find_box(edge['index'], edges, xs, ys)
                x_min = max(np.min(xs) - box_margin, 0)
                x_max = min(np.max(xs) + box_margin, self.image.shape[0])
                y_min = max(np.min(ys) - box_margin, 0)
                y_max = min(np.max(ys) + box_margin, self.image.shape[1])
                edge['box_plotted'] = True
                pl.axis([x_min, x_max, y_min, y_max])
                pl.savefig('%s%d.png' % (self.output_path, edge['index']))

        # Clear figure.
        pl.clf()

    def write_outputs(self):
        """Write information of detected streaks."""

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        fp = open('%sstreaks.txt' % self.output_path, 'w')
        fp.writelines('#ID x_center y_center area perimeter shape_factor ' +
                      'radius_deviation slope_angle intercept connectivity\n')
        for n, edge in enumerate(self.streaks):
            line = '%2d %7.2f %7.2f %6.1f %6.1f %6.3f %6.2f %5.2f %7.2f %2d\n' \
                   % \
                   (
                       edge['index'], edge['x_center'], edge['y_center'],
                       edge['area'], edge['perimeter'], edge['shape_factor'],
                       edge['radius_deviation'], edge['slope_angle'],
                       edge['intercept'], edge['connectivity']
                   )
            fp.writelines(line)
        fp.close()

if __name__ == '__main__':
    import time

    streak = Streak('./datasets/samples/long.fits')
    #streak = Streak('/Users/kim/Dropbox/iPythonNotebook/ASTRiDE/mgm035.fts',
    #                shape_cut=0.3, radius_dev_cut=0.4)

    start = time.time()
    streak.detect()
    end = time.time()

    streak.plot_figures()
    streak.write_outputs()

    print('%.2f seconds' % (end - start))
