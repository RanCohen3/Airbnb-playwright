import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple


def get_cheapest(listings):
    """
    Get the cheapest listing
    :param listings: List of listings
    """
    min_listing = None
    min_price = float('inf')

    for listing in listings:
        if listing["price"] < min_price:
            min_price = listing["price"]
            min_listing = listing

    return min_listing


def get_highest_rated(listings):
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