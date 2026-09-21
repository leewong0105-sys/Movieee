# main.py
# ============================================================
# 🎬 KOBIS Daily Box Office Dashboard
# 어제의 박스오피스를 보여주는 Streamlit 앱
#
# 사용 방법
# 1. Streamlit Cloud의 Secrets에 KOBIS_KEY를 등록합니다.
# 2. 이 파일을 main.py로 저장합니다.
# 3. Streamlit Cloud에서 실행합니다.
#
# KOBIS API에서 제공하는 데이터만 사용합니다.
# ============================================================

import requests
import pandas as pd
import streamlit as st

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="KOBIS Daily Box Office",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. 화면 디자인
# ============================================================

st.markdown(
    """
    <style>
        /* 전체 배경 */
        .stApp {
            background:
                radial-gradient(
                    circle at 15% 0%,
                    rgba(255, 80, 80, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 85% 10%,
                    rgba(80, 120, 255, 0.08),
                    transparent 25%
                ),
                #0b0d12;
            color: #f5f5f5;
        }

        /* 기본 여백 */
        .block-container {
            max-width: 1250px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        /* 제목 */
        .hero-title {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -2px;
            margin-bottom: 0.2rem;
        }

        .hero-subtitle {
            color: #9da3ae;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        /* 섹션 제목 */
        .section-title {
            font-size: 1.35rem;
            font-weight: 800;
            margin-top: 2.2rem;
            margin-bottom: 1rem;
        }

        /* 1위 영화 카드 */
        .winner-card {
            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.08),
                    rgba(255,255,255,0.025)
                );
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.25);
        }

        .winner-label {
            color: #ffcc66;
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }

        .winner-title {
            font-size: 2.4rem;
            font-weight: 900;
            letter-spacing: -1px;
            margin-bottom: 18px;
        }

        .winner-info {
            color: #aeb4bf;
            font-size: 0.95rem;
        }

        /* 지표 카드 */
        .stat-card {
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 20px;
            min-height: 120px;
        }

        .stat-label {
            color: #969daa;
            font-size: 0.85rem;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 1.7rem;
            font-weight: 900;
        }

        .stat-description {
            color: #777e8b;
            font-size: 0.78rem;
            margin-top: 5px;
        }

        /* 순위 배지 */
        .rank-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            font-weight: 800;
            font-size: 0.85rem;
        }

        /* 분석 카드 */
        .analysis-card {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 18px;
            padding: 20px;
            height: 100%;
        }

        .analysis-number {
            font-size: 1.8rem;
            font-weight: 900;
        }

        .analysis-label {
            color: #9299a6;
            font-size: 0.82rem;
            margin-top: 5px;
        }

        /* 구분선 */
        hr {
            border-color: rgba(255,255,255,0.08) !important;
        }

        /* Streamlit dataframe */
        [data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }

        /* 버튼 */
        .stButton button {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. 한국 시간 기준으로 '어제' 계산
# ============================================================

# Streamlit Cloud 서버는 한국 시간이 아닐 수 있으므로
# 서버의 시간을 그대로 사용하지 않습니다.
KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)
today_kst = now_kst.date()
yesterday_kst = today_kst - timedelta(days=1)

# KOBIS API가 요구하는 YYYYMMDD 형식
target_dt = yesterday_kst.strftime("%Y%m%d")

pretty_date = yesterday_kst.strftime("%Y년 %m월 %d일")


# ============================================================
# 4. 상단 헤더
# ============================================================

st.markdown(
    """
    <div class="hero-title">🎬 KOBIS DAILY BOX OFFICE</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero-subtitle">
        어제의 전국 영화관 박스오피스 · {pretty_date} 기준
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. KOBIS API 인증키
# ============================================================

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:
    st.error("🔑 KOBIS 인증키를 찾을 수 없습니다.")

    st.markdown(
        """
        ### 무엇을 확인해야 하나요?

        1. Streamlit Cloud에서 **Settings → Secrets**로 이동하세요.
        2. Secret 이름이 정확히 `KOBIS_KEY`인지 확인하세요.
        3. KOBIS에서 발급받은 API 인증키를 값으로 넣었는지 확인하세요.

        예:

        ```toml
        KOBIS_KEY = "발급받은_인증키"
        ```
        """
    )

    st.stop()


# ============================================================
# 6. KOBIS API 요청
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)

