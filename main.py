import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# -----------------------------------------
# 1. 기본 설정
# -----------------------------------------

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 어제의 박스오피스")


# -----------------------------------------
# 2. 한국 시간으로 어제 날짜 계산
# -----------------------------------------

korea_time = ZoneInfo("Asia/Seoul")

today = datetime.now(korea_time).date()
yesterday = today - timedelta(days=1)

target_date = yesterday.strftime("%Y%m%d")
display_date = yesterday.strftime("%Y-%m-%d")


# -----------------------------------------
# 3. Streamlit Secrets에서 API 키 가져오기
# -----------------------------------------

if "KOBIS_KEY" not in st.secrets:
    st.error("KOBIS_KEY가 설정되어 있지 않습니다.")
    st.info(
        "Streamlit Cloud의 Settings → Secrets에 "
        "KOBIS_KEY를 등록해주세요."
    )
    st.stop()

KOBIS_KEY = st.secrets["KOBIS_KEY"]


# -----------------------------------------
# 4. KOBIS API 주소
# -----------------------------------------

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# -----------------------------------------
# 5. API 요청
# -----------------------------------------

params = {
    "key": KOBIS_KEY,
    "targetDt": target_date
}

try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

except requests.exceptions.Timeout:
    st.error("KOBIS API 요청 시간이 초과되었습니다.")
    st.info("잠시 후 다시 실행해주세요.")
    st.stop()

except requests.exceptions.RequestException as e:
    st.error("KOBIS API에 연결하지 못했습니다.")
    st.info("인터넷 연결 또는 KOBIS API 상태를 확인해주세요.")
    st.stop()


# -----------------------------------------
# 6. HTTP 응답 확인
# -----------------------------------------

if response.status_code != 200:
    st.error(
        "KOBIS API 요청에 실패했습니다. "
        f"(HTTP {response.status_code})"
    )
    st.stop()


# -----------------------------------------
# 7. JSON 데이터로 변환
# -----------------------------------------

try:
    data = response.json()

except ValueError:
    st.error("KOBIS에서 올바른 데이터를 받지 못했습니다.")
    st.stop()


# -----------------------------------------
# 8. KOBIS 오류 확인
# -----------------------------------------

if "faultInfo" in data:
    fault = data["faultInfo"]

    error_code = fault.get("errorCode", "알 수 없음")
    error_message = fault.get(
        "message",
        "알 수 없는 오류가 발생했습니다."
    )

    st.error("KOBIS API 오류가 발생했습니다.")

    st.write("**오류 코드:**", error_code)
    st.write("**오류 내용:**", error_message)

    st.info(
        "다음 내용을 확인해주세요.\n\n"
        "1. Streamlit Secrets의 KOBIS_KEY가 정확한지 확인\n"
        "2. API 키 앞뒤에 불필요한 따옴표나 공백이 없는지 확인\n"
        "3. KOBIS API 사용이 정상적으로 가능한 키인지 확인"
    )

    st.stop()


# -----------------------------------------
# 9. 박스오피스 데이터 가져오기
# -----------------------------------------

box_office = data.get("boxOfficeResult")

if box_office is None:
    st.error("KOBIS에서 박스오피스 데이터를 받지 못했습니다.")
    st.stop()


movie_list = box_office.get("dailyBoxOfficeList", [])


# -----------------------------------------
# 10. 영화 목록이 비어 있는 경우
# -----------------------------------------

if not movie_list:
    st.warning(
        f"{display_date}의 박스오피스 데이터가 없습니다."
    )

    st.info(
        "KOBIS에서 해당 날짜의 영화관입장권 데이터가 "
        "아직 제공되지 않았거나 데이터가 비어 있을 수 있습니다."
    )

    st.stop()


# -----------------------------------------
# 11. 숫자를 안전하게 변환하는 함수
# -----------------------------------------

def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# -----------------------------------------
# 12. 순위 기준으로 정렬
# -----------------------------------------

movie_list = sorted(
    movie_list,
    key=lambda movie: to_int(movie.get("rank"))
)


# -----------------------------------------
# 13. 날짜 표시
# -----------------------------------------

st.subheader(f"📅 {display_date} 박스오피스")

st.caption(
    f"한국 시간 기준 · 조회 날짜 {target_date}"
)


# -----------------------------------------
# 14. 전체 영화 표
# -----------------------------------------

table_rows = []

for movie in movie_list:

    rank = to_int(movie.get("rank"))
    movie_name = movie.get("movieNm", "-")
    open_date = movie.get("openDt", "-")

    # 개봉일을 보기 좋게 변경
    if len(open_date) == 8:
        open_date = (
            open_date[:4]
            + "-"
            + open_date[4:6]
            + "-"
            + open_date[6:8]
        )

    audience = to_int(movie.get("audiCnt"))
    accumulated = to_int(movie.get("audiAcc"))
    screens = to_int(movie.get("scrnCnt"))

    table_rows.append(
        {
            "순위": f"{rank}위",
            "영화명": movie_name,
            "개봉일": open_date,
            "관객수": f"{audience:,}명",
            "누적관객": f"{accumulated:,}명",
            "스크린수": f"{screens:,}개"
        }
    )


table_df = pd.DataFrame(table_rows)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------------------
# 15. 1위 영화
# -----------------------------------------

first_movie = movie_list[0]

first_movie_name = first_movie.get("movieNm", "-")
first_audience = to_int(first_movie.get("audiCnt"))
first_accumulated = to_int(first_movie.get("audiAcc"))
first_screens = to_int(first_movie.get("scrnCnt"))


st.divider()

st.header(f"🥇 1위 — {first_movie_name}")


# -----------------------------------------
# 16. 3개 핵심 지표
# -----------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "어제 관객수",
        f"{first_audience:,}명"
    )

with col2:
    st.metric(
        "누적 관객수",
        f"{first_accumulated:,}명"
    )

with col3:
    st.metric(
        "스크린수",
        f"{first_screens:,}개"
    )


# -----------------------------------------
# 17. 관객수 TOP 5
# -----------------------------------------

st.divider()

st.header("📊 관객수 TOP 5")


top5 = sorted(
    movie_list,
    key=lambda movie: to_int(movie.get("audiCnt")),
    reverse=True
)[:5]


chart_rows = []

for movie in top5:

    movie_name = movie.get("movieNm", "-")
    audience = to_int(movie.get("audiCnt"))

    chart_rows.append(
        {
            "영화명": movie_name,
            "관객수": audience
        }
    )


chart_df = pd.DataFrame(chart_rows)

if not chart_df.empty:

    chart_df = chart_df.set_index("영화명")

    st.bar_chart(
        chart_df,
        horizontal=True
    )

else:
    st.info("차트로 표시할 데이터가 없습니다.")


# -----------------------------------------
# 18. 하단 안내
# -----------------------------------------

st.divider()

st.caption(
    "데이터 출처: KOBIS 영화관입장권통합전산망 Open API"
)
