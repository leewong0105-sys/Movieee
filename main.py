import streamlit as st
import requests
import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# =========================================================
# 1. 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 어제의 박스오피스")
st.caption("KOBIS 영화관입장권통합전산망 기준")


# =========================================================
# 2. 한국 시간으로 '어제' 계산
# =========================================================
# 배포 서버의 시간이 한국 시간이 아닐 수 있기 때문에
# Asia/Seoul을 직접 지정합니다.

KOREA_TIMEZONE = ZoneInfo("Asia/Seoul")

today_korea = datetime.now(KOREA_TIMEZONE).date()
yesterday = today_korea - timedelta(days=1)

# KOBIS API가 요구하는 날짜 형식: yyyymmdd
target_date = yesterday.strftime("%Y%m%d")

# 화면에 보여줄 날짜
display_date = yesterday.strftime("%Y년 %m월 %d일")


# =========================================================
# 3. Streamlit Secrets에서 API 키 가져오기
# =========================================================
# Streamlit Cloud의 Secrets에 다음과 같이 등록해야 합니다.
#
# KOBIS_KEY = "발급받은_키"
#
# API 키를 코드에 직접 작성하지 않습니다.

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:
    st.error("KOBIS_KEY를 찾을 수 없습니다.")

    st.info(
        "Streamlit Cloud의 Settings → Secrets에서 "
        "KOBIS_KEY가 등록되어 있는지 확인해주세요."
    )

    st.stop()


# =========================================================
# 4. KOBIS API 주소
# =========================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# =========================================================
# 5. KOBIS에 데이터 요청
# =========================================================
# key = 인증키
# targetDt = 조회할 날짜

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
    st.error("KOBIS 서버의 응답이 늦어지고 있습니다.")
    st.info("잠시 후 다시 실행해주세요.")
    st.stop()

except requests.exceptions.RequestException:
    st.error("KOBIS 서버에 연결하지 못했습니다.")
    st.info(
        "인터넷 연결이나 KOBIS API 상태를 확인한 뒤 "
        "잠시 후 다시 실행해주세요."
    )
    st.stop()


# =========================================================
# 6. HTTP 요청 상태 확인
# =========================================================

if response.status_code != 200:
    st.error("KOBIS에서 데이터를 가져오지 못했습니다.")

    st.info(
        f"서버 응답 상태 코드: {response.status_code}\n\n"
        "잠시 후 다시 실행하거나 KOBIS API 상태를 확인해주세요."
    )

    st.stop()


# =========================================================
# 7. JSON 데이터로 변환
# =========================================================

try:
    data = response.json()

except ValueError:
    st.error("KOBIS에서 올바른 데이터를 받지 못했습니다.")

    st.info(
        "KOBIS API 응답에 문제가 있을 수 있습니다. "
        "잠시 후 다시 실행해주세요."
    )

    st.stop()


# =========================================================
# 8. KOBIS API 자체 오류 확인
# =========================================================
# KOBIS는 인증키가 잘못되어도 HTTP 상태 코드가 200일 수 있습니다.
# 이 경우 faultInfo가 들어옵니다.

if "faultInfo" in data:

    fault_info = data.get("faultInfo", {})

    error_code = fault_info.get(
        "errorCode",
        "알 수 없음"
    )

    error_message = fault_info.get(
        "message",
        "알 수 없는 오류입니다."
    )

    st.error("KOBIS API 인증 또는 요청에 문제가 있습니다.")

    st.info(
        "다음 내용을 확인해주세요.\n\n"
        "• Streamlit Secrets에 KOBIS_KEY가 정확하게 등록되어 있는지\n"
        "• API 키 앞뒤에 불필요한 공백이 없는지\n"
        "• KOBIS에서 발급받은 인증키가 맞는지"
    )

    st.caption(
        f"오류 코드: {error_code} / {error_message}"
    )

    st.stop()


# =========================================================
# 9. boxOfficeResult 확인
# =========================================================

box_office_result = data.get("boxOfficeResult")

if not box_office_result:

    st.error("박스오피스 데이터를 찾을 수 없습니다.")

    st.info(
        "KOBIS에서 해당 날짜의 데이터를 제공하는지 "
        "확인해주세요."
    )

    st.stop()


# =========================================================
# 10. 영화 목록 가져오기
# =========================================================

movie_list = box_office_result.get(
    "dailyBoxOfficeList",
    []
)


# =========================================================
# 11. 영화 목록이 비어 있는 경우
# =========================================================

