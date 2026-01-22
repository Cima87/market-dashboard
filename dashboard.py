import streamlit as st
import yfinance as yf
import feedparser
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
# Auto-refresh every 30 seconds (30 * 1000 milliseconds)
st_autorefresh(interval=30 * 1000, key="dataframerefresh")

# Custom CSS for "Dark Mode" and Compact Layout
st.markdown("""
    <style>
    /* Force Black Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Compact Text for Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 24px !important; 
        color: #FFFFFF !important;
    }
    /* Remove padding to make it tight */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    /* Compact News List */
    .news-item {
        margin-bottom: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid #333;
        font-size: 14px;
    }
    a {
        color: #4da6ff;
        text-decoration: none;
    }
    /* Status Bars */
    .status-box {
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_market_data():
    # Fetch Futures (NQ=F) and Currency (USD/SEK)
    tickers = yf.Tickers("NQ=F SEK=X")
    
    # NQ Data
    nq = tickers.tickers['NQ=F'].history(period="1d", interval="1m")
    if not nq.empty:
        nq_price = nq['Close'].iloc[-1]
        nq_change = nq_price - nq['Open'].iloc[0] # Change since open
        nq_pct = (nq_change / nq['Open'].iloc[0]) * 100
    else:
        nq_price, nq_change, nq_pct = 0, 0, 0

    # SEK Data
    sek = tickers.tickers['SEK=X'].history(period="1d", interval="1m")
    if not sek.empty:
        sek_price = sek['Close'].iloc[-1]
    else:
        sek_price = 0
        
    return nq_price, nq_change, nq_pct, sek_price

def get_news():
    # Using CNBC Tech and Investing.com
    rss_url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
    feed = feedparser.parse(rss_url)
    return feed.entries[:6] # Top 6 headlines

# --- DATA FETCHING ---
nq_price, nq_change, nq_pct, sek_price = get_market_data()
news_items = get_news()

# --- LAYOUT ---

# 1. TOP ROW: Compact Price & Currency
c1, c2 = st.columns([2, 1])
with c1:
    st.metric("US100 Futures", f"{nq_price:,.0f}", f"{nq_change:+.1f} ({nq_pct:+.1f}%)")
with c2:
    st.metric("USD/SEK", f"{sek_price:.2f} kr", None)

st.markdown("---")

# 2. SENTIMENT SECTION (The 3 Bars)
st.markdown("### 🚦 Market Drivers")

col_green, col_orange, col_red = st.columns(3)

# Logic for "Fake" Sentiment (Since we don't have the AI API connected yet)
# In the future, the AI will set these variables automatically.
with col_green:
    st.markdown('<div class="status-box" style="background-color: #00FF00;">TECH (Bullish)</div>', unsafe_allow_html=True)
with col_orange:
    st.markdown('<div class="status-box" style="background-color: #FFA500;">FED (Caution)</div>', unsafe_allow_html=True)
with col_red:
    st.markdown('<div class="status-box" style="background-color: #FF4444;">GEO (Risk)</div>', unsafe_allow_html=True)

# 3. AI SUMMARY (White Text)
st.markdown("""
<div style="margin-top: 15px; font-style: italic; font-size: 14px; color: #DDDDDD;">
    1. <b>Tech:</b> Nvidia and Apple are holding gains pre-market, providing support.<br>
    2. <b>Fed:</b> Interest rate uncertainty remains high ahead of next week's meeting.<br>
    3. <b>Geo:</b> Tariff headlines from Davos are causing erratic spikes in futures.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. COMPACT NEWS FEED
st.markdown("### 📰 Live Feed")
for item in news_items:
    st.markdown(f"""
    <div class="news-item">
        <a href="{item.link}" target="_blank">{item.title}</a>
        <br><span style="color: #888; font-size: 12px;">{item.get('published', '')[0:25]}...</span>
    </div>
    """, unsafe_allow_html=True)
