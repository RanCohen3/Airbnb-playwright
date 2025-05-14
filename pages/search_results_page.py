import logging
from pages.base_page import BasePage
import re


class SearchResultsPage(BasePage):
    LISTING_RATING_ELEMENT = "span[aria-label*='rating']"
    LISTING_LINK = "a[data-testid='card-link']"

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def validate_guests(self, adults, children):
        """
        This method validates the number of adults and children of the reservation
        :param adults: Number of expected adults
        :param children: Number of expected children
        """
        # TODO figure out why this does not work - timing issue
        # TODO extract the regex to a diff method - did not work for me
        self.page.wait_for_load_state('domcontentloaded')
        match = re.search(r'adults=(\d+)', self.page.content())
        if match:
            adults_from_page = int(match.group(1))
        else:
            raise ValueError("Could not find any data on adults guests")

        if not adults == adults_from_page:
            logging.info(f"adults entered={adults}  validation failed")
            return False

        if children:
            if not f"children={children}" in self.page.content():
                raise ValueError("Number of children validation failed")

        return True

    def extract_adults_from_page_content(self, content):
        """
        This method extract the nuber of adults guests from the page content.
        :param content: page content
        """
        # TODO regex here
        pass

    def extract_children_from_page_content(self, content):
        # TODO regex here
        pass

    def validate_dates(self, checkin, checkout):
        # TODO Regex in a diff method
        check_in_match = re.search(r'check_in=([0-9]{4}-[0-9]{2}-[0-9]{2})', self.page.content())
        if check_in_match:
            check_in_date = check_in_match.group(1)
        else:
            raise ValueError("Could not find check in date")

        check_out_match = re.search(r'check_out=([0-9]{4}-[0-9]{2}-[0-9]{2})', self.page.content())
        if check_out_match:
            check_out_date = check_out_match.group(1)
        else:
            raise ValueError("Could not find check out date")

        if checkin != check_in_date:
            logging.info(f"check in date entered: {checkin}, check in received {check_in_date}")
            return False
        if checkout != check_out_date:
            logging.info(f"check out date entered: {checkin}, check out received {check_in_date}")
            return False

        return True

    def get_listings(self):
        """
        This method returns all the listing of the results page
        """
        return self.page.locator("[itemprop='itemListElement']").all()

    def extract_details(self):
        listings = self.get_listings()
        details = []

        for listing in listings:
            title = listing.locator("meta[itemprop='name']").get_attribute("content")
            raw_price = listing.locator("span:has-text('₪')").first.text_content().strip()
            price_match = re.search(r'₪([\d,]+)', raw_price)
            # If a match is found, remove commas and convert to integer
            # TODO raise instead of None?
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

    def get_highest_rated(self, listings):
        """
        This method checks which listing has the highest ratings, and out of the
        top-rated ones, it returns the most reviewed one.
        :param listings: List of listings.
        """
        max_rated_listings = []
        max_rating = float('-inf')

        for listing in listings:
            rating = listing.get("rating")
            if rating is not None:
                # None means there is no rating yet.
                if rating > max_rating:
                    max_rating = rating
                    max_rated_listings = [listing]
                elif rating == max_rating:
                    max_rated_listings.append(listing)

        top_listing = None
        max_reviews = -1

        for max_listing in max_rated_listings:
            reviews = max_listing.get("reviews")
            if reviews > max_reviews:
                max_reviews = reviews
                top_listing = max_listing

        return top_listing

    def get_cheapest(self, listings):
        min_listing = None
        min_price = float('inf')

        for listing in listings:
            if listing["price"] < min_price:
                min_price = listing["price"]
                min_listing = listing

        return min_listing

    def click_on_listing(self, listing):
        """
        FInd and click on a listing to view its details.
        :param listing: listing to view.
        """
        self.logger.info(f"Clicking on listing: {listing['title']}")

        # Find the locator that matches the listing by its nth index (from the list of itemListElement)
        listings_locator = self.page.locator("[itemprop='itemListElement']")

        # Loop through the listings and find the matching one by title or other identifiers
        for idx in range(listings_locator.count()):
            # Use the nth locator to get the listing at the current index
            listing_locator = listings_locator.nth(idx)

            # Extract the title of the listing and compare it with the provided title
            title_element = listing_locator.locator("meta[itemprop='name']").get_attribute("content")
            # listing_title = title_element.inner_text()

            if title_element == listing["title"]:
                # Click on the listing if titles match
                self.logger.info(f"Found matching listing: {listing['title']}")
                listing_locator.click()
                break
        else:
            # If no matching listing is found, log an error
            self.logger.error(f"Listing with title '{listing['title']}' not found.")
            raise Exception(f"Listing with title '{listing['title']}' not found.")

        # Wait for the page to load after clicking
        # self.page.wait_for_load_state("networkidle")