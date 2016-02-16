from os.path import dirname
from os.path import join

from astride.detect import Streak
from astride.utils.logger import Logger


def test():
    logger = Logger().getLogger()

    logger.info('Start.')
    module_path = dirname(__file__)
    file_path = join(module_path, '../datasets/samples', 'long.fits')

    logger.info('Read a fits file..')
    streak = Streak(file_path)

    logger.info('Search streaks..')
    streak.detect()

    logger.info('Save figures and write outputs to %s' %
                streak.output_path)
    streak.write_outputs()
    streak.plot_figures()

    logger.info('Done.')

    logger.handlers = []


if __name__ == '__main__':
    test()