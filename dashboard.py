import streamlit as st
import yfinance as yf
import feedparser
import time

# --- CONFIGURATION ---
# Force wide layout and dark theme setup
st.set_page_config(page_title="US100 Command Center", layout="wide")

# --- CUSTOM CSS (The "Black Mode" & Layout) ---
st.markdown("""
    <style>
    /* 1. Force Pitch Black Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 2. Hide standard Streamlit header/footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 3. Custom Price Ticker Styling */
    .ticker-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #111;
        padding: 10px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .main-price {
        font-size: 28px; /* Smaller than before */
        font-weight: bold;
        color: white;
        margin-right: 15px;
    }
    .price-change-green { color: #00FF00; font-size: 18px; }
    .price-change-red { color: #FF4444; font-size: 18px; }
    .currency-tag { font-size: 16px; color: #888; }
    
    /* 4. Sentiment Bars */
    .sentiment-wrapper {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
    }
    .bar {
        flex: 1;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        color: black;
        border-radius: 4px;
        font-size: 14px;
    }
    
    /* 5. Compact News List */
    .news-row {
        padding: 8px 0;
        border-bottom: 1px solid #222;
        font-size: 14px;
    }
    .news-source { color: #888; font-size: 12px; margin-right: 10px; }
    .news-link { color: #4da6ff; text-decoration: none; }
    .news-link:hover { text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FUNCTIONS ---
def get_data():
    try:
        # Fetch NQ=F (Futures) and SEK=X (USD/SEK)
        tickers = yf.Tickers("NQ=F SEK=X")
        
        # Nasdaq Data
        nq_hist = tickers.tickers['NQ=F'].history(period="1d", interval="1m")
        if not nq_hist.empty:
            price = nq_hist['Close'].iloc[-1]
            prev = nq_hist['Open'].iloc[0]
            change = price - prev
            pct = (change / prev) * 100
        else:
            price, change, pct = 0, 0, 0

        # SEK Data
        sek_hist = tickers.tickers['SEK=X'].history(period="1d", interval="1m")
        sek = sek_hist['Close'].iloc[-1] if not sek_hist.empty else 0.0
        
        return price, change, pct, sek
    except:
        return 0, 0, 0, 0

def get_news():
    try:
        url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
        return feedparser.parse(url).entries[:6]
    except:
        return []

# --- MAIN APP LOGIC ---

# 1. Fetch Data
price, change, pct, sek = get_data()
news = get_news()

# 2. HEADER: Live Price Ticker (Custom HTML)
color_class = "price-change-green" if change >= 0 else "price-change-red"
sign = "+" if change >= 0 else ""

st.markdown(f"""
<div class="ticker-container">
    <div>
        <span style="color:#888; font-size:14px; margin-right:10px;">US100 FUTURES</span>
        <span class="main-price">{price:,.2f}</span>
        <span class="{color_class}">{sign}{change:.2f} ({sign}{pct:.2f}%)</span>
    </div>
    <div>
        <span style="color:#888; font-size:14px; margin-right:10px;">USD/SEK</span>
        <span style="color:white; font-size:20px;">{sek:.2f} kr</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. SENTIMENT SECTION
st.caption("MARKET DRIVERS (AI SENTIMENT)")

# The 3 Colored Bars
st.markdown("""
<div class="sentiment-wrapper">
    <div class="bar" style="background-color: #4CAF50;">TECH (Bullish)</div>
    <div class="bar" style="background-color: #FFA726;">FED (Uncertain)</div>
    <div class="bar" style="background-color: #EF5350;">GEO (Risk)</div>
</div>
""", unsafe_allow_html=True)

# The AI Summary (White text)
st.markdown("""
<div style="background-color: #111; padding: 15px; border-radius: 5px; font-size: 14px; line-height: 1.6; margin-bottom: 20px; border: 1px solid #333;">
    <strong style="color: #4CAF50;">1. Tech:</strong> Nasdaq supported by pre-market strength in Semiconductor sector.<br>
    <strong style="color: #FFA726;">2. Fed:</strong> Bond yields are flat; market waiting for next week's rate decision.<br>
    <strong style="color: #EF5350;">3. Geo:</strong> Tariff headlines from Davos continue to create short-term volatility.
</div>
""", unsafe_allow_html=True)

# 4. NEWS FEED
st.caption("LIVE WIRE")
for item in news:
    st.markdown(f"""
    <div class="news-row">
        <span class="news-source">CNBC US</span>
        <a class="news-link" href="{item.link}" target="_blank">{item.title}</a>
    </div>
    """, unsafe_allow_html=True)

# 5. AUTO REFRESH LOGIC (Native)
time.sleep(30) # Wait 30 seconds
st.rerun()     # Restart the script
