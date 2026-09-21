
# main.py
# ============================================================
# 🎬 KOBIS DAILY BOX OFFICE
#
# 기능
# 1. 한국 시간 기준 '어제' 박스오피스 자동 조회
# 2. TOP 5 관객수를 세련된 카드 UI로 표시
# 3. 1위 영화 강조
# 4. 순위 변동 표시
# 5. 스크린당 관객 / 상영 1회당 관객 계산
# 6. 영화 검색 기능
# 7. 검색한 영화의 상세정보 조회
# 8. 영화의 러닝타임 / 장르 / 감독 / 배우 등 표시
# 9. KOBIS API 오류 안내
#
# 인증키는 코드에 작성하지 않습니다.
# Streamlit Secrets의 KOBIS_KEY에서 가져옵니다.
# ============================================================

import requests
import streamlit as st

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="KOBIS Daily Box Office",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. 디자인
# ============================================================

st.markdown(
    """
    <style>

    /* ----------------------------------------------------
       전체 페이지
    ---------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(255, 70, 90, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(80, 110, 255, 0.10),
                transparent 25%
            ),
            #0b0d12;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }


    /* ----------------------------------------------------
       헤더
    ---------------------------------------------------- */

    .hero-small {
        color: #8d94a1;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 0.4rem;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;
    }

    .hero-description {
        color: #9299a6;
        margin-top: 0.7rem;
        margin-bottom: 2rem;
    }


    /* ----------------------------------------------------
       섹션
    ---------------------------------------------------- */

    .section {
        margin-top: 2.5rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    .section-subtitle {
        color: #7f8794;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }


    /* ----------------------------------------------------
       1위 카드
    ---------------------------------------------------- */

    .winner {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.09),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 26px;

        padding: 30px;

        box-shadow:
            0 20px 70px rgba(0,0,0,0.28);

        margin-bottom: 1rem;
    }

    .winner-badge {
        display: inline-block;

        background: rgba(255,193,7,0.13);
        border: 1px solid rgba(255,193,7,0.22);

        color: #ffd166;

        padding: 6px 11px;
        border-radius: 999px;

        font-size: 0.78rem;
        font-weight: 900;

        margin-bottom: 13px;
    }

    .winner-name {
        font-size: 2.45rem;
        font-weight: 950;
        letter-spacing: -1.5px;
        line-height: 1.1;

        margin-bottom: 10px;
    }

    .winner-meta {
        color: #939aa7;
        font-size: 0.9rem;
    }


    /* ----------------------------------------------------
       지표 카드
    ---------------------------------------------------- */

    .metric-box {
        background: rgba(255,255,255,0.045);

        border: 1px solid rgba(255,255,255,0.075);

        border-radius: 18px;

        padding: 20px;

        min-height: 115px;
    }

    .metric-label {
        color: #858d9a;
        font-size: 0.8rem;
        font-weight: 700;

        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.55rem;
        font-weight: 900;

        letter-spacing: -0.5px;
    }

    .metric-desc {
        color: #676f7c;
        font-size: 0.75rem;

        margin-top: 5px;
    }


    /* ----------------------------------------------------
       TOP 영화 카드
    ---------------------------------------------------- */

    .movie-row {
        background: rgba(255,255,255,0.035);

        border: 1px solid rgba(255,255,255,0.065);

        border-radius: 18px;

        padding: 18px 20px;

        margin-bottom: 10px;
    }

    .movie-rank {
        color: #8e96a3;

        font-size: 0.8rem;
        font-weight: 800;
    }

    .movie-name {
        font-size: 1.05rem;
        font-weight: 900;

        margin-top: 3px;
    }

    .movie-detail {
        color: #777f8c;
        font-size: 0.75rem;

        margin-top: 4px;
    }

    .movie-audience {
        font-size: 1.05rem;
        font-weight: 900;
        text-align: right;
    }

    .movie-screen {
        color: #777f8c;
        font-size: 0.75rem;
        text-align: right;
        margin-top: 4px;
    }


    /* ----------------------------------------------------
       검색 결과 카드
    ---------------------------------------------------- */

    .search-card {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.06),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.09);

        border-radius: 22px;

        padding: 25px;

        margin-top: 15px;
    }

    .search-title {
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .search-en {
        color: #7e8693;
        font-size: 0.85rem;

        margin-top: 3px;
    }

    .info-label {
        color: #7e8693;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .info-value {
        color: #f0f1f3;
        font-size: 0.95rem;
        font-weight: 700;

        margin-top: 3px;
    }


    /* ----------------------------------------------------
       안내 박스
    ---------------------------------------------------- */

    .notice {
        background: rgba(255,255,255,0.035);

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 16px;

        padding: 17px 19px;

        color: #939aa7;

        font-size: 0.84rem;

        line-height: 1.6;
    }


    /* ----------------------------------------------------
       구분선
    ---------------------------------------------------- */

    hr {
        border-color: rgba(255,255,255,0.07) !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. 공통 함수
# ============================================================

def format_number(value):
    """숫자에 천 단위 쉼표를 넣습니다."""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return "-"


def safe_int(value, default=0):
    """문자열 숫자를 안전하게 정수로 변환합니다."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def api_get(url, params):
    """KOBIS API를 호출하고 JSON을 반환합니다."""

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:
        return None, "timeout"

    except requests.exceptions.RequestException:
        return None, "request"

    except ValueError:
        return None, "json"

    return data, None


# ============================================================
# 4. 한국 시간
# ============================================================

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)

