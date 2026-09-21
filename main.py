import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ---------------------------------------------------------
# 1. 페이지 기본 설정
# ---------------------------------------------------------

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 어제의 박스오피스")
st.caption("KOBIS 영화관입장권통합전산망 일별 박스오피스")


# ---------------------------------------------------------
# 2. 한국 시간 기준으로 '어제' 계산하기
# ---------------------------------------------------------
# Streamlit Cloud 서버의 시간이 한국 시간이 아닐 수 있으므로
# 서버의 현재 시간을 그대로 사용하지 않고 한국 시간(KST)을 사용합니다.

KST = ZoneInfo("Asia/Seoul")

today_kst = datetime.now(KST).date()
yesterday_kst = today_kst - timedelta(days=1)

# KOBIS API가 요구하는 yyyymmdd 형식으로 변환합니다.
target_dt = yesterday_kst.strftime("%Y%m%d")

st.info(
    f"📅 조회 날짜: {yesterday_kst.strftime('%Y년 %m월 %d일')} "
    f"(한국 시간 기준)"
)


# ---------------------------------------------------------
# 3. KOBIS API 인증키 가져오기
# ---------------------------------------------------------
# 실제 인증키는 코드에 작성하지 않습니다.
# Streamlit Cloud의 Secrets에 KOBIS_KEY를 등록해 두어야 합니다.

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]
except Exception:
    st.error("🔑 KOBIS 인증키를 찾을 수 없습니다.")
    st.markdown(
        """
        **확인할 사항**
        
        - Streamlit Cloud의 **Settings → Secrets**에 들어갔는지 확인하세요.
        - Secret 이름이 정확히 `KOBIS_KEY`인지 확인하세요.
        - 값에는 KOBIS에서 발급받은 실제 API 인증키를 입력하세요.
        """
    )
    st.stop()


# ---------------------------------------------------------
# 4. KOBIS 일별 박스오피스 API 호출
# ---------------------------------------------------------

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)

params = {
    "key": KOBIS_KEY,
    "targetDt": target_dt
}

try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )

    # HTTP 자체가 실패한 경우
    response.raise_for_status()

    data = response.json()

except requests.exceptions.RequestException as e:
    st.error("🚨 KOBIS API 요청에 실패했습니다.")
    st.markdown(
        """
        **확인할 사항**
        
        - 인터넷 연결이 정상인지 확인하세요.
        - KOBIS API 서버에 일시적인 문제가 없는지 확인하세요.
        - API 주소가 올바른지 확인하세요.
        - 잠시 후 페이지를 새로고침해 보세요.
        """
    )
    st.caption(f"오류 내용: {e}")
    st.stop()

except ValueError:
    st.error("🚨 KOBIS에서 올바른 JSON 응답을 받지 못했습니다.")
    st.markdown(
        """
        **확인할 사항**
        
        - KOBIS API가 정상적으로 응답하고 있는지 확인하세요.
        - 잠시 후 다시 시도해 보세요.
        """
    )
    st.stop()


# ---------------------------------------------------------
# 5. KOBIS의 오류 응답(faultInfo) 확인
# ---------------------------------------------------------
# KOBIS는 인증키가 틀려도 HTTP 상태코드가 200일 수 있습니다.
# 따라서 상태코드만 확인하지 않고 faultInfo가 있는지도 확인합니다.

if "faultInfo" in data:
    fault_info = data["faultInfo"]

    error_code = fault_info.get("errorCode", "알 수 없음")
    error_message = fault_info.get("message", "알 수 없는 오류")

    st.error("🔑 KOBIS API에서 오류를 반환했습니다.")

    st.markdown(
        f"""
        **KOBIS 오류 정보**

        - 오류 코드: `{error_code}`
        - 오류 메시지: `{error_message}`

        **확인할 사항**

        - Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인하세요.
        - API 키 앞뒤에 불필요한 공백이나 따옴표가 없는지 확인하세요.
        - KOBIS에서 발급받은 키가 아직 유효한지 확인하세요.
        """
    )
    st.stop()


# ---------------------------------------------------------
# 6. 정상적인 박스오피스 데이터 꺼내기
# ---------------------------------------------------------

box_office_result = data.get("boxOfficeResult", {})

movie_list = box_office_result.get("dailyBoxOfficeList", [])


# ---------------------------------------------------------
# 7. 영화 목록이 비어 있는 경우
# ---------------------------------------------------------

if not movie_list:
    st.warning("📭 조회된 영화 목록이 없습니다.")

    st.markdown(
        f"""
        **확인할 사항**

        - 조회 날짜가 `{yesterday_kst.strftime('%Y-%m-%d')}`인지 확인하세요.
        - KOBIS에서 해당 날짜의 일별 박스오피스 데이터가 집계되었는지 확인하세요.
        - KOBIS API가 일시적으로 데이터를 제공하지 않는 상황인지 확인하세요.
        - 잠시 후 페이지를 새로고침해 보세요.
        """
    )
    st.stop()


# ---------------------------------------------------------
# 8. API 데이터를 표에 사용하기 좋은 형태로 변환
# ---------------------------------------------------------

rows = []

for movie in movie_list:
    rows.append(
        {
            "순위": int(movie.get("rank", 0)),
            "영화명": movie.get("movieNm", "-"),
            "개봉일": movie.get("openDt", "-"),
            "관객수": int(movie.get("audiCnt", 0)),
            "누적관객": int(movie.get("audiAcc", 0)),
            "스크린수": int(movie.get("scrnCnt", 0)),
        }
    )

df = pd.DataFrame(rows)


# ---------------------------------------------------------
# 9. 1위 영화 정보
# ---------------------------------------------------------

first_movie = df.iloc[0]

st.subheader("🏆 1위 영화")

st.markdown(f"## {first_movie['영화명']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "어제 관객수",
        f"{first_movie['관객수']:,}명"
    )

with col2:
    st.metric(
        "누적 관객수",
        f"{first_movie['누적관객']:,}명"
    )

with col3:
    st.metric(
        "스크린수",
        f"{first_movie['스크린수']:,}개"
    )


# ---------------------------------------------------------
# 10. 전체 박스오피스 표
# ---------------------------------------------------------

st.subheader("📋 전체 박스오피스")

# 숫자에 천 단위 구분기호를 넣어서 보기 편하게 표시합니다.
display_df = df.copy()

display_df["관객수"] = display_df["관객수"].map(lambda x: f"{x:,}")
display_df["누적관객"] = display_df["누적관객"].map(lambda x: f"{x:,}")
display_df["스크린수"] = display_df["스크린수"].map(lambda x: f"{x:,}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# 11. 관객수 상위 5편 막대그래프
# ---------------------------------------------------------

st.subheader("📊 관객수 상위 5편")

top5 = df.head(5).copy()

# 영화명을 인덱스로 설정하면 Streamlit의 막대그래프에서
# 영화별 관객수를 바로 비교할 수 있습니다.
chart_data = top5.set_index("영화명")[["관객수"]]

st.bar_chart(
    chart_data,
    use_container_width=True
)


# ---------------------------------------------------------
# 12. 데이터 출처
# ---------------------------------------------------------

st.caption(
    "데이터 출처: KOBIS 영화관입장권통합전산망 "
    "일별 박스오피스 Open API"
)
