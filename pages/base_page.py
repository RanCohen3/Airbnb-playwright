import logging
from playwright.sync_api import Page


class BasePage:
    URL = "https://www.airbnb.com/"

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def open_page(self):
        self.page.goto(self.URL, timeout=1000 * 60)

    def wait_page_load(self):
        self.page.wait_for_load_state('domcontentloaded')

        # Sometimes JS takes time to execute, adding 5 sec delay
        self.page.wait_for_timeout(1000 * 5)

