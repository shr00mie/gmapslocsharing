import logging

class Logger:

    def __init__(self):

        self.log = self.create_logger()

    def create_logger(self):

        log = logging.getLogger('GMLS')
        log.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_formatter = logging.Formatter('[ {} ][ {} ][ {} ][ {} ]'\
        .format('%(asctime)s', '%(name)9s', '%(levelname)7s', '%(message)s'), \
        datefmt='%Y.%m.%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)

        log.addHandler(console_handler)
