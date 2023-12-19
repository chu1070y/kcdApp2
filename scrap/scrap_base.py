import logging
from module.driver import SeleniumDriver


class ScrapBase:
    def __init__(self):
        self.logger = logging.getLogger('kcd')
        self.driver = SeleniumDriver().get_chrome_driver()

    def __del__(self):
        self.logger.info('Quit driver')
        self.driver.quit()

