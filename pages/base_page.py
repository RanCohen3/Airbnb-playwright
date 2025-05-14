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

    def switch_he_to_en(self):
        if "he." in self.page.url:
            # If not on the US site, look for the language/currency button
            language_currency_button = self.page.locator(
                "button[aria-label='בחירת שפה ומטבע']")  # Modify this selector if needed
            language_currency_button.click()  # Click to open the dropdown

            # Wait for the dropdown to open and select the US option (you'll need to find the exact selector for US)
            # us_option = page.locator("lang=en-US)")  # Change this selector if needed
            us_option = self.page.locator('a[lang="en-US"]')
            us_option.click()  # Click on English (US)

    def handle_popup_if_exists(self):
        try:
            logging.info(f"Looking for popups")
            # has_pop_up = self.page \
            #     .wait_for_selector('div[data-testid="modal-container"]', state='visible', timeout=1000 * 10)
            # if has_pop_up:
            #     logging.info("Found popup, closing..")
            self.page \
                .wait_for_selector('div[data-testid="modal-container"]', state='visible', timeout=1000 * 10)
            self.page.query_selector('button:is([aria-label="Close"], [aria-label="סגירה"])').click()
        except Exception:
            logging.error(f"Was not able to find a popup")