params = {
    "key": KOBIS_KEY,
    "targetDt": target_dt,
}


try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

except requests.exceptions.Timeout:
    st.error("⏱️ KOBIS API 요청 시간이 초과되었습니다.")

    st.markdown(
        """
        ### 무엇을 확인해야 하나요?

        - 인터넷 연결을 확인하세요.
        - KOBIS API 서버가 일시적으로 느린지 확인하세요.
        - 잠시 후 페이지를 새로고침해 보세요.
        """
    )

    st.stop()

except requests.exceptions.RequestException as error:
    st.error("🚨 KOBIS API 요청에 실패했습니다.")

    st.markdown(
        """
        ### 무엇을 확인해야 하나요?

        - 인터넷 연결이 정상인지 확인하세요.
        - KOBIS API 서버에 문제가 없는지 확인하세요.
        - 잠시 후 다시 시도해 보세요.
        """
    )

    st.caption(f"오류 정보: {error}")

    st.stop()


# ============================================================
# 7. JSON 응답 확인
# ============================================================

try:
    data = response.json()

except ValueError:
    st.error("🚨 KOBIS에서 올바른 JSON 응답을 받지 못했습니다.")

    st.markdown(
        """
        ### 무엇을 확인해야 하나요?

        KOBIS API가 정상적인 응답을 보내고 있는지 확인한 뒤
        잠시 후 다시 시도해 주세요.
        """
    )

    st.stop()


# ============================================================
# 8. KOBIS 오류 응답 확인
# ============================================================

# KOBIS는 인증키가 잘못되어도 HTTP 200을 반환할 수 있습니다.
# 따라서 HTTP 상태코드만 확인하면 안 되고 faultInfo도 확인합니다.

if "faultInfo" in data:

    fault_info = data["faultInfo"]

    error_code = fault_info.get(
        "errorCode",
        "알 수 없음",
    )

    error_message = fault_info.get(
        "message",
        "알 수 없는 오류",
    )

    st.error("🔑 KOBIS API에서 오류를 반환했습니다.")

    st.markdown(
        f"""
        ### KOBIS 오류

        **오류 코드:** `{error_code}`

        **오류 메시지:** `{error_message}`

        ### 무엇을 확인해야 하나요?

        - Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인하세요.
        - 인증키 앞뒤에 불필요한 공백이 없는지 확인하세요.
        - KOBIS에서 발급받은 인증키가 유효한지 확인하세요.
        """
    )

    st.stop()


# ============================================================
# 9. 박스오피스 목록 가져오기
# ============================================================

box_office_result = data.get(
    "boxOfficeResult",
    {},
)

movie_list = box_office_result.get(
    "dailyBoxOfficeList",
    [],
)


# ============================================================
# 10. 영화 목록이 없는 경우
# ============================================================

if not movie_list:

    st.warning("📭 조회된 영화 목록이 없습니다.")

    st.markdown(
        f"""
        ### 조회 결과가 없습니다.

        현재 조회 날짜는 **{pretty_date}**입니다.

        다음 사항을 확인해 주세요.

        - KOBIS에서 해당 날짜의 일별 박스오피스가 집계되었는지
        - KOBIS API가 정상적으로 응답하고 있는지
        - API 인증키가 정상적으로 작동하는지
        - 잠시 후 페이지를 새로고침했을 때도 같은 문제가 발생하는지
        """
    )

    st.stop()


# ============================================================
# 11. API 데이터를 DataFrame으로 변환
# ============================================================

rows = []

