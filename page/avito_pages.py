import time
import os
import re
import requests
import urllib.parse
from time import sleep as sleep
from random import randint, uniform
from colorama import Fore, Style
from base.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class Avito(BasePage):

    # функция смены локализации
    LOCALIZATION_ICON = '//div[@class="main-svgWrapper-LdMtx"]'
    LOCATION_CHANGE_CONFIRMATION_BUTTON = '//div[@class="popup-buttons-WICnh"]'
    MAP_PAGINATION = '//span[@class="style-module-wrapper-Q6ELA"]'
    SELECT_CLEAR_LOCATION_INPUT = '//div[@class="suggest-icon-qI_yN"]'
    LOCALIZATION_INPUT = '(//input[@class="suggest-input-rORJM"])[1]'
    SEARCH_RADIUS = '(//span[@class="styles-module-text-wrapper-TEzPs"]//child::*)[1]'

    IMAGES_FULL_SCREEN = '//div[@class="image-frame-wrapper-_NvbY"]'



    """Инициализация дочерних функций от BasePage"""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver
        self.wite = WebDriverWait(driver, 15, 1)


    def logo_click(self):
        """Клик по логотипу Авито, переход на главную страницу"""
        selector = '//a[@class="Logo-module-root-pYmmC"]'
        self.click_obj(('xpath', f'{selector}'))


    def input_serch_avito(self, search_text):
        selector = '(//input[@class="input-input-Zpzc1"])[1]'
        self.find(('xpath', f'{selector}'))
        self.double_click_obj(('xpath', selector))
        self.send_keys_random_speed( ('xpath', selector), search_text)


    def click_serch_button(self):
        selector = '//span[@class="desktop-9uhrzn"]'
        self.click_obj(('xpath', f'{selector}'))


    def localization_switching(self, city = 'Москва'):
        """Изменяет локализацию.

        :arg
        city - str / указать целевой город
        """

        self.click_obj(('xpath', f'{self.LOCALIZATION_ICON}'))
        self.click_obj(('xpath', f'{self.SELECT_CLEAR_LOCATION_INPUT}'))
        self.send_keys_random_speed(('xpath', self.LOCALIZATION_INPUT), city)

        my_city = self.find(('xpath', f'{self.LOCALIZATION_INPUT}'))
        my_city.send_keys(Keys.ENTER)

        self.random_delay(.2, 1)
        random_number_pagination = [randint(1, 5)]
        random_selector = f'({self.MAP_PAGINATION}){random_number_pagination}'

        self.click_obj(('xpath', random_selector), message='Проблема отображения пагинации в разделе локализации')
        # Проверяем текст который остался в поле ввода.
        self.check_expected_value_text(('xpath', self.LOCALIZATION_INPUT), city)
        sleep(uniform(0.5, 2))
        self.click_obj(('xpath', self.LOCATION_CHANGE_CONFIRMATION_BUTTON)) # Клик по кнопке смены локации
        self.random_delay(1, 2)


    def ad_search(self, text_header_bloc):

        def check_post(self):
            """
            1) Определение наличия объявления на странице
            """

            # responce = self.driver.execute_script("return document.documentElement.outerHTML;")
            responce = self.driver.page_source
            text = urllib.parse.unquote(responce)

            # Очищаем страницу. Берем только заголовки объявлений
            clear_text = re.findall(r'},"title":"(.*?)","urlPath"', text)

            all_string = len(clear_text)
            for i in range(all_string):
                clear = clear_text[i]

                if text_header_bloc == clear:
                    number_position = i + 1
                    # print(f"\n\n#{number_position}: {clear_text[i]}")
                    # print(f"объявление на {number_position} месте из {len(clear_text)}")
                    # time.sleep(200)
                    return number_position



        def sroll_logics(self):
            """Если функция check_post(self) не пустая, значит двигаемся
            по элементам к нужному объявлению. Возвращаем в функцию значение 1.

            Иначе, двигаемся в конец объявлений к пагинации страницы.
            И переходим на следующую страницу. Возвращаем в функцию значение 0.
            """
            if check_post(self) is not None:
                """Скролл к номеру объекта на странице по порядку """
                number_position = check_post(self)
                for _ in range(1, number_position + 1):
                    headline = '//div[@class="iva-item-title-py3i_"]/a[@rel="noopener"]'

                    position = self.find(('xpath', f'({headline})[{_}]'))
                    try:
                        self.driver.execute_script("return arguments[0].scrollIntoView();", position)
                    except:
                        pass

                    # rand = randint(0, 1)
                    self.random_delay(0.1, 1.3)
                    if _ == number_position:
                        """Клик на целевой заголовок"""
                        self.click_obj(('xpath', f'({headline})[{_}]'))
                        print(f'{Fore.YELLOW}Клик по заголовку:{Style.RESET_ALL} {Fore.CYAN}{position.text}{Style.RESET_ALL}')


                        """Определение факта открытия второй вкладки"""

                        self.swith_too_new_window(('xpath', self.IMAGES_FULL_SCREEN))

                        """Переход к файлу full_announcement"""
                        # self.go_dance()

                        return 1
                        break


            else:
                button_pagination_next_page = '//a[@data-marker="pagination-button/nextPage"]'
                for p in range(1, 50):
                    headline = '//div[@class="iva-item-title-py3i_"]/a[@rel="noopener"]'
                    position = self.find(('xpath', f'({headline})[{p}]'))
                    try:
                        self.driver.execute_script("return arguments[0].scrollIntoView();", position)
                    except:
                        pass
                    # rand = randint(0, 1)
                    self.random_delay(0.1, 1.3)

                # Нажимаем на погинацию. Кнопку следующей страницы
                self.click_obj(('xpath', button_pagination_next_page))
                print(f'{Fore.YELLOW}pagination:{Style.RESET_ALL} click_next_page')
                time.sleep(3)

                return 0



        while sroll_logics(self) == 0:
            check_post(self) # Определяем есть ли на странице нужный заголовок