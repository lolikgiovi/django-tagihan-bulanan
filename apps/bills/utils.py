from datetime import date, timedelta

from django.utils import timezone


def calculate_next_payment_date(payment_day, reference_date=None):
    """
    Calculate the next payment date based on a payment day.

    Args:
        payment_day (int): The day of the month when payment is due
        reference_date (date, optional): The reference date to calculate from. Defaults to today.

    Returns:
        date: The next payment due date
    """
    # Use today if no reference date is provided
    if reference_date is None:
        reference_date = timezone.now().date()

    # Determine if the payment is for this month or next month
    if payment_day > reference_date.day:  # Still upcoming this month
        next_month = reference_date.month
        next_year = reference_date.year
    else:  # Already passed this month, schedule for next month
        next_month = reference_date.month + 1 if reference_date.month < 12 else 1
        next_year = (
            reference_date.year
            if reference_date.month < 12
            else reference_date.year + 1
        )

    # Handle month length issues
    return adjust_payment_day(next_year, next_month, payment_day)


def adjust_payment_day(year, month, payment_day):
    """
    Adjust payment day to be valid for the given month, handling cases like Feb 30.

    Args:
        year (int): The year
        month (int): The month (1-12)
        payment_day (int): The preferred payment day

    Returns:
        date: A valid date with the payment day adjusted if necessary
    """
    # Handle month length issues
    try:
        return date(year, month, payment_day)
    except ValueError:
        # If the day is invalid for the month, use the last valid day
        if month == 2:  # February
            # Check for leap year
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                payment_day = min(payment_day, 29)
            else:
                payment_day = min(payment_day, 28)
        elif month in [4, 6, 9, 11]:  # 30-day months
            payment_day = min(payment_day, 30)

        return date(year, month, payment_day)
