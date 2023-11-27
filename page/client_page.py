from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from random import uniform, randint
from datetime import datetime as DT
from base.base_page import BasePage
from colorama import Fore, Style


class Clientpage(BasePage):
    """Методы страницы клиента поисковика"""

    my_exception_count = 0

    # Элементы взаимодействия с объявлением
    LEFT_IMAGE_FRAME = '//div[@data-marker="image-frame/left-button"]'
    RIGHT_IMAGE_FRAME = '//div[@data-marker="image-frame/right-button"]'
    ADD_TO_FAVORITES = '//div[@class="style-header-add-favorite-M7nA2"]'
    IN_FAVORITES = '//div[@class="style-header-add-favorite-M7nA2"]/button[@data-is-favorite="true"]'
    ADD_TO_NOTES = '(//button[@class="desktop-usq1f1"])[2]'
    SHOW_PHONE = '//button[@data-marker="item-phone-button/card"]'
    STATUS_DOCUMENTS = '//div[@data-marker="badge-23"]'
    SHOWING_THE_MAP = '//div[@class="style-item-map-control-X1Oqc"]'
    ANNOUNCEMENT_TEXT = '(//div[@data-marker="item-view/item-description"]/child::*)'  # текст в объявлении

    # Блок звонков
    WITHOUT_CALLS = '//span[@class="messenger-button-onboardingButtonText-vzjCr"]'
    POP_UP_PHONE = '//img[@data-marker="phone-popup/phone-image"]'
    CLOSED_POP_UP_PHONE = '(//div[@data-marker="item-popup/popup"]/child::*)[1]'
    NUMBR_AFTER_CLOSING_THE_WINDOW = '//img[@class="button-phone-image-LkzoU button-phone-image_card-MvwUd"]'

    # Картинка на полный экран
    OPEN_IMAGES_FULL_SCREEN = '//div[@class="image-frame-wrapper-_NvbY"]'
    CLOSE_IMAGES_FULL_SCREEN = '//div[@class="styles-cross-jE1a2"]'
    BUTON_GO_RIGHT = '(//button[@class="styles-control-button-OuAYU"])[2]'
    BUTON_GO_LEFT = '(//button[@class="styles-control-button-OuAYU"])[1]'
    MINI_PICTURES = '//div[@data-marker="extended-image-preview/item"]'

    # Блок карта
    LINC_MAP = '//div[@class="style-item-map-control-X1Oqc"]'
    MAP = '//div[@class="map-root-Jj6f4"]'
    MAP_GEO_LOCATION = '//button[@data-marker="map-my-geolocation"]'
    MAP_ZOOM_IN = '//button[@data-marker="map-zoom-button_in"]'
    MAP_ZOOM_OUT = '//button[@data-marker="map-zoom-button_out"]'





    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver
        self.wite = WebDriverWait(driver, 15, 1)

    def click_show_phone_button(self):
        """
        Клик по кнопке Показать телефон и закрыть окно через рандомное время.
        Если пользователь закрыл функцию звонков, выдавать сообщение: режим звонков - отключен
        """

        if self.find(('xpath', self.SHOW_PHONE)):
            # Если возможность позвонить есть
            self.click_obj(('xpath', self.SHOW_PHONE))

            print(f'{Fore.YELLOW}Режим звонков:{Style.RESET_ALL}{Fore.CYAN} Включен, (номер виден){Style.RESET_ALL}')
            self.random_delay(2, 7)


            if self.find(('xpath', self.POP_UP_PHONE)):
                # Клик и ожидаемый результат после клика
                self.click_obj(('xpath', self.CLOSED_POP_UP_PHONE))
                self.find(('xpath', self.NUMBR_AFTER_CLOSING_THE_WINDOW))
        else:
            print(f'{Fore.YELLOW}Режим звонков:{Style.RESET_ALL}{Fore.CYAN} ОТКЛЮЧЕН{Style.RESET_ALL}')

        # Скрол в верх
        for k in range(30):
            self.driver.execute_script("window.scrollBy(0, -50);")
            self.random_delay(.1, .3)

    def click_add_too_favorites(self, enable_value: int =  0):
        """Клик по кнопке добавление в избранное и убеждаемся, что действительно добавлено после клика

        Params:
            enable__value: int - значение от 1 - 10. Чем выше значение тем чаще срабатывает функция.
        """
        if randint(1, 10) >= enable_value:
            self.random_delay(.5, 1.5)
            self.click_obj(('xpath', self.ADD_TO_FAVORITES), message='Кнопка лайка не нажата')
            self.random_delay(1.0, 3.0)

            self.find(('xpath', self.IN_FAVORITES))
            print(f'{Fore.YELLOW}В избранное:{Style.RESET_ALL}{Fore.CYAN} добавлено{Style.RESET_ALL}')

    def read_ad_text(self):
        # self.open('https://www.avito.ru/moskva/predlozheniya_uslug/razrabotka_logotipa_firmennyy_stil_2919373342')

        """Симуляция прочтения текста объявления (в низ / вверх)
        - проверяем видимость блока с описанием объявления
        - получаем количество элементов в блоке описания (строки)
        - через рандомное время имитируем скролл. Перемещаясь от объекта к обьекту.
        """

        self.find(('xpath', self.ANNOUNCEMENT_TEXT))
        # скрол к блоку с текстом в низ
        for k in range(23):
            self.driver.execute_script("window.scrollBy(5, 50);")
            self.random_delay(.1, .5)

        count_elements_in_locator = self.driver.find_elements('xpath', self.ANNOUNCEMENT_TEXT)
        # Скролл вниз
        for i in range((len(count_elements_in_locator))):
            self.driver.execute_script("return arguments[0].scrollIntoView();", count_elements_in_locator[i])
            self.random_delay(1.8, 5.0)

        # Скролл вниз по элементам текста
        for i in range((len(count_elements_in_locator))):
            self.driver.execute_script("return arguments[0].scrollIntoView();", count_elements_in_locator[-(i + 1)])
            self.random_delay(0.1, .9)

        # Скрол в верх
        for k in range(30):
            self.driver.execute_script("window.scrollBy(10, -50);")
            self.random_delay(.1, .3)

        print(f'{Fore.YELLOW}Блок описания:{Style.RESET_ALL}{Fore.CYAN} прочитали{Style.RESET_ALL}')

    def serch_in_map(self):
        # self.open('https://www.avito.ru/moskva/predlozheniya_uslug/graficheskiy_dizayner._vyveski._bannery._plakaty_3034741420')

        self.random_delay(1.0, 4)

        # скрол к блоку с текстом в низ
        for k in range(18):
            self.driver.execute_script("window.scrollBy(15, 50);")

            self.random_delay(.1, .6)

        self.click_obj(('xpath', self.LINC_MAP))
        self.find(('xpath', self.MAP))
        print(f'{Fore.YELLOW}Карта:{Style.RESET_ALL}{Fore.CYAN} открыта{Style.RESET_ALL}')

        # Zoom in
        for _ in range(randint(2, 6)):
            self.random_delay(.3, 1.5)
            self.click_obj(('xpath', self.MAP_ZOOM_IN))

        # Zoom out
        for _ in range(randint(2, 4)):
            self.random_delay(.2, .7)
            self.click_obj(('xpath', self.MAP_ZOOM_OUT))

        self.random_delay(.2, .7)

        # Скрол в верх
        for k in range(30):
            self.driver.execute_script("window.scrollBy(0, -50);")
            self.random_delay(.1, .3)

        self.random_delay(1, 3)

    def view_pictures(self):

        # self.open('https://www.avito.ru/moskva/predlozheniya_uslug/graficheskiy_dizayner._vyveski._bannery._plakaty_3034741420')
        """Просмотр картинок в полноэкранном режиме + рандомизация"""

        def goo_click_right_button():
            all_pics = len(self.wite.until(EC.visibility_of_all_elements_located(('xpath', self.MINI_PICTURES))))

            try:
                self.find(('xpath', self.BUTON_GO_RIGHT))
            except TimeoutException:
                if self.my_exception_count != 3:
                    self.click_obj(('xpath', self.CLOSE_IMAGES_FULL_SCREEN))
                    self.random_delay(1.3, 4)
                    view_pictures(self)
                    self.my_exception_count += 1

            for _ in range((all_pics) - 1):
                self.click_obj(('xpath', self.BUTON_GO_RIGHT))
                self.random_delay(.2, 3)

        self.random_delay(1.3, 4)
        self.click_obj(('xpath', self.OPEN_IMAGES_FULL_SCREEN))
        self.random_delay(1.0, 4)

        goo_click_right_button()  # последовательный просмотр картинок стрелкой вправо

        limit = randint(2, 5)
        self.click_on_objects_after_random_time((self.MINI_PICTURES))
        self.random_delay(2, 5)
        self.click_obj(('xpath', self.CLOSE_IMAGES_FULL_SCREEN))
        self.random_delay(1.0, 4)

