from .get_API import *
from .get_foldername import *

from fredapi import Fred
import yfinance as yf
'''
api_key = Get_FRED_API_KEY()
fred = Fred(api_key=api_key)

start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 4, 1)

# Fetch the Federal Funds Rate (FRED series ID: FEDFUNDS) for the specified date range
federal_funds_rate = fred.get_series('FEDFUNDS', observation_start=start_date, observation_end=end_date)
'''


def save_technical_data_to_csv(federal_funds_rate, foldername):
    folder_name = foldername
    federal_funds_rate.to_csv(file_name, index=True)
    os.chdir('/workspace/Market_Analayze')
    with open(f"dataset/{folder_name}/FRED.csv", mode="a", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["CURRENT", "PRICE", "DAILY_CHANGE_PCT"])  # 헤더 행 작성

        for FREDdata in federal_funds_rate:
            csv_writer.writerow(FREDdata)  # 각 환율 데이터 행 작성
    
def get_technical_data(ticker, start_day, end_day):
    ticker = ticker
    technical_data = yf.download(ticker, start=start_day, end=end_day)

    # Calculate Moving Averages (SMA)
    technical_data['SMA20'] = technical_data['Close'].rolling(window=20).mean()
    technical_data['SMA50'] = technical_data['Close'].rolling(window=50).mean()
    technical_data['SMA200'] = technical_data['Close'].rolling(window=200).mean()

    # Calculate Bollinger Bands
    technical_data['BB_Middle'] = technical_data['Close'].rolling(window=20).mean()
    technical_data['BB_Upper'] = technical_data['BB_Middle'] + 2 * technical_data['Close'].rolling(window=20).std()
    technical_data['BB_Lower'] = technical_data['BB_Middle'] - 2 * technical_data['Close'].rolling(window=20).std()

    # Calculate RSI
    delta = technical_data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    technical_data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD
    technical_data['EMA12'] = technical_data['Close'].ewm(span=12).mean()
    technical_data['EMA26'] = technical_data['Close'].ewm(span=26).mean()
    technical_data['MACD'] = technical_data['EMA12'] - technical_data['EMA26']
    technical_data['MACD_Signal'] = technical_data['MACD'].ewm(span=9).mean()

    return technical_dataset
