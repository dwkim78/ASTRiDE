"""Regression and behavior tests for ASTRiDE."""
import os

import numpy as np
import pytest
from astropy.io import fits

from astride import Streak
from astride.utils.edge import EDGE

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'astride',
                      'datasets', 'samples', 'long.fits')


def make_image(segments, shape=(300, 300), noise=1.0, amp=50.0, sigma=1.5,
               seed=42):
    """Gaussian noise background plus thin Gaussian-profile streaks."""
    rng = np.random.RandomState(seed)
    img = rng.normal(0., noise, shape)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(float)
    for (x0, y0, x1, y1) in segments:
        dx, dy = x1 - x0, y1 - y0
        t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / (dx * dx + dy * dy),
                    0., 1.)
        d2 = (xx - (x0 + t * dx)) ** 2 + (yy - (y0 + t * dy)) ** 2
        img += amp * np.exp(-d2 / (2. * sigma ** 2))
    return img


def save_fits(img, path, header=None):
    hdu = fits.PrimaryHDU(np.asarray(img, dtype=np.float32))
    if header:
        for key, value in header.items():
            hdu.header[key] = value
    hdu.writeto(str(path))
    return str(path)


def out_dir(tmp_path, name):
    return str(tmp_path / name) + '/'


def test_sample_image(tmp_path):
    streak = Streak(SAMPLE, output_path=out_dir(tmp_path, 'long'))
    streak.detect()

    assert len(streak.streaks) == 2
    first, second = streak.streaks
    assert first['connectivity'] == 2
    assert second['connectivity'] == -1
    assert first['slope_angle'] == pytest.approx(-5.10, abs=0.3)
    assert second['slope_angle'] == pytest.approx(-4.95, abs=0.3)
    assert first['length'] == pytest.approx(153.5, abs=2.)
    assert second['length'] == pytest.approx(158.5, abs=2.)

    streak.write_outputs()
    streak.plot_figures()
    output = os.path.join(streak.output_path, 'streaks.txt')
    assert os.path.exists(output)
    assert os.path.exists(os.path.join(streak.output_path, 'all.png'))
    with open(output) as fp:
        header = fp.readline()
        # The sample image has a WCS, so sky coordinates are written.
        assert 'ra(hms)' in header
        assert len(fp.readlines()) == 2


