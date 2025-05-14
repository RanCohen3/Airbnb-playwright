import logging
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)