for movie in movie_list:

    # KOBIS API 숫자 값은 문자열로 오므로
    # 계산하기 전에 int로 변환합니다.

    rank = int(movie.get("rank", 0))

    movie_name = movie.get(
        "movieNm",
        "-",
    )

    open_date = movie.get(
        "openDt",
        "-",
    )

    audience = int(
        movie.get(
            "audiCnt",
            0,
        )
    )

    audience_acc = int(
        movie.get(
            "audiAcc",
            0,
        )
    )

    screen_count = int(
        movie.get(
            "scrnCnt",
            0,
        )
    )

    show_count = int(
        movie.get(
            "showCnt",
            0,
        )
    )

    # 전일 대비 순위 증감
    rank_inten_raw = movie.get(
        "rankInten",
        "0",
    )

    try:
        rank_inten = int(rank_inten_raw)
    except (ValueError, TypeError):
        rank_inten = 0

    # 스크린 1개당 관객수
    if screen_count > 0:
        audience_per_screen = audience / screen_count
    else:
        audience_per_screen = 0

    # 상영 1회당 관객수
    if show_count > 0:
        audience_per_show = audience / show_count
    else:
        audience_per_show = 0

    # 순위 변동 표시
    if rank_inten > 0:
        rank_change = f"▲ {rank_inten}"

    elif rank_inten < 0:
        rank_change = f"▼ {abs(rank_inten)}"

    else:
        rank_change = "—"

    rows.append(
        {
            "순위": rank,
            "영화명": movie_name,
            "개봉일": open_date,
            "관객수": audience,
            "누적관객": audience_acc,
            "스크린수": screen_count,
            "상영횟수": show_count,
            "순위변동값": rank_inten,
            "순위변동": rank_change,
            "스크린당 관객": audience_per_screen,
            "회차당 관객": audience_per_show,
        }
    )


df = pd.DataFrame(rows)


# ============================================================
# 12. 1위 영화
# ============================================================

first_movie = df.iloc[0]

first_movie_name = first_movie["영화명"]
first_audience = int(first_movie["관객수"])
first_acc = int(first_movie["누적관객"])
first_screens = int(first_movie["스크린수"])
first_shows = int(first_movie["상영횟수"])

first_rank_change = int(
    first_movie["순위변동값"]
)


# 1위 순위 변동 문구
if first_rank_change > 0:
    first_change_text = (
        f"▲ 전일보다 {first_rank_change}계단 상승"
    )

elif first_rank_change < 0:
    first_change_text = (
        f"▼ 전일보다 {abs(first_rank_change)}계단 하락"
    )

else:
    first_change_text = "— 전일과 동일한 순위"


# ============================================================
# 13. 1위 영화 히어로 카드
# ============================================================

