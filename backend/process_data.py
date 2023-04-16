import openai

from .make_file.get_API import *
from .make_file.get_foldername import *

from .make_file.get_FRED import*
from .make_file.get_current import*
from .make_file.get_stock import*

OPENAI_API_KEY = Get_GPT_API_KEY()

openai.api_key = OPENAI_API_KEY
openai.Model.list()

def read_csv_data(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def get_market_data(folder_name):
    os.chdir('/workspace/GPT_Market_Analyze')
    
    try:
        stock_dataset = read_csv_data(f'dataset/{folder_name}/stock.csv')
    except FileNotFoundError:
        print("Warning: stock.csv not found.")
        stock_dataset = []
        
    try:
        current_dataset = read_csv_data(f'dataset/{folder_name}/current.csv')
    except FileNotFoundError:
        print("Warning: current.csv not found.")
        current_dataset = []
    
    return stock_dataset, current_dataset

def analyze_market(date, period):
    stock_dataset, current_dataset = get_market_data(date)
    market_dataset = stock_dataset + current_dataset
    market_dataset_str = "\n".join([f"{row[0]}: {row[1]}, {row[2]}%" for row in market_dataset])
    
    period_str = {
        0: "today",
        1: "this week",
        2: "this month",
    }.get(period, "this period")

    prompt = f"당신은 경제뉴스 기자이다. 주식시장의 정보를 csv파일 형태로 줄 것이다. 이를 통해 주식시황을 설명해주면 된다. 티커는 설명해 줄 필요 없으며, 뉴스 스크립트를 만들어주면 된다. 특히 미국에 대해서 자세히 설명해주어야한다. S%P500,나스닥100,다우지수를 설명해주면 된다.{date} ({period_str}):\n\nMarket data:\n{market_dataset_str}\n\nAnalysis: "

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=3000,
      top_p=0.5,
      best_of=1,
      stop=None
    )

    return response.choices[0].text.strip()

def store_analysis_to_txt(date, period):
    # Define a file name
    filename = f'dataset/{date}/GPT_Analyze.txt'
    os.chdir('/workspace/GPT_Market_Analyze')
    
    # Check if the file already exists
    if os.path.exists(filename):
        print("The file already exists. Skipping analysis.")
    else:
        # If the file doesn't exist, generate the analysis
        answer = analyze_market(date, period)

        # Open the file in write mode and write the answer to it
        with open(filename, 'w') as file:
            file.write(answer)
        print("Analysis saved.")

def make_report_proto(period):
    
    if period == 0:
        folder_name, fixday, composeday, report = get_daily_data()
    elif period == 1:
        folder_name, fixday, composeday, report = get_weekly_data()
    elif period == 2:
        folder_name, fixday, composeday, report = get_monthly_data()
    else :
        print("error ouucre")
        return 1
    
    print(folder_name)
    os.chdir('/workspace/GPT_Market_Analyze')
    os.makedirs(f"dataset/{folder_name}", exist_ok=True)
    print("Folder Made.")

    stock_csv_path = f'dataset/{folder_name}/stock.csv'
    if os.path.exists(stock_csv_path):
        print("stock.csv already exists. Skipping ETF data retrieval and processing.")
    else:
        etf_data = get_etf_data()
        print(etf_data)
        etf_dataset = process_etf_data(etf_data, fixday, composeday, report)
        print("Processed ETF_Data.")
        store_stock_data_to_csv(etf_dataset, folder_name)
        print("Saved ETF_Data.")
        
        
    cur_csv_path = f'dataset/{folder_name}/current.csv'
    if os.path.exists(cur_csv_path):
        print("current.csv already exists. Skipping current data retrieval and processing.")
    else:
        c, currency_rates, currency_pairs = get_cur_data()
        print(currency_pairs)
        cur_dataset, errorcode = process_exchange_rates(c, currency_rates, currency_pairs, fixday, composeday)
        print(cur_dataset)
        
        if errorcode == 0:
            store_exchange_rates_to_csv(cur_dataset, folder_name)
            print("Saved data.")
        else:
            print("Current Data has wrong.")
        
    store_analysis_to_txt(folder_name, period)
    print("Analysed and Saved Result.")
