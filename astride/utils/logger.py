__author__ = 'kim'

import logging


class Logger():
    """
    Create logger instance for writing to both console and a local file.
    """
    def __init__(self, filepath=None):
        """
        Initailize. Write logger to either console and/or to a disk.

        :param filepath: specify a log filename with the absolute path.
            If not given, no output is written to a file.
        :return:
        """

        # create logger.
        logger = logging.getLogger('UPSILoN')
        logger.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
            #datefmt='%Y/%m/%d %H:%M:%S')

        # create file handler which logs even debug messages.
        if filepath and filepath[0] == '/':
            fh = logging.FileHandler(filepath, 'w')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        # create console handler with a higher log level.
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(ch)

        self.logger = logger

    def getLogger(self):
        """
        Return log instance.
        """

        return self.logger

if __name__ == '__main__':

    logger = Logger().getLogger()

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')