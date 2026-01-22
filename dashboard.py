import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd

# --- CONFIGURATION ---
TICKER = "NQ=F"  # Nasdaq 100 Futures (Trades 23h/day)
RSS_FEEDS = {
    "CNBC Tech": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
    "Investing.com": "https://www.investing.com/rss/news_25.rss", # General market news
}

# --- 1. GET LIVE PRICE ---
def get_price():
    data = yf.Ticker(TICKER)
    # Get the latest 1-minute candle
    df = data.history(period="1d", interval="1m")
    if not df.empty:
        current_price = df['Close'].iloc[-1]
        # Calculate change from yesterday's close
        prev_close = data.info.get('previousClose', current_price)
        change = current_price - prev_close
        pct_change = (change / prev_close) * 100
        return current_price, change, pct_change
    return 0, 0, 0

# --- 2. GET NEWS HEADLINES ---
def get_news():
    news_items = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Top 5 per source
            news_items.append({
                "Title": entry.title,
                "Link": entry.link,
                "Source": source,
                "Published": entry.get('published', 'N/A')
            })
    return news_items

# --- 3. THE DASHBOARD UI ---
st.set_page_config(page_title="US100 Command Center", layout="centered")

# A. Header & Price
st.title("🦅 US100 Command Center")

if st.button('🔄 Refresh Data'):
    st.rerun()

price, change, pct = get_price()

# The "Big Number" Display
st.metric(
    label="Nasdaq 100 Futures (NQ=F)",
    value=f"{price:,.2f}",
    delta=f"{change:+.2f} ({pct:+.2f}%)"
)

st.divider()

# B. News Analysis (Placeholder for AI)
st.subheader("🤖 Sentiment Analysis")
st.info("AI STATUS: CALM. No major 3-star events detected in the last hour.")

# C. Raw Feed
st.subheader("📰 Live Wire")
news = get_news()
for item in news:
    st.markdown(f"**{item['Source']}**: [{item['Title']}]({item['Link']})")
    st.caption(f"Time: {item['Published']}")
    st.markdown("---")
