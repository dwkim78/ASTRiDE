from os.path import dirname
from os.path import join

from astride.detect import Streak
from astride.utils.logger import Logger


def test():
    logger = Logger().getLogger()

    logger.info('Start.')
    module_path = dirname(__file__)
    file_path = join(module_path, '../datasets/samples', 'long.fits')
    #file_path = '/Users/kim/Dropbox/iPythonNotebook/ASTRiDE/960-960-000534.fits'
    #file_path = '/Users/kim/Dropbox/iPythonNotebook/ASTRiDE/HorseHead.fits'
    #file_path = '/Users/kim/Dropbox/iPythonNotebook/ASTRiDE/dss2.17.00.00+30.00.00.fits'

    logger.info('Read a fits file..')
    streak = Streak(file_path)

    logger.info('Search streaks..')
    streak.detect()

    #from astride.utils.outlier import Outlier
    #logger.info('Search by Machine Learning..')
    #Outlier(streak.raw_borders)
    #import sys
    #sys.exit()

    logger.info('Save figures and write outputs to %s' %
                streak.output_path)
    streak.write_outputs()
    streak.plot_figures()

    logger.info('Done.')

    logger.handlers = []


if __name__ == '__main__':
    test()