today_kst = now_kst.date()

yesterday_kst = today_kst - timedelta(days=1)

target_dt = yesterday_kst.strftime("%Y%m%d")

pretty_date = yesterday_kst.strftime(
    "%Y년 %m월 %d일"
)


# ============================================================
# 5. API KEY
# ============================================================

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error("🔑 KOBIS_KEY를 찾을 수 없습니다.")

    st.markdown(
        """
        ### 확인해주세요

        Streamlit Cloud의

        **Settings → Secrets**

        에 다음 항목이 있어야 합니다.

        ```toml
        KOBIS_KEY = "본인의_API_인증키"
        ```

        인증키를 코드 안에 직접 넣을 필요는 없습니다.
        """
    )

    st.stop()


# ============================================================
# 6. KOBIS URL
# ============================================================

BOXOFFICE_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)

MOVIE_LIST_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/movie/"
    "searchMovieList.json"
)

MOVIE_INFO_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/movie/"
    "searchMovieInfo.json"
)


# ============================================================
# 7. 어제의 박스오피스 가져오기
# ============================================================

boxoffice_data, boxoffice_error = api_get(
    BOXOFFICE_URL,
    {
        "key": KOBIS_KEY,
        "targetDt": target_dt,
    },
)


if boxoffice_error == "timeout":

    st.error("⏱️ KOBIS API 요청 시간이 초과되었습니다.")

    st.info(
        "KOBIS 서버가 일시적으로 느릴 수 있습니다. "
        "잠시 후 새로고침해 주세요."
    )

    st.stop()


if boxoffice_error == "request":

    st.error("🚨 KOBIS API 요청에 실패했습니다.")

    st.info(
        "인터넷 연결과 KOBIS API 서버 상태를 확인한 뒤 "
        "다시 시도해 주세요."
    )

    st.stop()


if boxoffice_error == "json":

    st.error("🚨 KOBIS에서 올바른 응답을 받지 못했습니다.")

    st.info(
        "KOBIS API가 정상적으로 응답하고 있는지 확인한 뒤 "
        "잠시 후 다시 시도해 주세요."
    )

    st.stop()


# ============================================================
# 8. API faultInfo 확인
# ============================================================

