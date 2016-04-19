"""
Base IO code for all datasets
"""

from os.path import dirname
from os.path import join

from astropy.io import fits


def read_fits(filename='long.fits'):
    """
    Read an sample fits file and return only image part.

    Parameters
    ----------
    filename : str
        Fits filename.

    Returns
    -------
    data : numpy.ndarray
        Fits image data.
    """

    module_path = dirname(__file__)
    file_path = join(module_path, 'samples', filename)

    hdulist = fits.open(file_path)

    data = hdulist[0].data

    hdulist.close()

    return data