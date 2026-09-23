```python
# main.py
# ============================================================
# 🎬 KOBIS 어제의 박스오피스
#
# 초보자용 설명:
# - 한국 시간 기준으로 '어제' 날짜를 자동 계산합니다.
# - KOBIS Open API에서 어제의 일별 박스오피스를 가져옵니다.
# - API 인증키는 Streamlit Secrets의 KOBIS_KEY에서 가져옵니다.
# - 인증키를 코드에 직접 작성하지 않습니다.
# ============================================================


# ------------------------------------------------------------
# 1. 필요한 라이브러리 가져오기
# ------------------------------------------------------------

import requests
import streamlit as st

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ------------------------------------------------------------
# 2. Streamlit 페이지 기본 설정
# ------------------------------------------------------------

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide",
)


# ------------------------------------------------------------
# 3. 화면 제목
# ------------------------------------------------------------

st.title("🎬 어제의 박스오피스")
st.caption("KOBIS 영화관입장권통합전산망 Open API")


# ------------------------------------------------------------
# 4. 한국 시간 기준으로 '어제' 계산하기
#
# 배포 서버가 한국에 있지 않아도 문제가 없도록
# 반드시 Asia/Seoul 시간대를 사용합니다.
# ------------------------------------------------------------

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)

yesterday = now_kst.date() - timedelta(days=1)

# KOBIS API가 요구하는 날짜 형식:
# YYYYMMDD
target_date = yesterday.strftime("%Y%m%d")

# 화면에 보여줄 날짜
display_date = yesterday.strftime("%Y년 %m월 %d일")


# ------------------------------------------------------------
# 5. KOBIS API 주소
# ------------------------------------------------------------

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ------------------------------------------------------------
# 6. Streamlit Secrets에서 API 인증키 가져오기
#
# Streamlit Cloud에서:
# Settings → Secrets
#
# 다음처럼 등록하면 됩니다.
#
# KOBIS_KEY = "발급받은_인증키"
#
# 실제 인증키는 코드에 작성하지 않습니다.
# ------------------------------------------------------------

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:
    st.error("🔑 KOBIS_KEY를 찾을 수 없습니다.")

    st.info(
        """
        다음 내용을 확인해주세요.

        1. Streamlit Cloud에서 앱의 Settings를 엽니다.
        2. Secrets 메뉴로 이동합니다.
        3. 아래처럼 KOBIS_KEY를 등록합니다.

        KOBIS_KEY = "본인의_API_인증키"

        인증키를 main.py에 직접 작성하면 안 됩니다.
        """
    )

    st.stop()


# ------------------------------------------------------------
# 7. KOBIS API 요청
# ------------------------------------------------------------

params = {
    "key": KOBIS_KEY,
    "targetDt": target_date,
}


try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=15,
    )

except requests.exceptions.Timeout:
    st.error("⏱️ KOBIS API 요청 시간이 초과되었습니다.")

    st.info(
        """
        KOBIS 서버가 일시적으로 느리거나
        인터넷 연결에 문제가 있을 수 있습니다.

        잠시 후 페이지를 새로고침해 주세요.
        """
    )

    st.stop()

except requests.exceptions.RequestException as e:
    st.error("🚨 KOBIS API 요청에 실패했습니다.")

    st.info(
        """
        다음 내용을 확인해주세요.

        • 인터넷 연결 상태
        • KOBIS API 서버 상태
        • API 주소가 올바른지
        • Streamlit Cloud의 네트워크 상태
        """
    )

    st.stop()


# ------------------------------------------------------------
# 8. HTTP 응답 상태 확인
# ------------------------------------------------------------

if response.status_code != 200:
    st.error(
        f"🚨 KOBIS 서버에서 HTTP {response.status_code} 오류가 발생했습니다."
    )

    st.info(
        """
        KOBIS 서버가 정상적으로 응답하지 않았을 수 있습니다.

        잠시 후 다시 시도해주세요.
        """
    )

    st.stop()


# ------------------------------------------------------------
# 9. JSON으로 변환
# ------------------------------------------------------------

try:
    data = response.json()

except ValueError:
    st.error("🚨 KOBIS에서 올바른 JSON 데이터를 받지 못했습니다.")

    st.info(
        """
        API 서버가 예상하지 못한 응답을 보냈습니다.

        잠시 후 다시 시도해주세요.
        """
    )

    st.stop()


# ------------------------------------------------------------
# 10. KOBIS의 faultInfo 확인
#
# 중요한 부분입니다.
#
# KOBIS는 인증키가 잘못되어도 HTTP 상태코드가 200일 수 있습니다.
# 대신 응답 안에 faultInfo가 들어옵니다.
# ------------------------------------------------------------

if "faultInfo" in data:

    fault_info = data.get("faultInfo", {})

    error_code = fault_info.get(
        "errorCode",
        "알 수 없음",
    )

    error_message = fault_info.get(
        "message",
        "알 수 없는 오류",
    )

    st.error("🔑 KOBIS API에서 오류를 반환했습니다.")

    st.write(
        f"**오류 코드:** `{error_code}`"
    )

    st.write(
        f"**오류 메시지:** `{error_message}`"
    )

    st.info(
        """
        다음 내용을 확인해주세요.

        1. Streamlit Cloud의 Secrets에 KOBIS_KEY가 등록되어 있는지
        2. 인증키를 정확하게 입력했는지
        3. 인증키 앞뒤에 불필요한 공백이나 따옴표 문제가 없는지
        4. KOBIS API 인증키가 정상적으로 발급된 키인지
        """
    )

    st.stop()


# ------------------------------------------------------------
# 11. boxOfficeResult에서 영화 목록 가져오기
# ------------------------------------------------------------

box_office_result = data.get(
    "boxOfficeResult"
)

if not box_office_result:
    st.error("🚨 KOBIS 응답에 boxOfficeResult가 없습니다.")

    st.info(
        """
        KOBIS API가 예상한 박스오피스 데이터를
        반환하지 않았습니다.

        API 응답이나 KOBIS 서버 상태를 확인해주세요.
        """
    )

    st.stop()


movie_list = box_office_result.get(
    "dailyBoxOfficeList",
    [],
)


# ------------------------------------------------------------
# 12. 영화 목록이 비어 있는 경우
# ------------------------------------------------------------

if not movie_list:

    st.warning(
        f"📭 {display_date}의 박스오피스 영화 목록이 없습니다."
    )

    st.info(
        """
        다음 내용을 확인해주세요.

        • 해당 날짜의 박스오피스가 아직 집계되지 않았는지
        • KOBIS API가 데이터를 정상적으로 반환했는지
        • 조회 날짜가 올바른지
        • KOBIS 서버에 일시적인 문제가 없는지

        이 앱은 오늘 데이터가 아니라
        한국 시간 기준 '어제' 데이터를 조회합니다.
        """
    )

    st.stop()


# ------------------------------------------------------------
# 13. 화면 상단에 조회 날짜 표시
# ------------------------------------------------------------

st.subheader(
    f"📅 {display_date} 박스오피스"
)

st.caption(
    f"조회 날짜: {target_date} · 한국 시간 기준"
)


# ------------------------------------------------------------
# 14. API 데이터를 표에 맞게 정리하기
#
# KOBIS API의 숫자 값은 문자열로 오기 때문에
# int()를 이용해 숫자로 변환합니다.
# ------------------------------------------------------------

table_data = []

for movie in movie_list:

    # 순위
    rank = int(
        movie.get("rank", 0)
    )

    # 전날 대비 순위 변화
    rank_inten = int(
        movie.get("rankInten", 0)
    )

    # 영화 이름
    movie_name = movie.get(
        "movieNm",
        "-",
    )

    # 개봉일
    open_date = movie.get(
        "openDt",
        "-",
    )

    # 그날 관객수
    audience = int(
        movie.get("audiCnt", 0)
    )

    # 누적 관객수
    accumulated_audience = int(
        movie.get("audiAcc", 0)
    )

    # 스크린 수
    screen_count = int(
        movie.get("scrnCnt", 0)
    )

    table_data.append(
        {
            "순위": rank,
            "영화명": movie_name,
            "개봉일": open_date,
            "관객수": audience,
            "누적관객": accumulated_audience,
            "스크린수": screen_count,
        }
    )


# ------------------------------------------------------------
# 15. 박스오피스 전체 표
# ------------------------------------------------------------

st.subheader("🏆 전체 박스오피스")

st.dataframe(
    table_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "순위": st.column_config.NumberColumn(
            "순위",
            format="%d위",
        ),

        "관객수": st.column_config.NumberColumn(
            "관객수",
            format="%,d명",
        ),

        "누적관객": st.column_config.NumberColumn(
            "누적관객",
            format="%,d명",
        ),

        "스크린수": st.column_config.NumberColumn(
            "스크린수",
            format="%,d개",
        ),
    },
)


# ------------------------------------------------------------
# 16. 1위 영화 가져오기
# ------------------------------------------------------------

first_movie = movie_list[0]

first_movie_name = first_movie.get(
    "movieNm",
    "-",
)

first_audience = int(
    first_movie.get(
        "audiCnt",
        0,
    )
)

first_accumulated = int(
    first_movie.get(
        "audiAcc",
        0,
    )
)

first_screens = int(
    first_movie.get(
        "scrnCnt",
        0,
    )
)


# ------------------------------------------------------------
# 17. 1위 영화 크게 표시
# ------------------------------------------------------------

st.divider()

st.subheader("🥇 어제의 1위")

st.markdown(
    f"## {first_movie_name}"
)


# ------------------------------------------------------------
# 18. 1위 영화 지표 카드 3장
# ------------------------------------------------------------

card1, card2, card3 = st.columns(3)


with card1:

    st.metric(
        label="👥 어제 관객수",
        value=f"{first_audience:,}명",
    )


with card2:

    st.metric(
        label="🎟️ 누적 관객수",
        value=f"{first_accumulated:,}명",
    )


with card3:

    st.metric(
        label="🎞️ 스크린 수",
        value=f"{first_screens:,}개",
    )


# ------------------------------------------------------------
# 19. 관객수 TOP 5 막대그래프
# ------------------------------------------------------------

st.divider()

st.subheader("📊 관객수 TOP 5")

# 그래프에 사용할 영화 5개만 가져옵니다.
top5_movies = movie_list[:5]


# 그래프용 데이터 만들기
chart_data = []

for movie in top5_movies:

    chart_data.append(
        {
            "영화명": movie.get(
                "movieNm",
                "-",
            ),

            "관객수": int(
                movie.get(
                    "audiCnt",
                    0,
                )
            ),
        }
    )


# ------------------------------------------------------------
# 20. Pandas DataFrame으로 변환
# ------------------------------------------------------------

import pandas as pd

chart_df = pd.DataFrame(
    chart_data
)


# 영화명을 인덱스로 설정합니다.
chart_df = chart_df.set_index(
    "영화명"
)


# ------------------------------------------------------------
# 21. 막대그래프 표시
# ------------------------------------------------------------

st.bar_chart(
    chart_df,
    y="관객수",
    horizontal=True,
    use_container_width=True,
)


# ------------------------------------------------------------
# 22. 데이터 안내
# ------------------------------------------------------------

st.divider()

st.caption(
    "데이터 출처: 영화관입장권통합전산망(KOBIS) Open API"
)

st.caption(
    "조회 기준: 한국 시간 기준 전날의 일별 박스오피스"
)
```

### `requirements.txt`

요청한 대로 **버전 숫자 없이**, Streamlit·Pandas·NumPy는 제외하고 필요한 라이브러리만 적으면 돼.

```text
requests
```