if "faultInfo" in boxoffice_data:

    fault = boxoffice_data["faultInfo"]

    st.error("🔑 KOBIS API 오류")

    st.write(
        f"오류 코드: `{fault.get('errorCode', '-')}`"
    )

    st.write(
        f"오류 메시지: `{fault.get('message', '-')}`"
    )

    st.info(
        "Streamlit Secrets의 KOBIS_KEY가 정확한지 확인해 주세요."
    )

    st.stop()


# ============================================================
# 9. 영화 목록
# ============================================================

movie_list = (
    boxoffice_data
    .get("boxOfficeResult", {})
    .get("dailyBoxOfficeList", [])
)


if not movie_list:

    st.warning("📭 조회된 영화가 없습니다.")

    st.info(
        f"{pretty_date}의 KOBIS 일별 박스오피스가 "
        "아직 집계되지 않았거나 API에서 데이터를 반환하지 "
        "않았을 수 있습니다."
    )

    st.stop()


# ============================================================
# 10. 데이터 정리
# ============================================================

movies = []

for movie in movie_list:

    rank = safe_int(
        movie.get("rank")
    )

    audience = safe_int(
        movie.get("audiCnt")
    )

    accumulated = safe_int(
        movie.get("audiAcc")
    )

    screens = safe_int(
        movie.get("scrnCnt")
    )

    shows = safe_int(
        movie.get("showCnt")
    )

    rank_inten = safe_int(
        movie.get("rankInten")
    )

    if screens > 0:

        audience_per_screen = (
            audience / screens
        )

    else:

        audience_per_screen = 0


    if shows > 0:

        audience_per_show = (
            audience / shows
        )

    else:

        audience_per_show = 0


    # 순위 변동
    if rank_inten > 0:

        change_text = (
            f"▲ {rank_inten}"
        )

    elif rank_inten < 0:

        change_text = (
            f"▼ {abs(rank_inten)}"
        )

    else:

        change_text = "—"


    movies.append(
        {
            "rank": rank,
            "movieNm": movie.get(
                "movieNm",
                "-"
            ),
            "openDt": movie.get(
                "openDt",
                "-"
            ),
            "movieCd": movie.get(
                "movieCd",
                ""
            ),
            "audience": audience,
            "accumulated": accumulated,
            "screens": screens,
            "shows": shows,
            "rankInten": rank_inten,
            "change": change_text,
            "audiencePerScreen": audience_per_screen,
            "audiencePerShow": audience_per_show,
        }
    )


# ============================================================
# 11. 헤더
# ============================================================

