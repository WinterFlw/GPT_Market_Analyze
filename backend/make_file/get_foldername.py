import pandas_market_calendars as mcal
import pytz
import calendar
from datetime import datetime, timedelta

def get_previous_business_day(date):
    # Use New York Stock Exchange calendar
    nyse = mcal.get_calendar('NYSE')
    
    # Convert the 'date' to New York time, as the NYSE calendar is based on New York time
    date = date.astimezone(pytz.timezone('America/New_York'))

    # Get all valid days from the start of 2000 till 'date'
    valid_days = nyse.valid_days(start_date='2000-01-01', end_date=date.replace(tzinfo=None))  # remove timezone info
    
    # The last valid day is the previous business day
    previous_day = valid_days[-1]

    # Convert the 'previous_day' back to 'America/New_York' timezone
    previous_day = previous_day.tz_convert(pytz.timezone('America/New_York')).to_pydatetime()

    return previous_day

def is_business_day(date):
    nyse = mcal.get_calendar('NYSE')  # Use New York Stock Exchange calendar
    return not nyse.valid_days(start_date=date.replace(tzinfo=None), end_date=date.replace(tzinfo=None)).empty  # remove timezone info

def week_of_month(date):
    first_day_of_month = date.replace(day=1)
    day_of_month = date.day
    adjusted_dom = day_of_month + first_day_of_month.weekday()
    return int((adjusted_dom - 1) / 7) + 1

def get_daily_data():
    today = datetime.now(pytz.timezone('America/New_York'))
    if not is_business_day(today):  # Pass datetime object instead of string
        return None  # If today is not a business day, return None
    fixedday = get_previous_business_day(today)
    composeday = get_previous_business_day(fixedday)

    folder_name = fixedday.strftime("%Y/%Y-%m/%Y-%m-%d")
    report = 'D'
    return folder_name, fixedday, composeday, report


def get_weekly_data():
    today = datetime.now(pytz.timezone('America/New_York'))
    if not is_business_day(today.strftime("%Y-%m-%d")):
        return None
    last_friday = get_previous_business_day(today)
    last_monday = get_previous_business_day(last_friday)
    week_of_month_now = week_of_month(last_friday)
    folder_name = last_friday.strftime(f"%Y/%Y-%m/weekly/{week_of_month_now}")
    report = 'W'
    return folder_name, last_friday, last_monday, report

def get_monthly_data():
    today = datetime.now(pytz.timezone('America/New_York'))
    if not is_business_day(today.strftime("%Y-%m-%d")):
        return None
    year = today.year
    month = today.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    first_day_of_last_month = datetime(year, month, 1, tzinfo=pytz.timezone('America/New_York'))
    first_business_day = first_day_of_last_month
    while not is_business_day(first_business_day.strftime("%Y-%m-%d")):
        first_business_day += timedelta(days=1)
    last_day_of_last_month = calendar.monthrange(year, month)[1]
    last_day_of_last_month = datetime(year, month, last_day_of_last_month, tzinfo=pytz.timezone('America/New_York'))
    last_business_day = last_day_of_last_month
    while not is_business_day(last_business_day.strftime("%Y-%m-%d")):
        last_business_day -= timedelta(days=1)
    folder_name = first_day_of_last_month.strftime("%Y/%Y-%m")
    report = 'M'
    return folder_name, last_business_day, first_business_day, report
