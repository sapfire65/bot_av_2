import pytest
import os
from time import sleep
from base.base_anotation_test import BaseAnatations



class TestStartScript(BaseAnatations):

    def test_start_avito_bot(self):
        self.duckduck_page.open_page_duckduck()
        self.duckduck_page.way_to_avito()
        self.avito_pages.logo_click()
        self.avito_pages.localization_switching('Москва')
        self.avito_pages.input_serch_avito('Графический дизайнер')
        self.avito_pages.click_serch_button()
        self.avito_pages.ad_search('Графический дизайнер. Вывески. Баннеры. Плакаты')

        self.client_page.read_ad_text()
        self.client_page.view_pictures()
        self.client_page.serch_in_map()
        self.client_page.click_show_phone_button()
        # self.client_page.click_add_too_favorites()

        sleep(5)

