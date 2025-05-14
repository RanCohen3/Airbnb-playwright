import logging
from playwright.sync_api import Page


class BasePage:
    URL = "https://www.airbnb.com/"
    LANG_SWITCH_BUTTON = 'button[aria-label="בחירת שפה ומטבע"]'
    EN_BUTTON = 'a[lang="en-US"]'

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def open_page(self):
        self.page.goto(self.URL, timeout=1000 * 60)

    def wait_page_load(self):
        self.page.wait_for_load_state('domcontentloaded')

        # Sometimes JS takes time to execute, adding 5 sec delay
        self.page.wait_for_timeout(1000 * 5)

    def switch_he_to_en(self):
        if "he." in self.page.url or self.page.query_selector(self.LANG_SWITCH_BUTTON) is not None:
            language_currency_button = self.page.locator(self.LANG_SWITCH_BUTTON)
            # open dropdown
            language_currency_button.click()

            us_option = self.page.locator(self.EN_BUTTON)
            us_option.click()

    def handle_popup_if_exists(self):
        try:
            logging.info(f"Looking for popups")
            self.page \
                .wait_for_selector('div[data-testid="modal-container"]', state='visible', timeout=1000 * 10)
            self.page.query_selector('button:is([aria-label="Close"], [aria-label="סגירה"])').click()
        except Exception:
            logging.error(f"Was not able to find a popup")
