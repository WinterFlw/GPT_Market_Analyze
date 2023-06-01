import feedparser
import re
import html
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Download the vader_lexicon package
nltk.download('vader_lexicon')

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    clean_data = re.sub(clean, '', text).replace('\xa0\xa0', ' - ')
    return clean_data

"""
def get_feed_items(url, num_items):
    feed = feedparser.parse(url)
    items = feed.entries[:num_items]

    articles = []
    for item in items:
        article = {
            "title": html.unescape(item.title),
            "published": item.published,
            "summary": remove_html_tags(html.unescape(item.summary))
        }
        articles.append(article)
    return articles
"""

def get_feed_items(url, num_items):
    feed = feedparser.parse(url)
    items = feed.entries[:num_items]

    articles = []
    for item in items:
        summary = remove_html_tags(html.unescape(item.summary))
        
        # Split the summary into parts by ' - ' but only at the last occurrence
        summary_parts = summary.rsplit(' - ', 1)
        if len(summary_parts) > 1:  # If there is a part to ignore
            summary = summary_parts[0]  # Keep only the first part

        article = {
            "title": html.unescape(item.title),
            "published": item.published,
            "summary": summary
        }
        articles.append(article)
    return articles

def analyze_sentiment(article):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(article['summary'])
    return sentiment_scores

def get_kr_article(kr_search_name, start, end):
    kr_ssl_url = f'https://news.google.com/news?hl=ko&gl=kr&ie=UTF-8&q={kr_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(kr_ssl_url, 50)

    print("Korean")
    print(len(articles), "개")
    for article in articles:
        sentiment_scores = analyze_sentiment(article)
        print(article, sentiment_scores)
    
    return articles

def get_us_article(us_search_name, start, end):
    us_ssl_url = f'https://news.google.com/news?hl=eg&gl=us&ie=UTF-8&q={us_search_name}+after:{start}+before:{end}&output=rss'
    articles = get_feed_items(us_ssl_url, 50)

    print("English")
    print(len(articles), "개")
    for article in articles:
        sentiment_scores = analyze_sentiment(article)
        print(article, sentiment_scores,"\n")
    
    return articles, sentiment_scores

data = get_us_article("apple", '2023-05-08','2023-05-10')

"""
neg: 부정 sentiment score
neu: 중립 sentiment score
pos: 긍정 sentiment score
compound: 복합적 Compound sentiment score, which is a single number that represents the overall sentiment of the text.
"""