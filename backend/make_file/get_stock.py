from .get_API import *
from .get_foldername import *

import FinanceDataReader as fdr
import yfinance as yf


def calculate_change_percentage(today_rate, composeday_rate):
    return round((today_rate - composeday_rate) / composeday_rate * 100, 2)

def get_etf_data():
    etf_data = [
        ("미국", "VTI"),("일본","EWJ"),("유로존","EZU"),("대한민국", "EWY"), ("신흥국","EEM"),
        ("S&P500", "VOO"), ("나스닥100", "QQQ"), ("다우", "DIA"), ("VIX","VXX"),
        ("정보기술", "XLK"), ("헬스케어", "XLV"), ("금융", "XLF"), ("커뮤니케이션", "XLC"),
        ("소비순환재", "XLY"), ("경기방어주", "XLP"), ("산업재", "XLI"), ("유틸리티", "XLU"),
        ("에너지", "XLE"), ("리츠", "XLRE"), ("소재", "XLB"), ("반도체", "SOXX"), ("빅테크", "BULZ"),
        ("배당", "SCHD"), ("대형성장", "VUG"), ("중형성장", "IWP"), ("대형가치", "VTV"), ("중형가치", "VOE"),
        ("미국단기 채권", "SHY"),("미국중기 채권", "IEF"),("미국장기 채권", "TLT")
    ]
    return etf_data

def etf_korean_to_english():
    return {
        '미국': 'USA',
        '일본': 'Japan',
        '유로존': 'Eurozone',
        '대한민국': 'South Korea',
        '신흥국': 'Emerging Markets',
        'S&P500' : 'S&P500',
        '나스닥100' : 'Nasdaq100',
        '다우' : 'dow',
        'VIX':'VIX',
        '정보기술':'Information Technology',
        '헬스케어':'Healthcare',
        '금융':'Finance',
        '커뮤니케이션':'Communications',
        '소비순환재':'Consumer Circular Goods',
        '경기방어주':'Defensive Stocks',
        '산업재':'Industrials',
        '유틸리티':'Utilities',
        '에너지':'Energy',
        '리츠':'REITs',
        '소재':'Materials',
        '반도체':'Semiconductor',
        '빅테크':'Big Tech',
        '배당':'Dividend',
        '대형성장':'Mass Growth',
        '중형성장':'Medium Growth',
        '대형가치':'Mass Value',
        '중형가치':'Medium Value',
        '미국단기 채권':'US short-term bonds',
        '미국중기 채권':'미국중기 채권',
        '미국장기 채권':'미국장기 채권',
    }

def process_etf_data(etf_data, today, composeday, report):        
    etf_dataset = []
    today = today.strftime("%Y-%m-%d")
    composeday = composeday.strftime("%Y-%m-%d")
    
    if report != 'D' :
        for name, ticker in etf_data:
            if report == 'M':
                stock_info = fdr.DataReader(ticker,composeday, today)
            else:
                stock_info = fdr.DataReader(ticker,composeday)
            print(stock_info)
            if 'Close' not in stock_info.columns:
                print(f"Error: 'Close' column not found for {ticker}. Skipping this ETF.")
                continue
            OPEN = stock_info['Open'].iloc[0]
            CLOSE = stock_info['Close'].iloc[-1]
            price_change = calculate_change_percentage(OPEN, CLOSE)  # Calculate the change in percentage
            etf_dataset.append((name, ticker, price_change))
            
    else:
        for name, ticker in etf_data:
            composeday_stock_info = fdr.DataReader(ticker,composeday,composeday)
            today_stock_info = fdr.DataReader(ticker,today,today)
            print(composeday_stock_info, today_stock_info)
            if 'Close' not in composeday_stock_info.columns and 'Close' not in today_stock_info.columns:
                print(f"Error: 'Close' column not found for {ticker}. Skipping this ETF.")
                continue
            compo_close = composeday_stock_info['Open'].iloc[-1]
            today_close = today_stock_info['Close'].iloc[-1]
            price_change = calculate_change_percentage(compo_close, today_close)  # Calculate the change in percentage
            etf_dataset.append((name, ticker, price_change))
    return etf_dataset

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

def store_stock_data_to_csv(etf_dataset, foldername):
    folder_name = foldername
    os.chdir('/workspace/GPT_Market_Analyze')
    with open(f"dataset/{folder_name}/stock.csv", mode="w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Sector", "Ticker", "DAILY_CHANGE_PCT"])
        
        for ETFdata in etf_dataset:
            csv_writer.writerow(ETFdata)