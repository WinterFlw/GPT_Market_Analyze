from .get_API import *
from .get_foldername import *

from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter

def calculate_change_percentage(today_rate, composeday_rate):
    return round((today_rate - composeday_rate) / composeday_rate * 100, 2)

def get_cur_data():
    c = CurrencyConverter()
    currency_rates = CurrencyRates()

    currency_pairs = [
        ("USD/KRW", "USD", "KRW"),
        ("JPY/KRW", "JPY", "KRW"),
        ("EUR/KRW", "EUR", "KRW"),
        ("CNY/KRW", "CNY", "KRW"),
        ("CAD/KRW", "CAD", "KRW"),
        ("USD/CNY", "USD", "CNY"),
        ("USD/EUR", "USD", "EUR")
    ]
    
    return c, currency_rates, currency_pairs

def process_exchange_rates(c, currency_rates, currency_pairs, today, composeday):
    
    cur_dataset = []
    errorcode = 0
    for pair, from_currency, to_currency in currency_pairs:
        try:
            today_rate = round(currency_rates.get_rate(from_currency, to_currency, today) * (1 if from_currency != 'JPY' else 100), 2)
            composeday_rate = round(currency_rates.get_rate(from_currency, to_currency, composeday) * (1 if from_currency != 'JPY' else 100), 2)
        except RatesNotAvailableError:
            print("Currency Rates Source Not Ready")
            today_rate = 1
            composeday_rate = 1
            errorcode = 1
        change = calculate_change_percentage(today_rate, composeday_rate)
        cur_dataset.append((pair, today_rate, change))
    
    return cur_dataset, errorcode
            
def store_exchange_rates_to_csv(cur_dataset, foldername):
    folder_name = foldername
    os.chdir('/workspace/GPT_Market_Analyze')
    with open(f"dataset/{folder_name}/current.csv", mode="a", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["CURRENT", "PRICE", "DAILY_CHANGE_PCT"])  # 헤더 행 작성

        for CRTdata in cur_dataset:
            csv_writer.writerow(CRTdata)  # 각 환율 데이터 행 작성