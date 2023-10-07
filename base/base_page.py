from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from random import uniform, randint
from datetime import datetime as DT
from time import sleep
from colorama  import Fore, Style
import os
import re


class BasePage:
    """Базовые / общие функции"""

    # Авито - общие элементы
    AVITO_LOGO = '//a[@class="Logo-module-root-pYmmC"]'


    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wite = WebDriverWait(driver, 30, 1)

    def open(self, url: str):
        """ Метод открывает указанную страницу
        и проверяет текущий URL на соответствие """
        self.driver.delete_all_cookies()
        self.driver.get(url)
        self.wite.until(EC.url_to_be(url))
        print(f'Открыта страница: > {url}')


    def find(self, selector):
        """
        Проверяет видимый элемент на странице с ожиданием.
        Если элемента нет, обращается к функции error_info(), которая снимает скрин
        И выдает в консоли время и текстовую информацию исключения.

        Args:
            - selector:  str / например: (('xpath', selector))
            - exception_text: информация о ошибке
        """
        try:
            return self.wite.until(EC.visibility_of_element_located(selector))
        except TimeoutException:
            self.error_info(exception_text=f'ОБЪЕКТ НЕ НАЙДЕН. Локатор > {selector}')


    def click_obj(self, click_elem: str, message:str = 'СКРИН - Событие перед кликом'):
        """Клик по видимому обьекту страницы

        click_elem = str / например:  ('xpath', click_elem)

        """
        try:
            my_obj = self.wite.until(EC.visibility_of_element_located(click_elem))

            ActionChains(self.driver).click(my_obj).perform()


        except TimeoutException:
            self.error_info(message)


    def click_on_objects_after_random_time(self, locator, value_limit = None,  message ='СКРИН - Событие перед кликом'):
        """Рандомно кликает по всем найденным индексам элементов по локатору. С рандомной паузой.

        :param value_limit: (int) - ограничение использования рандомных индексов. По умолчанию будут использоваться
        все найденные индексы совпадений на странице. По локатору.
        """

        count_obj = self.wite.until(EC.visibility_of_all_elements_located(('xpath', locator)))
        all_objects = len(count_obj) # количество элементов по локатору

        def clic_my_elements():
            random_index = randint(1, all_objects)

            try:
                obg = self.wite.until(EC.visibility_of_element_located(('xpath', f'{locator}[{random_index}]')))
                ActionChains(self.driver).click(obg).perform()
                # obg.click()

            except TimeoutException:
                self.error_info(message)


        if value_limit is None:
            for i in range(all_objects):
                self.random_delay(.7, 7)
                clic_my_elements()

        else:
            for _ in range(value_limit):
                self.random_delay(.7, 7)
                clic_my_elements()

    def double_click_obj(self, click_elem):
        """Двойной Клик по видимому обьекту страницы

        click_elem = str / например:  ('xpath', click_elem)

        """
        try:
            my_obj = self.find(click_elem)

            action = ActionChains(self.driver)
            action.double_click((my_obj)).perform()
        except TimeoutException:
            self.find((click_elem), 'СКРИН / Событие перед кликом')


    def check_expected_value_text(self, locator, expected_text):
        """Проверяем значение поля ввода на ожидаемый текст

        :param locator:(str)  например:  ('xpath', 'selector')
        :param expected_text:(str)  например:  'Москва')"""

        try:
            wait = self.wite.until(EC.text_to_be_present_in_element_value(locator, expected_text))

        except Exception as e:
            print(f'Ошибка сравнения. {e} value != {expected_text}')


    def check_element_visibility_display(self, obj, expected_time = 4, exception_text = None):
        """Проверяем факт загрузки ключевого элемента (Logo) на всех страницах Авито"""

        try:
            self.wite.until(EC.visibility_of_element_located((obj)))

        except TimeoutException:
            self.driver.stop_client()
            self.driver.refresh()
            self.check_element_visibility_display(expected_time)
        except:
            self.error_info(exception_text)


    def swith_too_new_window(self, selector):
        """
        Функция проверяет достоверность наличия двух открытых вкладок.
        И если это так, активирует последнее открытую вкладку.
        Проверяет отображение уникального контрольного обьекта.
        Возвращает в функцию количество открытых вкладок.

        :param exception_text:(str) / Текст оповещения - в случае если ключевой объект не виден.
        :param selector:(str) / кортеж с параметрами ('xpath', selector)
        """

        count_window = self.driver.window_handles
        if len(count_window) == 2:
            last_window = count_window[1]
            self.driver.switch_to.window(last_window)

            self.find(selector)
            print('Переключение на новое окно')
            return len(count_window)


    def send_keys_random_speed(self, locator_input, my_text):
        my_input = self.find((locator_input))
        my_input.click()
        letters = list(my_text)

        for i in range(len(my_text)):
            random_count = uniform(0, 0.4) # Рандомное число с плавающей точкой
            my_input.send_keys(letters[i])
            sleep(random_count)
        sleep(2)
        # сделать механизм проверки известности города


    def random_delay(self, count_a = None, count_b = None):
        """
        Два варианта рандомной паузы uniform и randint.
        :param count_a: (float / int) randint или uniform
        :param count_b: (float / int) randint или uniform
        """
        if count_a and count_b is not None:
            if type(count_a) == float or type(count_b) == float:
                sleep(uniform(float(count_a), float(count_b)))
            else:
                sleep(randint(count_a, count_b))
        else:
            print('нет вводных данных для рандомной паузы')


    def error_info(self, exception_text = 'Смотреть скрин ошибки'):
        """Вспомогательный метод.
        Выводит дату / время / сообщение исключения функции
        Делает скриншот в папку - screen

        :exception_text - принимает str / сообщение исключения
        """
        data = str(DT.now())
        result = re.sub(r"\.\d+", "", data)
        print(f'\n{Fore.YELLOW}{result}{Style.RESET_ALL} >> {Fore.RED}{exception_text}{Style.RESET_ALL}')
        file_name = exception_text
        self.driver.get_screenshot_as_file(f'screen/{file_name}.png')
        self.driver.quit()

    # folder_path = "screen"
    # # Получаем список файлов в папке
    # file_list = os.listdir(folder_path)
    #
    # # Удаляем каждый файл в папке
    # for file_name in file_list:
    #     file_path = os.path.join(folder_path, file_name)
    #     os.remove(file_path)
    # print("Папка 'SCREEN' очищена от всех файлов.")