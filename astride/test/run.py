from os.path import dirname
from os.path import join

from astride.detect import Streak
from astride.utils.logger import Logger


def test():
    logger = Logger().getLogger()

    logger.info('Start.')

    logger.info('Read a fits file..')

    module_path = dirname(__file__)

    file_path = join(module_path, '../datasets/samples', 'long.fits')
    streak = Streak(file_path, output_path='./long/')

    # file_path = '/Users/kim/Temp/hst_13003_54_wfc3_ir_f110w_drz_saved.fits'
    # streak = Streak(file_path, contour_threshold=5, radius_dev_cut=0.4,
    #                 area_cut=100)

    # file_path = '/Users/kim/Temp/M6707HH.fits'
    # streak = Streak(file_path, contour_threshold=2.5)

    # file_path = '/Users/kim/Temp/HorseHead.fits'
    # streak = Streak(file_path)

    # file_path = '/Users/kim/Temp/mgm035.fts'
    # streak = Streak(file_path, shape_cut=0.3, radius_dev_cut=0.4)

    # file_path = '/Users/kim/Temp/dss2.17.00.00+30.00.00.fits'
    # streak = Streak(file_path)

    # file_path = '/Users/kim/Downloads/for_dwkim_2022_06_30/fits/' \
    #             '2022_06_29_16_14_01_000_011107-stacked-tn1657066011.fits'
    # streak = Streak(file_path)

    logger.info('Search streaks..')
    streak.detect()

    # from astride.utils.outlier import Outlier
    # logger.info('Search by Machine Learning..')
    # ot = Outlier(streak.raw_borders)
    # streak.streaks = ot.run(contamination=0.0001)
    # print(streak.streaks)

    logger.info('Save figures and write outputs to %s' %
                streak.output_path)
    streak.write_outputs()
    streak.plot_figures(cut_threshold=5.0)

    logger.info('Done.')

    logger.handlers = []


if __name__ == '__main__':
    test()
