import os
import pytz
import time
import calendar
import csv
from datetime import datetime, timedelta

def get_previous_business_day(date):
    previous_day = date - timedelta(days=1)
    while previous_day.weekday() >= 5:  # Weekdays are 0-4, weekends are 5-6
        previous_day -= timedelta(days=1)
    return previous_day

def week_of_month(date):
    first_day_of_month = date.replace(day=1)
    day_of_month = date.day
    adjusted_dom = day_of_month + first_day_of_month.weekday()
    
    return int((adjusted_dom - 1) / 7) + 1

def get_daily_data():
    now = datetime.now()
    today = datetime.now()
    fixedday = get_previous_business_day(today)
    composeday = get_previous_business_day(fixedday)

    folder_name = fixedday.strftime("%Y/%Y-%m/%Y-%m-%d")
    report = 'D'
    return folder_name, fixedday, composeday, report

def get_weekly_data():
    now = datetime.now(pytz.timezone('Asia/Seoul'))
    today = now

    # Find last Friday
    if today.weekday() >= 4:  # If it's Friday or later
        last_friday = today - timedelta(days=(today.weekday() - 4))
    else:  # If it's before Friday
        last_friday = today - timedelta(days=(today.weekday() + 3))

    # Find last Monday
    last_monday = last_friday - timedelta(days=4)
    
    week_of_month_now = week_of_month(last_friday)
    folder_name = last_friday.strftime(f"%Y/%Y-%m/weekly/{week_of_month_now}")

    report = 'W'
    
    return folder_name, last_friday, last_monday, report

def get_monthly_data():
    now = datetime.now(pytz.timezone('Asia/Seoul'))
    today = now
    year = now.year
    month = now.month
    
    # Subtract one month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1

    # Get the first day of last month
    first_day_of_last_month = datetime(year, month, 1)

    # Get the first business day of last month
    first_business_day = first_day_of_last_month
    while first_business_day.weekday() >= 5:
        first_business_day += timedelta(days=1)

    # Get the last day of last month
    _, last_day_of_last_month = calendar.monthrange(year, month)
    last_day_of_last_month = datetime(year, month, last_day_of_last_month)
    
    # Get the last business day of last month
    last_business_day = last_day_of_last_month
    while last_business_day.weekday() >= 5:
        last_business_day -= timedelta(days=1)

    folder_name = first_day_of_last_month.strftime("%Y/%Y-%m")

    report = 'M'

    return folder_name, last_business_day, first_business_day, report