import datetime
from zoneinfo import ZoneInfo  # 파이썬 3.9 이상 기본 탑재 시간대 모듈
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# 1. 페이지 제목 및 기본 레이아웃 설정
st.set_page_config(page_title="일별 박스오피스", layout="wide")

st.title("🎬 어제의 박스오피스")


# 2. 인증키 확인 (Secrets Vault에서 KOBIS_KEY 호출)
if "KOBIS_KEY" not in st.secrets:
    st.error(
        "🔑 **인증키 설정 필요**: Streamlit Cloud Secrets 또는 local `.streamlit/secrets.toml`에 `KOBIS_KEY`를 설정해주세요."
    )
    st.stop()

api_key = st.secrets["KOBIS_KEY"]


# 3. 한국 시간(KST) 기준 '어제' 날짜 계산 (zoneinfo 사용)
# external library(pytz) 없이 파이썬 내장 ZoneInfo를 사용하여 KST 시간대를 가져옵니다.
now_kst = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
yesterday = now_kst - datetime.timedelta(days=1)
target_dt = yesterday.strftime("%Y%m%d")  # YYYYMMDD 8자리 문자열 변환

st.write(f"📅 **조회 기준일(어제):** {yesterday.strftime('%Y년 %m월 %d일')}")


# 4. KOBIS API 데이터 호출 함수 (1시간 캐시)
@st.cache_data(ttl=3600)
def fetch_box_office(key, date_str):
    url = "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {"key": key, "targetDt": date_str}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"네트워크 통신 오류가 발생했습니다: {e}"


# API 호출 실행
data, error_msg = fetch_box_office(api_key, target_dt)


# 5. 예외 처리 및 검증 (한국어 안내)
if error_msg:
    st.error(f"⚠️ **요청 실패**: {error_msg}")
    st.info("💡 **확인해 보세요:** 인터넷 연결 상태를 확인하고 잠시 후 다시 시도해 주세요.")
    st.stop()

# 인증키 오류 발생 시 (200 OK 응답 + faultInfo)
if "faultInfo" in data:
    st.error("⚠️ **API 오류 발생 (faultInfo)**")
    st.warning(
        f"메시지: {data['faultInfo'].get('message', '알 수 없는 오류')}"
    )
    st.info(
        "💡 **확인해 보세요:** Streamlit Secrets에 입력한 KOBIS API 키가 올바른지 확인해 주세요."
    )
    st.stop()

# 응답 내 영화 목록 확인
box_office_result = data.get("boxOfficeResult", {})
daily_list = box_office_result.get("dailyBoxOfficeList", [])

# 영화 목록이 비어 있는 경우
if not daily_list:
    st.warning("⚠️ **영화 데이터가 없습니다.**")
    st.info(
        "💡 **확인해 보세요:**\n"
        "- KOBIS 시스템의 집계 지연일 수 있습니다. 잠시 후 다시 조회해 주세요.\n"
        "- 조회 대상 날짜가 올바른지 확인해 주세요."
    )
    st.stop()


# 6. 데이터 전처리 (문자열 숫자를 정수로 변환)
df = pd.DataFrame(daily_list)

numeric_cols = ["rank", "audiCnt", "audiAcc", "scrnCnt", "rankInten"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)


# 7. 1위 영화 상단 강조 화면 (지표 카드 3장)
top_1 = df.iloc[0]

st.markdown("---")
st.subheader(f"🥇 어제의 1위 영화: {top_1['movieNm']}")

col1, col2, col3 = st.columns(3)

# 전날 대비 순위 증감
rank_inten = top_1["rankInten"]
delta_text = (
    f"+{rank_inten}"
    if rank_inten > 0
    else (str(rank_inten) if rank_inten < 0 else "변동 없음")
)

with col1:
    st.metric(
        label="어제 관객수",
        value=f"{top_1['audiCnt']:,} 명",
        delta=f"순위 변동: {delta_text}",
    )

with col2:
    st.metric(label="누적 관객수", value=f"{top_1['audiAcc']:,} 명")

with col3:
    st.metric(label="상영 스크린수", value=f"{top_1['scrnCnt']:,} 개")

st.markdown("---")


# 8. 상위 5편 관객수 막대그래프 시각화
st.subheader("📊 관객수 상위 5개 영화")

top_5_df = df.head(5).copy()

fig = px.bar(
    top_5_df,
    x="movieNm",
    y="audiCnt",
    text="audiCnt",
    labels={"movieNm": "영화명", "audiCnt": "어제 관객수"},
    title="상위 5위 일별 관객수",
)

fig.update_traces(texttemplate="%{text:,}명", textposition="outside")
fig.update_layout(yaxis_title="관객수(명)", xaxis_title="", height=400)

st.plotly_chart(fig, use_container_width=True)


# 9. 박스오피스 전체 순위 표 출력
st.subheader("📋 어제 박스오피스 순위 목록")

display_df = df[
    ["rank", "movieNm", "openDt", "audiCnt", "audiAcc", "scrnCnt"]
].copy()
display_df.columns = [
    "순위",
    "영화명",
    "개봉일",
    "어제 관객수",
    "누적 관객수",
    "스크린수",
]

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "어제 관객수": st.column_config.NumberColumn(format="%d명"),
        "누적 관객수": st.column_config.NumberColumn(format="%d명"),
        "스크린수": st.column_config.NumberColumn(format="%d개"),
    },
)
