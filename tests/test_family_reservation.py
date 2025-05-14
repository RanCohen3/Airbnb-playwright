import pytest
from pages.home_page import AirBnbHomePage
from pages.listing_details_page import ListingDetailsPage
from pages.search_results_page import SearchResultsPage

@pytest.mark.playwright
def test_search_family(page, check_airbnb_us):
    home = AirBnbHomePage(page)
    # home.goto()
    home.accept_cookies()
    home.search("Tel Aviv", "2025-08-01", "2025-08-05", adults=2, children=1)

    results = SearchResultsPage(page)

    listing_details_page = ListingDetailsPage(page)

    results.validate_parameters(adults=2, children=1)

    listings = results.extract_details()
    highest = results.get_highest_rated(listings)
    print(f"Highest Rated Listing: {highest}")

    # find the listing and click on it
    results.click_on_listing(highest)
    # listing_details_page.wait_for_page_load()

    reservation_details = listing_details_page.get_reservation_details()

    #need to fill this
    details = {}

    # listing_url = highest['url']
    # page.goto(listing_url)

    # Click on the listing title
    # page.locator(f"text={highest['title']}").click()

    # get the reserve button
    reserve_button = page.locator('button[data-testid="homes-pdp-cta-btn"]')
    # Click the button
    reserve_button.click()
    # print("Reservation Card Details:", details)

    # page.locator("button:has-text('Reserve')").click()
    page.wait_for_load_state("networkidle")
    page.fill("input[type='tel']", "+1234567890")

    # Validate again
    confirm = page.locator("[data-testid='reservation-container']").inner_text()
    assert reservation_details in confirm