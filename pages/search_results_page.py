import logging
from pages.base_page import BasePage
import re


class SearchResultsPage(BasePage):
    GET_LISTINGS = "div[itemprop='itemListElement']"
    LISTING_TITLE = "meta[itemprop='name']"

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_listings(self):
        """
        This method returns all the listing of the results page
        """
        return self.page.locator(self.GET_LISTINGS).all()

    def extract_details(self):
        self.wait_page_load()
        listings = self.get_listings()
        details = []
        logging.info(f"found {len(listings)} listings")

        for listing in listings:
            title = listing.locator(self.LISTING_TITLE).get_attribute("content")
            raw_price = listing.locator("span:has-text('₪')").first.text_content().strip()
            price_match = re.search(r'₪([\d,]+)', raw_price)
            # If a match is found, remove commas and convert to integer
            price = int(price_match.group(1).replace(',', '')) if price_match else None

            # Get listing rating
            rating_span = listing.locator('span[aria-hidden="true"]', has_text=r'(')
            if rating_span.count() > 0:
                rating_text = rating_span.first.text_content()

                # extracting rating and reviews
                match = re.search(r'([\d.]+) \((\d+)\)', rating_text)
                if match:
                    rating = float(match.group(1))
                    reviews = int(match.group(2))
                else:
                    raise Exception(f"Could not find rating for the listing: {title}")
            else:
                rating, reviews = None, None

            link_element = listing.locator("a[aria-labelledby]").first
            link_url = link_element.get_attribute("href") if link_element.count() > 0 else ""
            full_url = f"{self.page.url} + {link_url}"

            details.append({
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "url": full_url,
                "listing": listing
            })
        return details
