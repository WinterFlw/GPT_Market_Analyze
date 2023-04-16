from .get_API import *
from .get_foldername import *

from fredapi import Fred

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
    