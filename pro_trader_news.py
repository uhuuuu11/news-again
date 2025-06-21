import streamlit as st
from gnews import GNews
from textblob import TextBlob
import feedparser
from datetime import datetime
import pytz

# ========== CONFIG ==========
st.set_page_config(page_title="Pro Trader News Alerts", layout="wide")
st.title("🚨 Pro Trader Market News Dashboard")

CATEGORIES = {
    "Macro/Political": [
        "fed", "inflation", "interest rate", "election", "war", "gdp",
        "unemployment", "recession", "cpi", "conflict", "debt"
    ],
    "Crypto Regulation": [
        "crypto", "bitcoin", "ethereum", "regulation", "sec", "binance", 
        "coinbase", "etf", "ban", "law", "mi ca"
    ],
    "Tech": [
        "ai", "chip", "nvidia", "semiconductor", "cyber", "hacker", 
        "apple", "microsoft", "cloud", "openai", "intel", "quantum"
    ],
    "Market Movers": [
        "earnings", "profit", "merger", "acquisition", "upgrade", 
        "downgrade", "buyback", "ipo", "layoffs"
    ]
}
URGENT_KEYWORDS = [
    "crisis", "emergency", "ban", "lawsuit", "default", "collapse", 
    "arrest", "explosion", "attack", "sanction", "hack", "raid"
]

# ========== FETCH NEWS ==========

@st.cache_data(ttl=60)
def fetch_gnews():
    gn = GNews(language='en', country='US', max_results=50)
    return [{"title": n['title'], "url": n['url'], "source": "GNews"} for n in gn.get_top_news()]

@st.cache_data(ttl=60)
def fetch_rss(url, source_name):
    parsed = feedparser.parse(url)
    return [{"title": e.title, "url": e.link, "source": source_name} for e in parsed.entries]

# Combine all sources
def get_all_news():
    all_news = []
    all_news += fetch_gnews()
    all_news += fetch_rss("https://www.forexlive.com/feed/", "Forexlive")
    all_news += fetch_rss("https://cryptopanic.com/feed/", "CryptoPanic")
    return all_news

# ========== ANALYSIS TOOLS ==========

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Bullish 🔺", "green"
    elif polarity < -0.1:
        return "Bearish 🔻", "red"
    else:
        return "Neutral ⚪", "gray"

def match_category(title):
    for cat, keywords in CATEGORIES.items():
        if any(k in title.lower() for k in keywords):
            return cat
    return "Other"

def is_urgent(title):
    return any(k in title.lower() for k in URGENT_KEYWORDS)

# ========== SIDEBAR FILTERS ==========

st.sidebar.header("⚙️ Filters")
active_cats = st.sidebar.multiselect("News Categories", list(CATEGORIES.keys()), default=list(CATEGORIES.keys()))
only_urgent = st.sidebar.checkbox("🔴 Urgent Only", False)

# ========== DISPLAY ==========

news_items = get_all_news()
filtered = []

for item in news_items:
    title = item['title']
    url
