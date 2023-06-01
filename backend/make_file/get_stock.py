from .get_API import *
from .get_foldername import *
import os
import FinanceDataReader as fdr
import csv

def calculate_change_percentage(today_rate, composeday_rate):
    return round((today_rate - composeday_rate) / composeday_rate * 100, 2)

def get_etf_data():
    etf_data = {
        'stock_indices': (
            ('다우 존스', 'Dow Jones', '^DJI'),
            ('나스닥', 'Nasdaq', '^IXIC'),
            ('S&P 500', 'S&P500', '^GSPC'),
            #('CSI 300', 'CSI300', 'ASHR'),
            #('유로 스톡스 50', 'Euro Stoxx 50', '^STOXX50E'),
            #('항생지수', 'Hang Seng', '^HSI'),
            #('코스닥', 'KOSDAQ', '^KQ11'),
            #('코스피', 'KOSPI', '^KS11'),
            #('MSCI 신흥시장 지수', 'MSCI Emerging Markets', 'EEM'),
            #('닛케이', 'Nikkei', '^N225')
        ),
        'sector_etfs': (
            ('정보기술', 'Information Technology', 'XLK'),
            ('헬스케어', 'Healthcare', 'XLV'),
            ('금융', 'Finance', 'XLF'),
            ('커뮤니케이션', 'Communications', 'XLC'),
            ('소비순환주', 'Consumer Cyclical', 'XLY'),
            ('경기방어주', 'Defensive Stocks', 'XLP'),
            ('산업재', 'Industrials', 'XLI'),
            ('유틸리티', 'Utilities', 'XLU'),
            ('에너지', 'Energy', 'XLE'),
            ('리츠', 'REITs', 'XLRE'),
            ('소재', 'Materials', 'XLB'),
            ('반도체', 'Semiconductor', 'SOXX'),
            ('빅테크', 'Big Tech', 'BULZ'),
            ('배당', 'Dividend', 'SCHD'),
            ('대형 성장주', 'Large Cap Growth', 'VUG'),
            ('대형 가치주', 'Large Cap Value', 'VTV'),
            ('중형 성장주', 'Mid Cap Growth', 'IWP'),
            ('중형 가치주', 'Mid Cap Value', 'VOE'),
            ('반도체', 'Semiconductor', 'SOXX')
        ),
        'bonds_and_bond_futures': (
            ('2년 미국 국채 선물', '2-Year US Treasury Futures', 'ZT=F'),
            ('5년 미국 국채 선물', '5-Year US Treasury Futures', 'ZF=F'),
            ('10년 미국 국채 선물', '10-Year US Treasury Futures', 'ZN=F'),
            ('20년 이상 미국 국채 선물', '20+ Year US Treasury Futures', 'ZB=F')
        ),
        'cryptocurrencies': (
            ('비트코인', 'Bitcoin', 'BTC/USD'),
            ('이더리움', 'Ethereum', 'ETH/USD'),
            ('리플', 'Ripple', 'XRP/USD')
        ),

        'metals': (
            ('금', 'Gold', 'GC=F'),
            ('팔라듐', 'Palladium', 'PA=F'),
            ('플래티넘', 'Platinum', 'PL=F'),
            ('은', 'Silver', 'SI=F'),
            ('구리', 'Copper', 'CL=F')
        ),

        'energy': (
            ('브런트유', 'Brent Crude Oil', 'BZ=F'),
            ('가솔린', 'Gasoline', 'RB=F'),
            ('히팅오일', 'Heating Oil', 'HO=F'),
            ('천연가스', 'Natural Gas', 'NG=F'),
            ('WTI유', 'WTI Crude Oil', 'CL=F')
        ),

        'agriculture': (
            ('옥수수', 'Corn', 'ZC=F'),
            ('돼지', 'Lean Hogs', 'HE=F'),
            ('소', 'Live Cattle', 'LE=F'),
            ('비육우', 'Feeder Cattle', 'GF=F'),
            ('귀리', 'Oats', 'ZO=F'),
            ('쌀', 'Rough Rice', 'ZR=F'),
            ('대두유', 'Soybean Oil', 'ZL=F'),
            ('콩', 'Soybeans', 'ZS=F'),
            ('밀', 'Wheat', 'KE=F')
        ),

        'soft_commodities': (
            ('코코아', 'Cocoa', 'CC=F'),
            ('커피', 'Coffee', 'KC=F'),
            ('목화', 'Cotton', 'CT=F'),
            ('목재', 'Lumber', 'LBS=F'),
            ('오렌지주스', 'Orange Juice', 'OJ=F'),
            ('설탕', 'Sugar', 'SB=F')
        )
        }
    return etf_data

def process_etf_data(etf_data, today, composeday, report):
    etf_dataset = []
    today = today.strftime("%Y-%m-%d")
    composeday = composeday.strftime("%Y-%m-%d")
    if report != 'D':
        for sector, data in etf_data.items():
            for name, ticker in data:
                if report == 'M':
                    stock_info = fdr.DataReader(ticker, composeday, today)
                else:
                    stock_info = fdr.DataReader(ticker, composeday)
                print(name)
                if 'Close' not in stock_info.columns:
                    print(f"Error: 'Close' column not found for {ticker}. Skipping this ETF.")
                    continue
                Td_close = stock_info['Close'].iloc[0]
                Co_close = stock_info['Close'].iloc[-1]
                price_change = calculate_change_percentage(Td_close, Co_close)  # Calculate the change in percentage
                etf_dataset.append((sector, name, ticker, price_change))
    else:
        #print(etf_data.items())
        for sector, data in etf_data.items():
            for kr_name, en_name, ticker in data:
                composeday_stock_info = fdr.DataReader(ticker, composeday, composeday)
                today_stock_info = fdr.DataReader(ticker, today, today)
                print(composeday_stock_info, today_stock_info)
                if 'Close' not in composeday_stock_info.columns and 'Close' not in today_stock_info.columns:
                    print(f"Error: 'Close' column not found for {ticker}. Skipping this ETF.")
                    continue
                compo_close = composeday_stock_info['Open'].iloc[-1]
                today_close = today_stock_info['Close'].iloc[-1]
                price_change = calculate_change_percentage(compo_close, today_close)  # Calculate the change in percentage
                price = round(today_close, 2)
                etf_dataset.append((sector, kr_name, en_name, ticker, price, price_change))
    return etf_dataset

def store_stock_data_to_csv(etf_dataset, foldername):
    folder_name = foldername
    os.chdir('/workspace/GPT_Market_Analyze')
    with open(f"dataset/{folder_name}/stock.csv", mode="w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Sector", "KR_name", "EN_name","Ticker", "Price", "DAILY_CHANGE_PCT"])

        for ETFdata in etf_dataset:
            csv_writer.writerow(ETFdata)