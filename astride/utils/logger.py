import logging


class Logger():
    """
    Create logger instance for writing to both console and a local file.

    Parameters
    ----------
    filepath : str, optional
        Specify a log filename with the absolute path.
        If not given, no output is written to a file.
    """
    def __init__(self, filepath=None):
        # create logger.
        logger = logging.getLogger('ASTRiDE')
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
        """Return a logger instance."""

        return self.logger

if __name__ == '__main__':

    logger = Logger().getLogger()

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')