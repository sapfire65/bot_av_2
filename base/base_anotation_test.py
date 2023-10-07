import pytest
from base.base_page import BasePage
from page.duckduck_page import DuckduckPage
from page.avito_pages import Avito
from page.client_page import Clientpage


class BaseAnatations:
    """Создание связи методов с разных страниц"""
    base_page: BasePage
    duckduck_page: DuckduckPage
    avito_pages: Avito
    client_page: Clientpage

    @pytest.fixture(autouse=True)
    def setup_anatations(self, request, driver):

        request.cls.driver = driver
        request.cls.base_page = BasePage(driver)
        request.cls.duckduck_page = DuckduckPage(driver)
        request.cls.avito_pages = Avito(driver)
        request.cls.client_page = Clientpage(driver)

