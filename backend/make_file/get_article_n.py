import pandas as pd
import os
import feedparser
import re
import html
from typing import List, Tuple, Dict

def create_lists_by_sector(file_path: str) -> Dict[str, List[Tuple]]:
    """Create a dictionary of sectors and their respective data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    grouped = df.groupby('Sector')
    lists_by_sector = {name: [tuple(x) for x in group[['KR_name', 'EN_name', 'Ticker', 'Price', 'DAILY_CHANGE_PCT']].values] for name, group in grouped}
    return lists_by_sector

def remove_html_tags(text: str) -> str:
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    clean_data = re.sub(clean, '', text).replace('\xa0\xa0', ' - ')
    return clean_data

def get_feed_items(url: str, num_items: int) -> List[Dict]:
    """Retrieve a number of feed items from a URL."""
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"Error retrieving feed items: {e}")
        return []
    items = feed.entries[:num_items]
    return [{"title": html.unescape(item.title), "published": item.published, "summary": remove_html_tags(html.unescape(item.summary)).rsplit(' - ', 1)[0]} for item in items]

def get_us_article(us_search_name: str, start: str, end: str) -> List[Dict]:
    """Retrieve articles from a specific US search name."""
    us_ssl_url = f'https://news.google.com/news?hl=eg&gl=us&ie=UTF-8&q={us_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(us_ssl_url, 5)
    print(us_search_name, "English", len(articles), "articles")
    for article in articles:
        print(article, "\n")
    return articles

def get_sector_article(lists_by_sector: Dict[str, List[Tuple]], folder_name: str, fixday: str, composeday: str):
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

        try:
            with open(f"dataset/{folder_name}/sector/{sector}.txt", mode="w", newline='', encoding='utf-8') as file:
                file.write(f"{sector}\n")
                for i, article in enumerate(sector_articles, start=1):
                    file.write(f"{article}\n")
        except FileNotFoundError:
            print(f"File not found: dataset/{folder_name}/sector/{sector}.txt")

    
    """
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    # Download the vader_lexicon package
    nltk.download('vader_lexicon')
    
    def analyze_sentiment(article: Dict) -> Dict:
    Analyze the sentiment of an article.
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(article['summary'])
    return sentiment_scores
    
    def get_us_article_sen(us_search_name: str, start: str, end: str) -> Tuple[List[Dict], Dict]:
    Retrieve articles and their sentiment scores from a specific US search name.
    us_ssl_url = f'https://news.google.com/news?hl=eg&gl=us&ie=UTF-8&q={us_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(us_ssl_url, 50)
    print(us_search_name,"English",len(articles), "articles")
    sentiment_scores_list = []
    for article in articles:
        sentiment_scores = analyze_sentiment(article)
        sentiment_scores_list.append(sentiment_scores)
        print(article, sentiment_scores,"\n")
    return articles, sentiment_scores_list
    
    """