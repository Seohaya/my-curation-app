import streamlit as st
import feedparser
import requests
import yfinance as yf

# 화면 설정
st.set_page_config(page_title="나만의 큐레이션 앱", layout="wide")

# 왼쪽 사이드바 메뉴 
st.sidebar.title("📁 카테고리")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요:", 
    ["🏠 홈", "📰 경제 뉴스", "📝 블로그", "📺 유튜브", "📈 거시경제 & 암호화폐", "🐦 X(트위터)"]
)

# --- 1. 홈 화면 ---
if menu == "🏠 홈":
    st.title("🚀 나의 AI 큐레이션 대시보드")
    st.write("관심 있는 뉴스, 블로그, 유튜브, 그리고 시장 지표를 한눈에 확인하세요.")

# --- 2. 경제 뉴스 화면 ---
elif menu == "📰 경제 뉴스":
    st.title("📰 이코노믹리뷰 실시간 속보")
    st.write("이코노믹리뷰(Econovill) 홈페이지에 올라오는 최신 뉴스 20개를 실시간으로 가져옵니다.")
    
    if st.button("🔄 최신 뉴스 20개 불러오기"):
        with st.spinner("뉴스를 불러오는 중입니다..."):
            try:
                rss_url = "https://www.econovill.com/rss/allArticle.xml"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(rss_url, headers=headers, timeout=10)
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    st.success("최신 기사를 성공적으로 가져왔습니다!")
                    st.write("---")
                    for i, entry in enumerate(feed.entries[:20]):
                        st.markdown(f"**{i+1}. [{entry.title}]({entry.link})**")
                else:
                    st.error("뉴스를 불러올 수 없습니다. 사이트 상태를 확인해 주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# --- 3. 블로그 화면 ---
elif menu == "📝 블로그":
    st.title("📝 내 관심 블로그")
    blog_list = {
        "메르의 블로그": "ranto28", 
        "비즈카페 블로그": "bizucafe",
        "거시경제 시황": "macro_blogger",
        "한국전력 및 에너지": "kepco_blogger", 
        "KINX 및 클라우드": "kinx_blogger"        
    }
    selected_blog = st.selectbox("블로그 선택:", list(blog_list.keys()))
    if st.button("새 글 가져오기"):
        rss_url = f"https://rss.blog.naver.com/{blog_list[selected_blog]}.xml"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            st.success(f"'{selected_blog}'의 최신 글 5개를 가져왔습니다.")
            for entry in feed.entries[:5]:
                st.subheader(f"📌 {entry.title}")
                st.write(f"🔗 [원문 보기]({entry.link})")
                st.divider()
        else:
            st.warning("정보를 불러올 수 없습니다. 아이디를 확인해 주세요.")

# --- 4. 유튜브 화면 ---
elif menu == "📺 유튜브":
    st.title("📺 유튜브 채널별 최신 영상")
    youtube_channels = {
        "1. 백훈종의 전지적 비트코인 시점": "UCVu8stljjVNfYoISzDUFsbA",
        "2. 윤수목의 생존투자훈련소": "UCk0UntQHS9ShzfTBMrfSdog",
        "3. 소수몽키": "UCC3yfxS5qC6PCwDzetUuEWg",
        "4. 비욘드로스": "UC8YedDlXaHXlsoT9S7xE_sQ",
        "5. 안될공학": "UCeN2YeJcBCRJoXgzF_OU3qw",
        "6. Mark Moss": "UC9ZM3N0ybRtp44-WLqsW3iQ",
        "7. Natalie Brunell": "UCru3nlhzHrbgK21x0MdB_eg",
        "8. 자기계발 및 학습": "채널_ID_입력_6",
        "9. 부동산 및 자산관리": "채널_ID_입력_7",
        "10. 글로벌 비즈니스": "채널_ID_입력_8"
    }
    selected_channel = st.selectbox("어떤 채널의 영상을 볼까요?", list(youtube_channels.keys()))
    channel_id = youtube_channels[selected_channel]

    if st.button("🎥 최신 영상 불러오기"):
        if channel_id.startswith("채널_ID_입력"):
            st.warning("먼저 코드에서 실제 유튜브 채널 ID를 입력해 주세요.")
        else:
            try:
                youtube_rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(youtube_rss_url, headers=headers, timeout=10)
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    st.success(f"'{selected_channel}' 채널의 최신 영상 5개를 가져왔습니다.")
                    for entry in feed.entries[:5]:
                        st.subheader(f"🎬 {entry.title}")
                        st.caption(f"📅 게시일: {entry.published[:10]}")
                        st.write(f"🔗 [영상 바로가기]({entry.link})")
                        st.divider()
                else:
                    st.error("채널 정보를 가져올 수 없습니다. ID가 정확한지 확인해 주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# --- 5. 거시경제 & 암호화폐 대시보드 ---
elif menu == "📈 거시경제 & 암호화폐":
    st.title("📈 거시경제 & 유동성 대시보드")
    
    if st.button("🔄 시장 지표 업데이트"):
        with st.spinner("야후 파이낸스 데이터를 불러오는 중입니다..."):
            st.subheader("📊 주요 시장 지표")
            yf_tickers = {
                "나스닥 100": "^NDX",
                "S&P 500": "^GSPC",
                "미국채 10년 금리": "^TNX",
                "비트코인": "BTC-USD",
                "이더리움": "ETH-USD",
                "WTI 유가": "CL=F",
                "달러 인덱스": "DX-Y.NYB",
                "VIX 지수": "^VIX",
                "MOVE 지수": "^MOVE"
            }
            cols_yf = st.columns(3)
            for i, (name, symbol) in enumerate(yf_tickers.items()):
                col = cols_yf[i % 3]
                try:
                    ticker_data = yf.Ticker(symbol)
                    hist = ticker_data.history(period="5d")
                    if len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        pct_change = (change / prev_price) * 100
                        
                        if "금리" in name:
                            price_str = f"{current_price:.2f}%"
                        elif "비트코인" in name or "이더리움" in name or "유가" in name:
                            price_str = f"${current_price:,.2f}"
                        else:
                            price_str = f"{current_price:,.2f}"
                            
                        change_str = f"{change:.2f} ({pct_change:.2f}%)"
                        col.metric(label=name, value=price_str, delta=change_str)
                    else:
                        col.metric(label=name, value="데이터 지연")
                except Exception:
                    col.metric(label=name, value="조회 실패") # 이 부분의 오타가 완벽히 수정되었습니다!

    st.write("---")
    st.subheader("🏦 미 연준(FRED) 유동성 차트 보러가기")
    col1, col2 = st.columns(2)
    with col1:
        st.info("📉 **[미 재무부 TGA 잔고 확인하기](https://fred.stlouisfed.org/series/WTREGEN)**")
    with col2:
        st.info("📉 **[연준 역레포(RRP) 잔고 확인하기](https://fred.stlouisfed.org/series/RRPONTSYD)**")

# --- 6. X(트위터) 화면 (사용자 리스트 반영!) ---
elif menu == "🐦 X(트위터)":
    st.title("🐦 관심 X(트위터) 계정 바로가기")
    st.write("대신, 아래에서 계정을 선택하시면 클릭 한 번으로 새 창에서 쾌적하게 피드를 확인하실 수 있습니다.")
    st.write("---")
    
    twitter_accounts = {
        "MrMarket89": "MrMarket89",
        "도널드 트럼프": "realDonaldTrump",
        "일론 머스크": "elonmusk",
        "마이클 세일러": "saylor",
        "톰 리": "fundstrat",
        "제프 박": "dgt10011",
        "자유로운 계정 추가 4": "X_아이디_입력"
    }
    
    selected_twitter = st.selectbox("어떤 계정의 피드를 볼까요?", list(twitter_accounts.keys()))
    twitter_id = twitter_accounts[selected_twitter]

    # 직관적이고 커다란 바로가기 버튼 제공
    st.info(f"👉 **[{selected_twitter} 피드 바로가기] (https://x.com/{twitter_id})**")