def test_remove_bkg_map(tmp_path):
    """The photutils Background2D path must keep working."""
    img = make_image([(50., 50., 250., 200.)])
    # Add a gradient so that a background map is actually needed.
    img += np.linspace(0., 20., img.shape[1])[np.newaxis, :]
    path = save_fits(img, tmp_path / 'gradient.fits')
    streak = Streak(path, remove_bkg='map', bkg_box_size=50,
                    output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    assert streak.background_map is not None
    assert np.isfinite(streak._std) and streak._std > 0.
    assert len(streak.streaks) == 1


def test_invalid_remove_bkg():
    with pytest.raises(RuntimeError):
        Streak(SAMPLE, remove_bkg='nope')


def test_boundary_crossing_streak(tmp_path):
    """A streak crossing the image boundary must still be detected."""
    img = make_image([(-20., 50., 320., 250.)])
    path = save_fits(img, tmp_path / 'boundary.fits')
    streak = Streak(path, output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    assert len(streak.streaks) == 1
    assert streak.streaks[0]['slope_angle'] == pytest.approx(30.5, abs=2.)


def test_vertical_broken_streak_connected(tmp_path):
    """Nearly vertical fragments must be linked despite the angle wrap."""
    img = make_image([(150., 20., 150., 120.), (150., 180., 150., 280.)])
    path = save_fits(img, tmp_path / 'vertical.fits')
    streak = Streak(path, output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    assert len(streak.streaks) == 2
    assert streak.streaks[0]['connectivity'] == 2
    assert abs(streak.streaks[0]['slope_angle']) == pytest.approx(90., abs=1.)


def test_connectivity_distance_cut(tmp_path):
    """Distant collinear objects must not be linked by default."""
    segments = [(10., 150., 40., 150.), (260., 150., 290., 150.)]
    img = make_image(segments)
    path = save_fits(img, tmp_path / 'distant.fits')

    streak = Streak(path, output_path=out_dir(tmp_path, 'out'),
                    shape_cut=0.5, radius_dev_cut=0.4)
    streak.detect()
    assert len(streak.streaks) == 2
    assert streak.streaks[0]['connectivity'] == -1

    # Disabling the distance check restores the old behavior.
    streak = Streak(path, output_path=out_dir(tmp_path, 'out2'),
                    shape_cut=0.5, radius_dev_cut=0.4,
                    connectivity_distance_cut=None)
    streak.detect()
    assert streak.streaks[0]['connectivity'] == 2


def test_bad_wcs_fallback(tmp_path):
    """A header with a broken WCS must fall back to pixel-only output."""
    img = make_image([(50., 50., 250., 200.)])
    path = save_fits(img, tmp_path / 'badwcs.fits',
                     header={'CTYPE1': 'RA---XXX', 'CTYPE2': 'DEC--XXX'})
    streak = Streak(path, output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    streak.write_outputs()
    with open(os.path.join(streak.output_path, 'streaks.txt')) as fp:
        header = fp.readline()
    assert 'ra(hms)' not in header


def test_valid_wcs_output(tmp_path):
    img = make_image([(50., 50., 250., 200.)])
    path = save_fits(img, tmp_path / 'wcs.fits',
                     header={'CTYPE1': 'RA---TAN', 'CTYPE2': 'DEC--TAN',
                             'CRVAL1': 180., 'CRVAL2': 30., 'CRPIX1': 150.,
                             'CRPIX2': 150., 'CD1_1': -1.e-4, 'CD1_2': 0.,
                             'CD2_1': 0., 'CD2_2': 1.e-4})
    streak = Streak(path, output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    streak.write_outputs()
    with open(os.path.join(streak.output_path, 'streaks.txt')) as fp:
        header = fp.readline()
        row = fp.readline().split()
    assert 'ra(hms)' in header
    # ra(deg) of the center must be close to CRVAL1.
    assert float(row[5]) == pytest.approx(180., abs=0.1)


def test_compressed_and_mef_fits(tmp_path):
    """Data in extension HDUs must be found."""
    img = make_image([(50., 50., 250., 200.)])

    path = str(tmp_path / 'comp.fits')
    fits.HDUList([fits.PrimaryHDU(),
                  fits.CompImageHDU(img.astype(np.float32))]).writeto(path)
    streak = Streak(path, output_path=out_dir(tmp_path, 'out1'))
    streak.detect()
    assert len(streak.streaks) == 1

    path = str(tmp_path / 'mef.fits')
    fits.HDUList([fits.PrimaryHDU(),
                  fits.ImageHDU(img.astype(np.float32),
                                name='SCI')]).writeto(path)
    streak = Streak(path, output_path=out_dir(tmp_path, 'out2'))
    streak.detect()
    assert len(streak.streaks) == 1


def test_nan_pixels(tmp_path):
    img = make_image([(50., 50., 250., 200.)])
    img[140:160, :] = np.nan
    path = save_fits(img, tmp_path / 'nan.fits')
    streak = Streak(path, output_path=out_dir(tmp_path, 'out'))
    streak.detect()
    assert np.isfinite(streak._med)
    assert np.isfinite(streak._std)
    assert len(streak.streaks) >= 1


def test_no_image_data(tmp_path):
    path = str(tmp_path / 'empty.fits')
    fits.PrimaryHDU().writeto(path)
    with pytest.raises(ValueError):
        Streak(path)


def test_output_path_without_extension(tmp_path):
    img = make_image([(50., 50., 250., 200.)])
    path = save_fits(img, tmp_path / 'noext')
    streak = Streak(path)
    assert streak.output_path.rstrip('/').endswith('noext_output')


def test_edge_pipeline_order():
    """quantify computes cheap values; fit_lines the line-based ones."""
    img = make_image([(50., 50., 250., 200.)])
    from skimage import measure
    contours = measure.find_contours(img, 3., fully_connected='high')
    edge = EDGE(contours)
    edge.quantify()
    assert 'slope_angle' not in edge.get_edges()[0]
    edge.filter_edges()
    edge.fit_lines()
    assert 'slope_angle' in edge.get_edges()[0]
    edge.connect_edges()
