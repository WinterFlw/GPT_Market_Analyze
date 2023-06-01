from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from datetime import datetime
from backend.process_data_n import make_report_proto

app = Flask(__name__)

def safe_read_csv(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            return df.to_html()  # Return DataFrame as HTML
        except pd.errors.EmptyDataError:
            return "The file is empty"
    else:
        return "The file does not exist or is empty"

def read_stock_csv(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    stock_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/stock.csv'
    return safe_read_csv(stock_file_path)

def read_cur_csv(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    cur_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/current.csv'
    return safe_read_csv(cur_file_path)

def read_analyze_txt(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    analyze_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/GPT_Analyze.txt'

    if os.path.isfile(analyze_file_path):
        with open(analyze_file_path, 'r', encoding='utf-8') as f:
            analyze_content = f.read()
        return analyze_content
    else:
        return "The file does not exist or is empty"

@app.route('/run_report', methods=['POST'])
def run_report():
    try:
        make_report_proto(0)
    except ValueError as e:
        return render_template('index.html', error=str(e))
    return redirect(url_for('index'))

    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return render_template('index.html', error="Invalid date format. Please use YYYY-MM-DD.")
        
        stock_content = read_stock_csv(date)
        cur_content = read_cur_csv(date)
        analyze_content = read_analyze_txt(date)
        
        return render_template('index.html', stock_content=stock_content, cur_content=cur_content,
                               analyze_content=analyze_content, date=date_str)

    else:
        return render_template('index.html', stock_content=None, cur_content=None, analyze_content=None, date=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
