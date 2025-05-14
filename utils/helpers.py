import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple


def setup_logger():
    """Set up and configure the logger"""
    logger = logging.getLogger("airbnb_tests")
    logger.setLevel(logging.INFO)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(ch)

    return logger


def generate_random_dates(min_days_ahead: int = 7, max_days_ahead: int = 30, min_stay: int = 3, max_stay: int = 7) -> \
Tuple[datetime, datetime]:
    """Generate random check-in and check-out dates

    Args:
        min_days_ahead: Minimum days ahead for check-in
        max_days_ahead: Maximum days ahead for check-in
        min_stay: Minimum length of stay
        max_stay: Maximum length of stay

    Returns:
        Tuple of (check-in date, check-out date)
    """
    # Generate random check-in date
    checkin_days_ahead = random.randint(min_days_ahead, max_days_ahead)
    checkin_date = datetime.now() + timedelta(days=checkin_days_ahead)

    # Generate random length of stay
    stay_duration = random.randint(min_stay, max_stay)

    # Calculate check-out date
    checkout_date = checkin_date + timedelta(days=stay_duration)

    return checkin_date, checkout_date


def generate_phone_number(country_prefix: str = "+1") -> str:
    """Generate a random phone number with the specified country prefix

    Args:
        country_prefix: Country code prefix for the phone number

    Returns:
        Formatted phone number string
    """
    # Generate random 10-digit number
    digits = "".join([str(random.randint(0, 9)) for _ in range(10)])

    # Format: +1 (XXX) XXX-XXXX
    formatted_number = f"{country_prefix} ({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    return formatted_number


def print_listing_comparison(highest_rated: Dict, cheapest: Dict):
    """Print a comparison between the highest rated and cheapest listings

    Args:
        highest_rated: Dictionary with highest rated listing details
        cheapest: Dictionary with cheapest listing details
    """
    print("\n" + "=" * 50)
    print("LISTING COMPARISON")
    print("=" * 50)

    print("\nHIGHEST RATED LISTING:")
    print(f"Title: {highest_rated['title']}")
    print(f"Rating: {highest_rated['rating']}")
    print(f"Price: ${highest_rated['price']}")

    print("\nCHEAPEST LISTING:")
    print(f"Title: {cheapest['title']}")
    print(f"Rating: {cheapest['rating']}")
    print(f"Price: ${cheapest['price']}")

    print("\n" + "=" * 50)