st.markdown(
    """
    <div class="section-title">🏆 어제의 1위</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="winner-card">

        <div class="winner-label">
            🥇 DAILY BOX OFFICE #1
        </div>

        <div class="winner-title">
            {first_movie_name}
        </div>

        <div class="winner-info">
            {first_change_text}
            &nbsp;&nbsp;·&nbsp;&nbsp;
            어제 하루 관객 {first_audience:,}명
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 14. 1위 영화 주요 지표 3개
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">👥 어제 관객수</div>
            <div class="stat-value">{first_audience:,}명</div>
            <div class="stat-description">
                하루 동안 관람한 관객
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🎟️ 누적 관객수</div>
            <div class="stat-value">{first_acc:,}명</div>
            <div class="stat-description">
                개봉 이후 누적 관객
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🎞️ 스크린수</div>
            <div class="stat-value">{first_screens:,}개</div>
            <div class="stat-description">
                해당 날짜의 스크린 수
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 15. 전체 박스오피스 요약
# ============================================================

total_audience = int(
    df["관객수"].sum()
)

total_screens = int(
    df["스크린수"].sum()
)

total_shows = int(
    df["상영횟수"].sum()
)

top5_audience = int(
    df.head(5)["관객수"].sum()
)

if total_audience > 0:
    top5_share = (
        top5_audience / total_audience
    ) * 100
else:
    top5_share = 0


# ============================================================
# 16. 전체 요약 카드
# ============================================================

st.markdown(
    """
    <div class="section-title">📈 어제의 박스오피스 요약</div>
    """,
    unsafe_allow_html=True,
)

summary1, summary2, summary3, summary4 = st.columns(4)

with summary1:

    st.markdown(
        f"""
        <div class="analysis-card">
            <div class="analysis-number">
                {total_audience:,}
            </div>
            <div class="analysis-label">
                전체 조회 영화 관객수
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with summary2:

    st.markdown(
        f"""
        <div class="analysis-card">
            <div class="analysis-number">
                {total_screens:,}
            </div>
            <div class="analysis-label">
                전체 스크린 수 합계
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with summary3:

    st.markdown(
        f"""
        <div class="analysis-card">
            <div class="analysis-number">
                {total_shows:,}
            </div>
            <div class="analysis-label">
                전체 상영횟수 합계
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with summary4:

    st.markdown(
        f"""
        <div class="analysis-card">
            <div class="analysis-number">
                {top5_share:.1f}%
            </div>
            <div class="analysis-label">
                TOP 5 관객 점유율
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 17. TOP 5 관객수 막대그래프
# ============================================================

st.markdown(
    """
    <div class="section-title">📊 관객수 TOP 5</div>
    """,
    unsafe_allow_html=True,
)

top5 = df.head(5).copy()

chart_data = top5[
    ["영화명", "관객수"]
].set_index("영화명")

st.bar_chart(
    chart_data,
    y="관객수",
    use_container_width=True,
)


# ============================================================
# 18. TOP 5 상세 지표
# ============================================================

st.markdown(
    """
    <div class="section-title">🔥 TOP 5 한눈에 보기</div>
    """,
    unsafe_allow_html=True,
)

for index, movie in top5.iterrows():

    rank = int(movie["순위"])
    movie_name = movie["영화명"]
    audience = int(movie["관객수"])
    screens = int(movie["스크린수"])
    shows = int(movie["상영횟수"])
    rank_change = movie["순위변동"]

    if rank == 1:
        emoji = "🥇"
    elif rank == 2:
        emoji = "🥈"
    elif rank == 3:
        emoji = "🥉"
    else:
        emoji = "🎬"

    col_a, col_b, col_c, col_d = st.columns(
        [0.7, 3.5, 1.7, 1.7]
    )

    with col_a:
        st.markdown(
            f"### {emoji}"
        )

    with col_b:
        st.markdown(
            f"**{movie_name}**"
        )
        st.caption(
            f"순위 {rank} · {rank_change}"
        )

    with col_c:
        st.metric(
            "관객수",
            f"{audience:,}명",
        )

    with col_d:
        st.metric(
            "스크린",
            f"{screens:,}개",
        )


# ============================================================
# 19. 효율 지표
# ============================================================

st.markdown(
    """
    <div class="section-title">🎟️ 상영 효율 지표</div>
    """,
    unsafe_allow_html=True,
)

eff1, eff2 = st.columns(2)

# 스크린당 관객수가 가장 높은 영화
best_screen_movie = df.loc[
    df["스크린당 관객"].idxmax()
]

# 상영 1회당 관객수가 가장 높은 영화
best_show_movie = df.loc[
    df["회차당 관객"].idxmax()
]


with eff1:

    st.markdown(
        f"""
        <div class="analysis-card">

            <div class="stat-label">
                🎞️ 스크린당 관객수가 가장 높은 영화
            </div>

            <div class="analysis-number">
                {best_screen_movie["영화명"]}
            </div>

            <div class="analysis-label">
                스크린 1개당
                {best_screen_movie["스크린당 관객"]:,.1f}명
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with eff2:

    st.markdown(
        f"""
        <div class="analysis-card">

            <div class="stat-label">
                🎟️ 상영 1회당 관객수가 가장 높은 영화
            </div>

            <div class="analysis-number">
                {best_show_movie["영화명"]}
            </div>

            <div class="analysis-label">
                상영 1회당
                {best_show_movie["회차당 관객"]:,.1f}명
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 20. 전체 박스오피스 표
# ============================================================

st.markdown(
    """
    <div class="section-title">📋 전체 박스오피스</div>
    """,
    unsafe_allow_html=True,
)


# 화면에 보여줄 표를 따로 만듭니다.
display_df = df[
    [
        "순위",
        "영화명",
        "개봉일",
        "관객수",
        "누적관객",
        "스크린수",
        "상영횟수",
        "순위변동",
        "스크린당 관객",
        "회차당 관객",
    ]
].copy()


# 숫자를 읽기 쉽게 표시
display_df["관객수"] = display_df[
    "관객수"
].map(lambda x: f"{x:,}")

display_df["누적관객"] = display_df[
    "누적관객"
].map(lambda x: f"{x:,}")

display_df["스크린수"] = display_df[
    "스크린수"
].map(lambda x: f"{x:,}")

display_df["상영횟수"] = display_df[
    "상영횟수"
].map(lambda x: f"{x:,}")

display_df["스크린당 관객"] = display_df[
    "스크린당 관객"
].map(lambda x: f"{x:,.1f}")

display_df["회차당 관객"] = display_df[
    "회차당 관객"
].map(lambda x: f"{x:,.1f}")


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# 21. 간단한 데이터 해석
# ============================================================

st.markdown(
    """
    <div class="section-title">💡 오늘의 박스오피스 포인트</div>
    """,
    unsafe_allow_html=True,
)


# 1위와 2위 관객수 차이
if len(df) >= 2:

    second_audience = int(
        df.iloc[1]["관객수"]
    )

    audience_gap = (
        first_audience - second_audience
    )

else:

    second_audience = 0
    audience_gap = 0


# 가장 많이 상승한 영화
rising_movie = df.loc[
    df["순위변동값"].idxmax()
]

# 가장 많이 하락한 영화
falling_movie = df.loc[
    df["순위변동값"].idxmin()
]


point1, point2, point3 = st.columns(3)


with point1:

    st.markdown(
        f"""
        <div class="analysis-card">

            <div class="stat-label">
                🥇 1위와 2위의 관객수 차이
            </div>

            <div class="analysis-number">
                {audience_gap:,}명
            </div>

            <div class="analysis-label">
                1위 {first_movie_name}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with point2:

    if rising_movie["순위변동값"] > 0:
        rising_text = (
            f"▲ {int(rising_movie['순위변동값'])}계단"
        )
    else:
        rising_text = "가장 큰 상승 없음"

    st.markdown(
        f"""
        <div class="analysis-card">

            <div class="stat-label">
                📈 가장 많이 상승
            </div>

            <div class="analysis-number">
                {rising_movie["영화명"]}
            </div>

            <div class="analysis-label">
                {rising_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with point3:

    if falling_movie["순위변동값"] < 0:
        falling_text = (
            f"▼ {abs(int(falling_movie['순위변동값']))}계단"
        )
    else:
        falling_text = "가장 큰 하락 없음"

    st.markdown(
        f"""
        <div class="analysis-card">

            <div class="stat-label">
                📉 가장 많이 하락
            </div>

            <div class="analysis-number">
                {falling_movie["영화명"]}
            </div>

            <div class="analysis-label">
                {falling_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 22. 데이터 출처 및 안내
# ============================================================

st.divider()

st.caption(
    f"📅 조회 기준일: {pretty_date} · "
    "데이터 출처: KOBIS 영화관입장권통합전산망"
)

st.caption(
    "※ 스크린당 관객 = 관객수 ÷ 스크린수 · "
    "회차당 관객 = 관객수 ÷ 상영횟수"
)
