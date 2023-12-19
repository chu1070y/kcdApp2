import logging
from logging.handlers import RotatingFileHandler


class CustomLog:
    def __init__(self, name):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(name)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] %(message)s')

        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        self.logger.addHandler(s_handler)

        r_handler = RotatingFileHandler('./log/app.log', mode='a', maxBytes=10240, backupCount=10)
        r_handler.setFormatter(formatter)
        self.logger.addHandler(r_handler)

        self.logger.info('logger created')

    def getLogger(self):
        return self.logger