st.markdown(
    """
    <div class="hero-small">
        KOBIS · DAILY BOX OFFICE
    </div>

    <div class="hero-title">
        🎬 어제의 박스오피스
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero-description">
        {pretty_date} · 한국 시간 기준 · 전국 일별 박스오피스
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 12. 1위 영화
# ============================================================

first = movies[0]

rank_change = first["rankInten"]

if rank_change > 0:

    rank_text = (
        f"▲ 전일보다 {rank_change}계단 상승"
    )

elif rank_change < 0:

    rank_text = (
        f"▼ 전일보다 {abs(rank_change)}계단 하락"
    )

else:

    rank_text = "— 전일과 동일한 순위"


st.markdown(
    """
    <div class="section">
        <div class="section-title">🏆 어제의 1위</div>
        <div class="section-subtitle">
            가장 많은 관객이 찾은 영화
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# HTML 안에 영화 제목을 직접 넣지 않고
# 일반 Streamlit 요소를 사용해 깨짐을 줄입니다.

st.markdown(
    f"""
    <div class="winner">

        <div class="winner-badge">
            🥇 DAILY BOX OFFICE #1
        </div>

        <div class="winner-name">
            {first["movieNm"]}
        </div>

        <div class="winner-meta">
            {rank_text}
            &nbsp;&nbsp;·&nbsp;&nbsp;
            어제 {format_number(first["audience"])}명 관람
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 13. 1위 핵심 지표
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                👥 어제 관객수
            </div>
            <div class="metric-value">
                {format_number(first["audience"])}명
            </div>
            <div class="metric-desc">
                해당 날짜 관객수
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                🎟️ 누적 관객
            </div>
            <div class="metric-value">
                {format_number(first["accumulated"])}명
            </div>
            <div class="metric-desc">
                개봉 이후 누적
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                🎞️ 스크린
            </div>
            <div class="metric-value">
                {format_number(first["screens"])}개
            </div>
            <div class="metric-desc">
                해당 날짜 스크린 수
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 14. TOP 5 관객수
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">🔥 관객수 TOP 5</div>
        <div class="section-subtitle">
            숫자 표 대신 영화별 카드로 표시합니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


for movie in movies[:5]:

    rank = movie["rank"]

    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"
    else:
        medal = "🎬"


    st.markdown(
        f"""
        <div class="movie-row">

            <div style="display:flex;
                        justify-content:space-between;
                        align-items:center;">

                <div>

                    <div class="movie-rank">
                        {medal} {rank}위
                    </div>

                    <div class="movie-name">
                        {movie["movieNm"]}
                    </div>

                    <div class="movie-detail">
                        {movie["change"]}
                        &nbsp; · &nbsp;
                        {format_number(movie["screens"])} 스크린
                        &nbsp; · &nbsp;
                        {format_number(movie["shows"])}회 상영
                    </div>

                </div>

                <div>

                    <div class="movie-audience">
                        {format_number(movie["audience"])}명
                    </div>

                    <div class="movie-screen">
                        어제 관객수
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 15. TOP 5 막대그래프
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">📊 관객수 비교</div>
    </div>
    """,
    unsafe_allow_html=True,
)


chart_data = {
    movie["movieNm"]: movie["audience"]
    for movie in movies[:5]
}

st.bar_chart(
    chart_data,
    horizontal=True,
)


# ============================================================
# 16. 주요 데이터 분석
# ============================================================

total_audience = sum(
    movie["audience"]
    for movie in movies
)

top5_audience = sum(
    movie["audience"]
    for movie in movies[:5]
)


if total_audience > 0:

    top5_share = (
        top5_audience /
        total_audience *
        100
    )

else:

    top5_share = 0


best_screen = max(
    movies,
    key=lambda x: x["audiencePerScreen"]
)


best_show = max(
    movies,
    key=lambda x: x["audiencePerShow"]
)


most_up = max(
    movies,
    key=lambda x: x["rankInten"]
)


most_down = min(
    movies,
    key=lambda x: x["rankInten"]
)


# ============================================================
# 17. 데이터 포인트
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">💡 오늘의 박스오피스 포인트</div>
        <div class="section-subtitle">
            어제 데이터를 기준으로 계산한 간단한 지표입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


p1, p2, p3 = st.columns(3)


with p1:

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                🔥 TOP 5 관객 비중
            </div>

            <div class="metric-value">
                {top5_share:.1f}%
            </div>

            <div class="metric-desc">
                조회된 전체 영화 관객수 기준
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with p2:

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                📈 가장 크게 상승
            </div>

            <div class="metric-value">
                {most_up["movieNm"]}
            </div>

            <div class="metric-desc">
                {most_up["change"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with p3:

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                📉 가장 크게 하락
            </div>

            <div class="metric-value">
                {most_down["movieNm"]}
            </div>

            <div class="metric-desc">
                {most_down["change"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 18. 상영 효율
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">🎟️ 상영 효율</div>
        <div class="section-subtitle">
            KOBIS의 관객수·스크린수·상영횟수를 이용해 계산합니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


e1, e2 = st.columns(2)


with e1:

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                🎞️ 스크린당 관객수가 가장 높은 영화
            </div>

            <div class="metric-value">
                {best_screen["movieNm"]}
            </div>

            <div class="metric-desc">
                스크린 1개당
                {best_screen["audiencePerScreen"]:,.1f}명
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with e2:

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                🎟️ 상영 1회당 관객수가 가장 높은 영화
            </div>

            <div class="metric-value">
                {best_show["movieNm"]}
            </div>

            <div class="metric-desc">
                상영 1회당
                {best_show["audiencePerShow"]:,.1f}명
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 19. 영화 검색
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">🔎 영화 정보 검색</div>
        <div class="section-subtitle">
            KOBIS 영화정보에서 영화의 상세 정보를 검색합니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


search_col1, search_col2 = st.columns(
    [4, 1]
)


with search_col1:

    search_text = st.text_input(
        "영화 검색",
        placeholder="영화 제목을 입력하세요",
        label_visibility="collapsed",
    )


with search_col2:

    search_button = st.button(
        "🔎 검색",
        use_container_width=True,
        type="primary",
    )


# 엔터로 검색하는 것도 지원하기 위해
# 검색어가 입력되어 있으면 검색 결과를 처리합니다.
if search_button and search_text.strip():

    search_data, search_error = api_get(
        MOVIE_LIST_URL,
        {
            "key": KOBIS_KEY,
            "movieNm": search_text.strip(),
            "itemPerPage": 10,
        },
    )


    if search_error:

        st.error(
            "영화 검색 요청에 실패했습니다. "
            "잠시 후 다시 시도해 주세요."
        )

    elif "faultInfo" in search_data:

        st.error(
            search_data["faultInfo"].get(
                "message",
                "KOBIS API 오류",
            )
        )

    else:

        search_result = (
            search_data
            .get("movieListResult", {})
            .get("movieList", [])
        )


        if not search_result:

            st.warning(
                f"'{search_text}'에 해당하는 영화를 찾지 못했습니다."
            )

        else:

            st.success(
                f"'{search_text}' 검색 결과 "
                f"{len(search_result)}건"
            )


            # 검색 결과를 selectbox로 선택
            search_options = {}

            for item in search_result:

                title = item.get(
                    "movieNm",
                    "-"
                )

                code = item.get(
                    "movieCd",
                    ""
                )

                year = item.get(
                    "prdtYear",
                    ""
                )

                label = title

                if year:
                    label += f" ({year})"

                search_options[label] = code


            selected_movie = st.selectbox(
                "영화를 선택하세요",
                list(search_options.keys()),
            )


            selected_code = search_options[
                selected_movie
            ]


            # ------------------------------------------------
            # 선택한 영화의 상세 정보
            # ------------------------------------------------

            info_data, info_error = api_get(
                MOVIE_INFO_URL,
                {
                    "key": KOBIS_KEY,
                    "movieCd": selected_code,
                },
            )


            if info_error:

                st.error(
                    "영화 상세정보를 가져오지 못했습니다."
                )

            elif "faultInfo" in info_data:

                st.error(
                    info_data["faultInfo"].get(
                        "message",
                        "KOBIS API 오류",
                    )
                )

            else:

                movie_info = (
                    info_data
                    .get("movieInfoResult", {})
                    .get("movieInfo", {})
                )


                if not movie_info:

                    st.warning(
                        "해당 영화의 상세정보가 없습니다."
                    )

                else:

                    movie_title = movie_info.get(
                        "movieNm",
                        "-"
                    )

                    movie_en = movie_info.get(
                        "movieNmEn",
                        ""
                    )

                    open_date_raw = movie_info.get(
                        "openDt",
                        ""
                    )

                    show_time = movie_info.get(
                        "showTm",
                        ""
                    )

                    movie_type = movie_info.get(
                        "typeNm",
                        "-"
                    )

                    status = movie_info.get(
                        "prdtStatNm",
                        "-"
                    )


                    # 개봉일을 YYYY-MM-DD로 변환
                    if len(open_date_raw) == 8:

                        open_date = (
                            f"{open_date_raw[:4]}-"
                            f"{open_date_raw[4:6]}-"
                            f"{open_date_raw[6:]}"
                        )

                    else:

                        open_date = (
                            open_date_raw or "-"
                        )


                    # 러닝타임
                    if show_time:

                        runtime_text = (
                            f"{show_time}분"
                        )

                    else:

                        runtime_text = "-"


                    # 장르
                    genres = movie_info.get(
                        "genres",
                        []
                    )

                    genre_names = [
                        genre.get(
                            "genreNm",
                            ""
                        )
                        for genre in genres
                    ]

                    genre_text = ", ".join(
                        [
                            x
                            for x in genre_names
                            if x
                        ]
                    ) or "-"


                    # 국가
                    nations = movie_info.get(
                        "nations",
                        []
                    )

                    nation_names = [
                        nation.get(
                            "nationNm",
                            ""
                        )
                        for nation in nations
                    ]

                    nation_text = ", ".join(
                        [
                            x
                            for x in nation_names
                            if x
                        ]
                    ) or "-"


                    # 감독
                    directors = movie_info.get(
                        "directors",
                        []
                    )

                    director_names = [
                        director.get(
                            "peopleNm",
                            ""
                        )
                        for director in directors
                    ]

                    director_text = ", ".join(
                        [
                            x
                            for x in director_names
                            if x
                        ]
                    ) or "-"


                    # 배우
                    actors = movie_info.get(
                        "actors",
                        []
                    )

                    actor_names = [
                        actor.get(
                            "peopleNm",
                            ""
                        )
                        for actor in actors[:8]
                    ]

                    actor_text = ", ".join(
                        [
                            x
                            for x in actor_names
                            if x
                        ]
                    ) or "-"


                    # ------------------------------------------------
                    # 검색 영화 카드
                    # ------------------------------------------------

                    st.markdown(
                        f"""
                        <div class="search-card">

                            <div class="search-title">
                                {movie_title}
                            </div>

                            <div class="search-en">
                                {movie_en}
                            </div>

                            <hr>

                            <div style="
                                display:grid;
                                grid-template-columns:
                                repeat(3, 1fr);
                                gap:20px;
                            ">

                                <div>
                                    <div class="info-label">
                                        🎬 장르
                                    </div>
                                    <div class="info-value">
                                        {genre_text}
                                    </div>
                                </div>

                                <div>
                                    <div class="info-label">
                                        ⏱️ 러닝타임
                                    </div>
                                    <div class="info-value">
                                        {runtime_text}
                                    </div>
                                </div>

                                <div>
                                    <div class="info-label">
                                        📅 개봉일
                                    </div>
                                    <div class="info-value">
                                        {open_date}
                                    </div>
                                </div>

                                <div>
                                    <div class="info-label">
                                        🌏 국가
                                    </div>
                                    <div class="info-value">
                                        {nation_text}
                                    </div>
                                </div>

                                <div>
                                    <div class="info-label">
                                        🎥 감독
                                    </div>
                                    <div class="info-value">
                                        {director_text}
                                    </div>
                                </div>

                                <div>
                                    <div class="info-label">
                                        📌 제작상태
                                    </div>
                                    <div class="info-value">
                                        {status}
                                    </div>
                                </div>

                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    # 배우는 HTML grid 밖에서 별도 표시
                    st.markdown(
                        f"""
                        <div class="notice"
                             style="margin-top:12px;">

                            <b>🎭 주요 출연진</b><br>

                            {actor_text}

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    # ------------------------------------------------
                    # 상영관 안내
                    # ------------------------------------------------

                    st.markdown(
                        """
                        <div class="section">
                            <div class="section-title">
                                🎞️ 상영 정보
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    st.markdown(
                        f"""
                        <div class="notice">

                            <b>⏱️ 영화 러닝타임</b>
                            &nbsp; {runtime_text}

                            <br><br>

                            <b>🏢 극장별 상영관 / 상영시간표</b>

                            <br>

                            KOBIS Open API의 영화 상세정보에서는
                            영화의 러닝타임 등의 작품 정보는 제공하지만,
                            현재 이 API에서 극장별 실시간 상영관과
                            상영시간표를 직접 제공하지 않습니다.

                            <br><br>

                            따라서 존재하지 않는 상영관이나
                            상영시간을 임의로 표시하지 않습니다.

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# 20. 메인 영화 선택 → 상세정보
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">
            🎬 영화 상세정보 바로가기
        </div>

        <div class="section-subtitle">
            박스오피스에 있는 영화를 선택하면
            KOBIS 영화 상세정보를 확인할 수 있습니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


main_movie_options = [
    movie["movieNm"]
    for movie in movies
]


selected_main_movie = st.selectbox(
    "박스오피스 영화 선택",
    main_movie_options,
    key="main_movie_select",
)


selected_main = next(
    (
        movie
        for movie in movies
        if movie["movieNm"] == selected_main_movie
    ),
    None,
)


if selected_main:

    st.caption(
        f"선택한 영화: {selected_main['movieNm']}"
    )

    if st.button(
        "🎞️ 이 영화 상세정보 보기",
        key="main_detail_button",
    ):

        detail_data, detail_error = api_get(
            MOVIE_INFO_URL,
            {
                "key": KOBIS_KEY,
                "movieCd": selected_main["movieCd"],
            },
        )


        if detail_error:

            st.error(
                "영화 상세정보를 불러오지 못했습니다."
            )

        elif "faultInfo" in detail_data:

            st.error(
                detail_data["faultInfo"].get(
                    "message",
                    "KOBIS API 오류",
                )
            )

        else:

            detail = (
                detail_data
                .get("movieInfoResult", {})
                .get("movieInfo", {})
            )


            if detail:

                detail_runtime = detail.get(
                    "showTm",
                    "-"
                )

                detail_open = detail.get(
                    "openDt",
                    "-"
                )

                detail_genres = ", ".join(
                    genre.get(
                        "genreNm",
                        ""
                    )
                    for genre in detail.get(
                        "genres",
                        []
                    )
                ) or "-"


                st.markdown(
                    f"""
                    <div class="search-card">

                        <div class="search-title">
                            {detail.get("movieNm", "-")}
                        </div>

                        <div class="search-en">
                            {detail.get("movieNmEn", "")}
                        </div>

                        <hr>

                        <b>⏱️ 러닝타임</b>
                        &nbsp; {detail_runtime}분

                        &nbsp;&nbsp; · &nbsp;&nbsp;

                        <b>📅 개봉일</b>
                        &nbsp; {detail_open}

                        &nbsp;&nbsp; · &nbsp;&nbsp;

                        <b>🎬 장르</b>
                        &nbsp; {detail_genres}

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.warning(
                    "상세 영화정보가 없습니다."
                )


# ============================================================
# 21. 상영관 관련 안내
# ============================================================

st.divider()

st.markdown(
    """
    <div class="notice">

        <b>📌 데이터 안내</b><br>

        박스오피스 데이터와 영화 상세정보는
        KOBIS 영화관입장권통합전산망 Open API를 사용합니다.

        <br><br>

        KOBIS의 공개 Open API에서 제공되는 작품정보에는
        영화명, 개봉일, 러닝타임, 장르, 감독, 배우 등의
        정보가 포함됩니다.

        <br><br>

        반면 극장별 <b>실시간 상영관·상영시간표</b>는
        이 Open API에서 제공되는 데이터가 아니므로
        임의의 값을 만들어 표시하지 않습니다.

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 22. 푸터
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

st.caption(
    f"🎬 KOBIS Daily Box Office · {pretty_date}"
)

st.caption(
    "데이터 출처: 영화관입장권통합전산망(KOBIS) Open API"
)
