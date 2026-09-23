import streamlit as st
from openai import OpenAI


# =========================================================
# 1. 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="CAPITANO",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 2. 카피타노 분위기의 어두운 UI
# =========================================================
# Streamlit 기본 화면을 검은색 중심으로 바꿉니다.
# 기존 main.py에는 아무 영향도 주지 않습니다.

st.markdown(
    """
    <style>

    /* ---------------------------------------------
       전체 페이지
       --------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #242424 0%,
                #111111 38%,
                #070707 75%,
                #030303 100%
            );
        color: #e7e7e7;
    }


    /* ---------------------------------------------
       기본 여백
       --------------------------------------------- */

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }


    /* ---------------------------------------------
       상단 캐릭터 영역
       --------------------------------------------- */

    .capitano-header {
        text-align: center;
        padding: 18px 0 28px 0;
    }

    .capitano-symbol {
        width: 70px;
        height: 70px;
        margin: 0 auto 14px auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                #3a3a3a 0%,
                #171717 65%,
                #080808 100%
            );

        border: 1px solid #555;

        box-shadow:
            0 0 0 1px #111,
            0 0 25px rgba(120, 0, 0, 0.22);

        font-size: 31px;
    }


    .capitano-name {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: 6px;
        color: #eeeeee;
        margin-bottom: 6px;
    }


    .capitano-title {
        font-size: 12px;
        letter-spacing: 3px;
        color: #777777;
        text-transform: uppercase;
    }


    /* ---------------------------------------------
       구분선
       --------------------------------------------- */

    .dark-line {
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #444444,
                #7d1616,
                #444444,
                transparent
            );

        margin: 0 0 30px 0;
    }


    /* ---------------------------------------------
       캐릭터 소개 카드
       --------------------------------------------- */

    .character-card {
        background:
            linear-gradient(
                135deg,
                rgba(40, 40, 40, 0.72),
                rgba(10, 10, 10, 0.92)
            );

        border: 1px solid #292929;
        border-left: 2px solid #5f1717;

        border-radius: 4px;

        padding: 18px 22px;
        margin-bottom: 30px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.35);
    }


    .character-card-title {
        color: #b9b9b9;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }


    .character-card-text {
        color: #777777;
        font-size: 13px;
        line-height: 1.7;
    }


    /* ---------------------------------------------
       Streamlit 채팅 말풍선
       --------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding-top: 8px;
        padding-bottom: 8px;
    }


    /* ---------------------------------------------
       AI 메시지
       --------------------------------------------- */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                135deg,
                #171717,
                #0d0d0d
            );

        border: 1px solid #292929;
        border-left: 2px solid #631818;

        border-radius: 3px;

        padding: 15px 18px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.28);
    }


    /* ---------------------------------------------
       사용자 메시지
       --------------------------------------------- */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                135deg,
                #222222,
                #181818
            );

        border: 1px solid #303030;

        border-radius: 3px;

        padding: 15px 18px;
    }


    /* ---------------------------------------------
       AI 아바타
       --------------------------------------------- */

    [data-testid="chatAvatarIcon-assistant"] {
        background: #151515 !important;
        border: 1px solid #444 !important;
    }


    /* ---------------------------------------------
       사용자 아바타
       --------------------------------------------- */

    [data-testid="chatAvatarIcon-user"] {
        background: #252525 !important;
        border: 1px solid #444 !important;
    }


    /* ---------------------------------------------
       입력창
       --------------------------------------------- */

    [data-testid="stChatInput"] {
        background: transparent;
    }


    [data-testid="stChatInput"] > div {
        background:
            linear-gradient(
                135deg,
                #171717,
                #0d0d0d
            ) !important;

        border: 1px solid #3a3a3a !important;

        border-radius: 4px !important;

        box-shadow:
            0 0 30px rgba(0, 0, 0, 0.5);
    }


    [data-testid="stChatInput"] textarea {
        color: #eeeeee !important;
        background: transparent !important;
    }


    [data-testid="stChatInput"] textarea::placeholder {
        color: #626262 !important;
    }


    /* ---------------------------------------------
       버튼
       --------------------------------------------- */

    [data-testid="stChatInput"] button {
        color: #aaaaaa !important;
    }


    /* ---------------------------------------------
       일반 글자
       --------------------------------------------- */

    .stMarkdown {
        color: #dddddd;
    }


    /* ---------------------------------------------
       스크롤바
       --------------------------------------------- */

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #050505;
    }

    ::-webkit-scrollbar-thumb {
        background: #292929;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #444444;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. 상단 캐릭터 헤더
# =========================================================

st.markdown(
    """
    <div class="capitano-header">

        <div class="capitano-symbol">
            ⚔
        </div>

        <div class="capitano-name">
            CAPITANO
        </div>

        <div class="capitano-title">
            THE CAPTAIN · FATUI HARBINGER
        </div>

    </div>

    <div class="dark-line"></div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. 캐릭터 소개
# =========================================================
# 캐릭터 설정 자체를 전부 노출하지 않고
# 화면에는 분위기만 보여줍니다.

st.markdown(
    """
    <div class="character-card">

        <div class="character-card-title">
            THE CAPTAIN
        </div>

        <div class="character-card-text">
            말보다 행동을 중시하는 자.
            <br>
            조용하고 냉정하며, 자신의 책임을 쉽게 내려놓지 않는다.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 5. Gemini API 키 가져오기
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:

    st.warning(
        "AI를 연결할 수 없습니다. 관리자에게 API 키 설정을 확인해 주세요."
    )

    st.stop()


# =========================================================
# 6. Gemini OpenAI 호환 API 연결
# =========================================================

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# =========================================================
# 7. 카피타노 캐릭터 성격
# =========================================================
# 이 내용은 화면에 표시되지 않습니다.
# AI에게만 전달됩니다.

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 만들어진 대화형 캐릭터다.

너의 핵심은 강함 그 자체가 아니라
강한 힘을 책임과 보호를 위해 사용하는 태도다.

말수가 적고 과묵하다.
필요하지 않은 말을 길게 하지 않는다.

항상 침착하고 절제되어 있다.
갑작스러운 상황에서도 쉽게 흥분하거나 당황하지 않는다.

감정을 느끼지 않는 것이 아니다.
감정을 쉽게 밖으로 드러내지 않을 뿐이다.

동료와 자신이 책임져야 할 사람들을 중요하게 생각한다.
겉으로는 무심해 보여도 상대의 안전과 상황을 세심하게 살핀다.

자신이 맡은 책임을 다른 사람에게 쉽게 떠넘기지 않는다.

명예, 책임, 신뢰, 의무를 중요하게 생각한다.

상대가 적이라고 해도 능력과 용기를 인정할 수 있다.
상대방을 함부로 모욕하거나 깎아내리지 않는다.

자신의 강함을 과시하기 위해 말하지 않는다.
힘을 자랑하기보다 필요할 때 행동으로 보여준다.

말투는 낮고 차분하며 무게감이 있다.

항상 정중한 존댓말을 사용한다.

하지만 지나치게 딱딱한 공문서 말투는 사용하지 않는다.

인터넷 밈이나 과도한 이모티콘을 사용하지 않는다.

상대가 장난스럽게 말해도 캐릭터성을 잃지 않는다.

상대가 고민을 이야기하면 먼저 상황을 파악한다.
쓸데없는 위로나 장황한 말을 하지 않는다.

필요한 경우 짧고 정확한 조언을 한다.

상대를 무시하지 않는다.
상대가 실수했다고 해서 모욕하지 않는다.

칭찬할 때는 과장하지 않는다.
상대가 잘한 부분을 정확하게 짚어 짧게 인정한다.

걱정할 때는 감정적으로 호들갑을 떨지 않는다.
대신 현실적으로 도움이 되는 행동이나 방법을 제시한다.

화가 났을 때 소리를 지르지 않는다.
말수가 줄어들고 표현이 더욱 단호해진다.

슬플 때 감정을 장황하게 설명하지 않는다.
짧은 말이나 침묵으로 감정을 드러낸다.

기본적으로 답변은 간결하게 한다.
다만 사용자가 자세한 설명을 요청하면 충분히 설명한다.

사용자의 질문에는 실제로 도움이 되는 답을 해야 한다.
캐릭터성을 위해 답변의 정확성을 희생하지 않는다.

자신이 모르는 사실을 아는 척하지 않는다.

카피타노라는 캐릭터 설정을 사용자에게 설명하지 않는다.

자신을 AI라고 설명하지 않는다.

대화 중 캐릭터의 성격을 메타적으로 분석하거나 설명하지 않는다.

한국어로 대화한다.
"""


# =========================================================
# 8. 대화 기록 저장
# =========================================================
# 페이지가 다시 실행되어도 현재 대화가 유지됩니다.

if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = []


# =========================================================
# 9. 이전 대화 표시
# =========================================================

for message in st.session_state.chat_messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar=":material/person:"
        ):
            st.markdown(message["content"])

    else:

        with st.chat_message(
            "assistant",
            avatar="⚔"
        ):
            st.markdown(message["content"])


# =========================================================
# 10. 사용자 입력창
# =========================================================

user_message = st.chat_input(
    "말을 걸어보십시오..."
)


# =========================================================
# 11. 새로운 메시지를 입력했을 때
# =========================================================

if user_message:

    # ---------------------------------------------
    # 사용자 메시지 표시
    # ---------------------------------------------

    with st.chat_message(
        "user",
        avatar=":material/person:"
    ):

        st.markdown(user_message)


    # ---------------------------------------------
    # 사용자 메시지 저장
    # ---------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # =====================================================
    # 12. AI에게 보낼 전체 대화 만들기
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    # 지금까지의 대화를 모두 전달합니다.
    messages.extend(
        st.session_state.chat_messages
    )


    # =====================================================
    # 13. AI 답변 생성
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="⚔"
    ):

        answer_box = st.empty()

        full_answer = ""

        try:

            # 스트리밍 방식으로 답변을 받습니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages,
                stream=True
            )


            # ---------------------------------------------
            # 답변이 생성되는 즉시 화면에 출력
            # ---------------------------------------------

            for chunk in response:

                if not chunk.choices:
                    continue

                text = chunk.choices[0].delta.content

                if text:

                    full_answer += text

                    answer_box.markdown(
                        full_answer + "▌"
                    )


            # 마지막 커서 제거
            answer_box.markdown(
                full_answer
            )


        except Exception:

            # API 오류 내용을 사용자에게 그대로 노출하지 않습니다.

            full_answer = (
                "……잠시 기다려 주십시오. "
                "지금은 응답을 가져올 수 없습니다."
            )

            answer_box.markdown(
                full_answer
            )


    # =====================================================
    # 14. AI 답변 저장
    # =====================================================

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": full_answer
        }
    )
