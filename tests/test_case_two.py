import logging
import pytest
from pages.home_page import AirBnbHomePage
from pages.listing_details_page import ListingDetailsPage
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger("airbnb_tests")

@pytest.mark.playwright
def test_case_two(page):
    logger.info("starting test case two")
    # 1. Navigate to airbnb homepage
    home = AirBnbHomePage(page)
    home.open_page()
    home.wait_page_load()

    # switching to english in case of hebrew
    home.switch_he_to_en()
    home.wait_page_load()

    # 2. Search for apartments
    home.handle_popup_if_exists()
    home.search("Tel Aviv", "2025-08-01", "2025-08-05", adults=2, children=1)

    # 3. Validate parameters of results
    results = SearchResultsPage(page)

    listing_details_page = ListingDetailsPage(page)

    results.validate_guests(adults=2, children=1)

    listings = results.extract_details()
    # 4. Select the highest rated result and click it
    highest = results.get_highest_rated(listings)
    print(f"Highest Rated Listing: {highest}")

    # find the listing and click on it
    results.click_on_listing(highest)
    # listing_details_page.wait_for_page_load()


    # 5. a. get reservation details from reservation card
    # TODO I didnt manage to do so
    reservation_details = listing_details_page.get_reservation_details()

    # 5. b. print the details
    details = {}

    # listing_url = highest['url']
    # page.goto(listing_url)

    # Click on the listing title
    # page.locator(f"text={highest['title']}").click()


    # 6. a. click the reserve button
    reserve_button = page.locator('button[data-testid="homes-pdp-cta-btn"]')
    # Click the button
    reserve_button.click()

    # 6. b. validate reservation details again

    # 6. c. enter a phone number with a prefix of your choice
    page.wait_for_load_state("networkidle")
    page.fill("input[type='tel']", "+1234567890")

    # Validate again
    confirm = page.locator("[data-testid='reservation-container']").inner_text()
    assert reservation_details in confirm