from selenium import webdriver


class SeleniumDriver:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument("--start-maximized")
        self.options.add_argument('--window-size=1000,1000')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-notifications')
        self.options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

    def get_chrome_driver(self):
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)


if __name__ == "__main__":
    driver = SeleniumDriver().get_chrome_driver()
    driver.get('https://www.google.com')

    from time import sleep
    sleep(5)
    driver.quit()
