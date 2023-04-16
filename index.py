from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import csv
from datetime import datetime
from io import StringIO
from backend.process_data import make_report_proto

app = Flask(__name__)


def read_stock_csv(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    stock_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/stock.csv'
    if os.path.isfile(stock_file_path):
        with open(stock_file_path, 'r', encoding='utf-8') as f:  # Update this line
            stock_content = f.read()
        return stock_content
    else:
        return "No CSV file found for the selected date."

def read_cur_csv(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    cur_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/current.csv'
    if os.path.isfile(cur_file_path):
        with open(cur_file_path, 'r', encoding='utf-8') as f:  # Update this line
            cur_content = f.read()
        return cur_content
    else:
        return "No CSV file found for the selected date."        

def read_analyze_txt(date):
    folder_structure = date.strftime("%Y/%Y-%m/%Y-%m-%d")
    analyze_file_path = f'/workspace/GPT_Market_Analyze/dataset/{folder_structure}/GPT_Analyze.txt'

    if os.path.isfile(analyze_file_path):
        with open(analyze_file_path, 'r', encoding='utf-8') as f:
            analyze_content = f.read()
        return analyze_content
    else:
        return "No TXT file found for the selected date."
    
@app.route('/run_report', methods=['POST'])
def run_report():
    make_report_proto(0)
    return redirect(url_for('index'))    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        stock_content = read_stock_csv(date)  # Update this line
        cur_content = read_cur_csv(date)  # Add this line
        analyze_content = read_analyze_txt(date)  # Update this line
        return render_template('index.html', stock_content=stock_content, cur_content=cur_content, analyze_content=analyze_content, date=date_str)
    else:
        return render_template('index.html', stock_content=None, cur_content=None, analyze_content=None, date=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)