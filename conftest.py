import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from get_user_agent_pls import fetch_user_agent
from colorama import Fore, Style


@pytest.fixture(scope='function', autouse=True)
def driver(request):
    # Генерация случайного user-agent
    ua_string = fetch_user_agent()

    print(f'\n{Fore.GREEN}user-agent: {ua_string} {Style.RESET_ALL}')

    # Опции запуска Chrome webdriver
    chrome_options = Options()

    # Подмена юзер агента на рандомный
    chrome_options.add_argument(f'--user-agent={ua_string}')

    """блок отвечает за отключение обнаружения автоматизации"""
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--incognito')

    """Дополнительные настройки"""
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--homedir=/tmp")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    request.cls.driver = driver
    yield driver
    driver.quit()


# def driver(request):
#     import time
#     import undetected_chromedriver as uc
#     from undetected_chromedriver import Chrome
#
#     ua = fetch_user_agent()
#     print(ua)
#
#     chrome_options = uc.ChromeOptions()
#     chrome_options.add_argument(f'--user-agent={ua}')
#     # opts.add_argument('--headless=new')
#     chrome_options.add_argument('--disable-extensions')
#     chrome_options.add_argument('--disable-logging')
#     chrome_options.add_argument('--log-level=3')
#     chrome_options.add_argument('--start-maximized')
#     chrome_options.add_argument('--disable-notifications')
#     chrome_options.add_argument("--disable-gpu")
#
#     """блок отвечает за отключение обнаружения автоматизации"""
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_argument("--homedir=/tmp")
#
#     chrome_options.add_argument("--ignore-certificate-errors")
#     chrome_options.add_argument("--ignore-ssl-errors")
#     chrome_options.add_argument("--ignore-certificate-errors-spki-list")
#
#
#
#
#
#     driver = Chrome(use_subprocess=True, options=chrome_options)
#     request.cls.driver = driver
#     yield driver
#     driver.quit()















