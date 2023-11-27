import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from random import uniform, randint
from datetime import datetime as DT
from base.base_page import BasePage
import colorama


class DuckduckPage(BasePage):
    """Методы страницы Duckduck поисковика"""

    SEARCH_TEXT = ['AVITO', 'Авито услуги',
                    'Авито', 'Авито дизайнер',
                    'Авито заказать логотип',
                    'Авито графический дизайнер']




    # Сервис поиска DuckDuckGo
    URL_DUCKDUCK = 'https://html.duckduckgo.com/html/'
    LOGO_VISIBILITY_CHECK = '//a[@title="About DuckDuckGo"]'
    SEARCH_INPUT = '//input[@id="search_form_input_homepage"]'
    SEARCH_BUTTON = '//input[@id="search_button_homepage"]'
    FIRST_BLOCK_OF_SERP = '//span[@class="result__icon"]'
    AVITO_LOGO = '//a[@data-marker="search-form/logo"]'


    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver
        self.wite = WebDriverWait(driver, 30, 1)

    def open_page_duckduck(self):
        self.open(self.URL_DUCKDUCK)

    def way_to_avito(self):
        """Кликает по первой ссылке в выдаче поисковика"""
        RANDOM_SEARCH_INPUT = self.SEARCH_TEXT[randint(0, len(self.SEARCH_TEXT) - 1)]

        self.send_keys_random_speed(('xpath', f'{self.SEARCH_INPUT}'), RANDOM_SEARCH_INPUT)
        self.click_obj(('xpath', f'{self.SEARCH_BUTTON}'))

        self.click_obj(('xpath', f'{self.FIRST_BLOCK_OF_SERP}'))
        error_text = 'Логотип Авито не прогрузился, значит страница тоже'
        self.check_element_visibility_display(('xpath', self.AVITO_LOGO), 4, error_text)