if not movie_list:

    st.warning(
        f"{display_date}의 박스오피스 영화 목록이 없습니다."
    )

    st.info(
        "KOBIS에서 해당 날짜의 박스오피스 데이터가 "
        "아직 제공되지 않았거나 데이터가 비어 있을 수 있습니다."
    )

    st.stop()


# =========================================================
# 12. 문자열로 들어오는 숫자를 숫자로 바꾸는 함수
# =========================================================
# KOBIS API에서는 rank, audiCnt 등의 숫자도 문자열로 옵니다.

def to_number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# =========================================================
# 13. 순위 기준으로 정렬
# =========================================================

movie_list = sorted(
    movie_list,
    key=lambda movie: to_number(movie.get("rank"))
)


# =========================================================
# 14. 조회 날짜 표시
# =========================================================

st.subheader(f"📅 {display_date}")

st.caption(
    f"한국 시간 기준 · KOBIS 조회 날짜: {target_date}"
)


# =========================================================
# 15. 전체 박스오피스 표 만들기
# =========================================================

table_rows = []

for movie in movie_list:

    rank = to_number(movie.get("rank"))

    movie_name = movie.get(
        "movieNm",
        "-"
    )

    open_date = movie.get(
        "openDt",
        "-"
    )

    # 개봉일 20260916 → 2026-09-16
    if len(open_date) == 8:
        open_date = (
            open_date[:4]
            + "-"
            + open_date[4:6]
            + "-"
            + open_date[6:8]
        )

    audience = to_number(
        movie.get("audiCnt")
    )

    accumulated_audience = to_number(
        movie.get("audiAcc")
    )

    screen_count = to_number(
        movie.get("scrnCnt")
    )

    table_rows.append(
        {
            "순위": f"{rank}위",
            "영화명": movie_name,
            "개봉일": open_date,
            "관객수": f"{audience:,}명",
            "누적관객": f"{accumulated_audience:,}명",
            "스크린수": f"{screen_count:,}개"
        }
    )


# =========================================================
# 16. 표 화면에 표시
# =========================================================

table_df = pd.DataFrame(table_rows)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 17. 1위 영화 찾기
# =========================================================

first_movie = movie_list[0]

first_movie_name = first_movie.get(
    "movieNm",
    "-"
)

first_audience = to_number(
    first_movie.get("audiCnt")
)

first_accumulated = to_number(
    first_movie.get("audiAcc")
)

first_screen_count = to_number(
    first_movie.get("scrnCnt")
)


# =========================================================
# 18. 1위 영화 크게 표시
# =========================================================

st.divider()

st.header(
    f"🥇 1위 영화: {first_movie_name}"
)


# =========================================================
# 19. 1위 영화 지표 카드 3개
# =========================================================

card1, card2, card3 = st.columns(3)

with card1:
    st.metric(
        label="어제 관객수",
        value=f"{first_audience:,}명"
    )

with card2:
    st.metric(
        label="누적 관객수",
        value=f"{first_accumulated:,}명"
    )

with card3:
    st.metric(
        label="스크린수",
        value=f"{first_screen_count:,}개"
    )


# =========================================================
# 20. 관객수 상위 5편 찾기
# =========================================================
# 순위가 아니라 실제 '그날 관객수(audiCnt)'를 기준으로
# 가장 많은 영화 5편을 선택합니다.

top5_movies = sorted(
    movie_list,
    key=lambda movie: to_number(
        movie.get("audiCnt")
    ),
    reverse=True
)[:5]


# =========================================================
# 21. 막대그래프용 데이터 만들기
# =========================================================

chart_rows = []

for movie in top5_movies:

    chart_rows.append(
        {
            "영화명": movie.get(
                "movieNm",
                "-"
            ),
            "관객수": to_number(
                movie.get("audiCnt")
            )
        }
    )


chart_df = pd.DataFrame(
    chart_rows
)


# =========================================================
# 22. 관객수 TOP 5 막대그래프
# =========================================================

st.divider()

st.header("📊 관객수 TOP 5")

if not chart_df.empty:

    chart_df = chart_df.set_index(
        "영화명"
    )

    st.bar_chart(
        chart_df,
        horizontal=True
    )

else:

    st.info(
        "막대그래프로 표시할 관객수 데이터가 없습니다."
    )


# =========================================================
# 23. 데이터 출처
# =========================================================

st.divider()

st.caption(
    "데이터 출처: KOBIS 영화관입장권통합전산망 Open API"
)
