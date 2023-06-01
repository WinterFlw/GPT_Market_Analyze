import pandas as pd
import os
import feedparser
import re
import html
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List
nltk.download('vader_lexicon')

def create_lists_by_sector(file_path):
    """Create a dictionary of sectors and their respective data from a CSV file."""
    df = pd.read_csv(file_path)
    grouped = df.groupby('Sector')
    lists_by_sector = {name: [tuple(x) for x in group[['KR_name', 'EN_name', 'Ticker', 'Price', 'DAILY_CHANGE_PCT']].values] for name, group in grouped}
    return lists_by_sector

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    clean_data = re.sub(clean, '', text).replace('\xa0\xa0', ' - ')
    return clean_data

def get_feed_items(url, num_items):
    """Retrieve a number of feed items from a URL."""
    feed = feedparser.parse(url)
    items = feed.entries[:num_items]
    return [{"title": html.unescape(item.title), "published": item.published, "summary": remove_html_tags(html.unescape(item.summary)).rsplit(' - ', 1)[0]} for item in items]

def get_us_article(us_search_name, start, end):
    """Retrieve articles from a specific US search name."""
    us_ssl_url = f'https://news.google.com/news?hl=eg&gl=us&ie=UTF-8&q={us_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(us_ssl_url, 5)
    print(us_search_name, "English", len(articles), "개")
    for article in articles:
        print(article, "\n")
    return articles

def analyze_sentiment(article):
    """Analyze the sentiment of an article."""
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(article['summary'])
    return sentiment_scores

def get_us_article_sen(us_search_name, start, end):
    """Retrieve articles and their sentiment scores from a specific US search name."""
    us_ssl_url = f'https://news.google.com/news?hl=eg&gl=us&ie=UTF-8&q={us_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(us_ssl_url, 50)
    print(us_search_name,"English",len(articles), "개")
    for article in articles:
        sentiment_scores = analyze_sentiment(article)
        print(article, sentiment_scores,"\n")
    return articles, sentiment_scores
            
def get_sector_article(lists_by_sector, folder_name, fixday, composeday):
    """Retrieve and save articles for a specific sector."""
    fixday_str = fixday.strftime("%Y-%m-%d")
    composeday_str = composeday.strftime("%Y-%m-%d")
    os.chdir('/workspace/GPT_Market_Analyze')

    for sector, data in lists_by_sector.items():
        sector_articles = []
        for company in data:
            articles = get_us_article(company[1].replace(" ", ""), composeday_str, fixday_str)
            article_dataset = [str(article) for article in articles]
            sector_articles.extend(article_dataset)

        with open(f"dataset/{folder_name}/sector/{sector}.txt", mode="w", newline='', encoding='utf-8') as file:
            file.write(f"{sector}\n")
            for i, article in enumerate(sector_articles, start=1):
                file.write(f"{article}\n")
