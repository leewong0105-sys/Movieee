import streamlit as st
from openai import OpenAI


# =========================================================
# 1. 페이지 설정
# =========================================================

st.set_page_config(
    page_title="CAPITANO",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 2. 전체 화면 디자인
# =========================================================
# HTML과 CSS는 st.html()을 사용합니다.
# 이렇게 하면 HTML 태그가 화면에 글자로 나타나는 문제를 피할 수 있습니다.

st.html("""
<style>

    /* ================================
       전체 배경
       ================================ */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                #252525 0%,
                #111111 35%,
                #080808 70%,
                #030303 100%
            );
        color: #e5e5e5;
    }


    /* ================================
       Streamlit 기본 여백
       ================================ */

    .block-container {
        max-width: 920px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }


    /* ================================
       상단 캐릭터 헤더
       ================================ */

    .cap-header {
        text-align: center;
        padding: 20px 0 26px 0;
    }

    .cap-symbol {
        width: 72px;
        height: 72px;

        margin: 0 auto 16px auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                #353535 0%,
                #171717 60%,
                #090909 100%
            );

        border: 1px solid #4c4c4c;

        box-shadow:
            0 0 0 1px #0a0a0a,
            0 0 35px rgba(120, 0, 0, 0.18);

        color: #cfcfcf;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: 2px;
    }


    .cap-name {
        color: #ededed;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 8px;
        margin-left: 8px;
    }


    .cap-subtitle {
        margin-top: 8px;

        color: #696969;

        font-size: 11px;
        letter-spacing: 3px;
    }


    /* ================================
       붉은 구분선
       ================================ */

    .cap-line {
        width: 100%;
        height: 1px;

        margin: 0 0 30px 0;

        background:
            linear-gradient(
                90deg,
                transparent 0%,
                #292929 25%,
                #651818 50%,
                #292929 75%,
                transparent 100%
            );
    }


    /* ================================
       캐릭터 소개
       ================================ */

    .character-card {
        padding: 18px 22px;
        margin-bottom: 32px;

        background:
            linear-gradient(
                135deg,
                rgba(30, 30, 30, 0.95),
                rgba(12, 12, 12, 0.98)
            );

        border: 1px solid #282828;
        border-left: 2px solid #681919;

        border-radius: 4px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.35);
    }


    .character-label {
        color: #8d8d8d;

        font-size: 10px;
        font-weight: 600;
        letter-spacing: 3px;

        margin-bottom: 9px;
    }


    .character-description {
        color: #a0a0a0;

        font-size: 13px;
        line-height: 1.8;
    }


    /* ================================
       채팅 메시지
       ================================ */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;

        padding-top: 7px !important;
        padding-bottom: 7px !important;
    }


    /* AI 말풍선 */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                135deg,
                #191919,
                #0e0e0e
            ) !important;

        border: 1px solid #292929 !important;
        border-left: 2px solid #641919 !important;

        border-radius: 4px !important;

        padding: 14px 18px !important;

        box-shadow:
            0 8px 28px rgba(0, 0, 0, 0.30);
    }


    /* 사용자 말풍선 */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                135deg,
                #242424,
                #181818
            ) !important;

        border: 1px solid #303030 !important;

        border-radius: 4px !important;

        padding: 14px 18px !important;
    }


    /* ================================
       채팅 입력창
       ================================ */

    [data-testid="stChatInput"] {
        background: transparent !important;
    }


    [data-testid="stChatInput"] > div {

        background:
            linear-gradient(
                135deg,
                #191919,
                #0d0d0d
            ) !important;

        border: 1px solid #3a3a3a !important;

        border-radius: 5px !important;

        box-shadow:
            0 0 30px rgba(0, 0, 0, 0.55);
    }


    [data-testid="stChatInput"] textarea {

        color: #eeeeee !important;

        background: transparent !important;

        font-size: 14px !important;
    }


    [data-testid="stChatInput"] textarea::placeholder {
        color: #606060 !important;
    }


    /* ================================
       스크롤바
       ================================ */

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
""")


# =========================================================
# 3. 상단 캐릭터 화면
# =========================================================

st.html("""
<div class="cap-header">

    <div class="cap-symbol">
        C
    </div>

    <div class="cap-name">
        CAPITANO
    </div>

    <div class="cap-subtitle">
        THE CAPTAIN · FATUI HARBINGER
    </div>

</div>

<div class="cap-line"></div>
""")


# =========================================================
# 4. 캐릭터 소개 카드
# =========================================================

st.html("""
<div class="character-card">

    <div class="character-label">
        THE CAPTAIN
    </div>

    <div class="character-description">
        말보다 행동을 중시하는 자.
        <br>
        조용하고 냉정하며, 자신의 책임을 쉽게 내려놓지 않는다.
    </div>

</div>
""")


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
# 6. Gemini 연결
# =========================================================

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# =========================================================
# 7. 카피타노 성격 설정
# =========================================================
# 이 내용은 화면에 표시되지 않습니다.
# AI에게만 전달됩니다.

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 한 대화형 캐릭터다.

말수가 적고 과묵하다.
필요하지 않은 말을 길게 하지 않는다.

항상 침착하고 절제되어 있다.
갑작스러운 상황에서도 쉽게 흥분하거나 당황하지 않는다.

감정을 느끼지 않는 것이 아니라 감정을 쉽게 밖으로 드러내지 않는다.

동료와 자신이 책임져야 할 사람들을 중요하게 생각한다.
겉으로는 무심해 보여도 상대의 안전과 상황을 세심하게 살핀다.

자신이 맡은 책임을 다른 사람에게 쉽게 떠넘기지 않는다.

명예, 책임, 신뢰, 의무를 중요하게 생각한다.

상대의 능력과 용기를 인정할 줄 안다.
상대를 함부로 모욕하거나 깎아내리지 않는다.

자신의 강함을 과시하기 위해 말하지 않는다.
힘을 자랑하기보다 행동으로 보여준다.

말투는 낮고 차분하며 무게감이 있다.

항상 정중한 존댓말을 사용한다.

그러나 지나치게 딱딱한 공문서 말투는 사용하지 않는다.

인터넷 밈이나 과도한 이모티콘을 사용하지 않는다.

상대가 장난스럽게 말해도 캐릭터성을 유지하면서 자연스럽게 대응한다.

상대가 고민을 이야기하면 먼저 상황을 파악한다.
불필요한 위로나 장황한 말을 하지 않는다.

필요한 경우 짧고 정확한 조언을 한다.

상대를 무시하지 않는다.
상대가 실수했다고 해서 모욕하지 않는다.

칭찬할 때는 과장하지 않는다.
상대가 잘한 부분을 정확하게 짚어 짧게 인정한다.

걱정할 때는 호들갑스럽게 반응하지 않는다.
대신 현실적으로 도움이 되는 방법을 제시한다.

화가 났을 때 소리를 지르지 않는다.
말수가 줄어들고 표현이 더욱 단호해진다.

슬플 때 감정을 장황하게 설명하지 않는다.
짧은 말이나 침묵으로 감정을 드러낸다.

기본적으로 답변은 간결하게 한다.
사용자가 자세한 설명을 원하면 충분히 설명한다.

사용자의 질문에는 실제로 도움이 되는 답을 해야 한다.
캐릭터성을 위해 정확성을 희생하지 않는다.

모르는 사실은 아는 척하지 않는다.

캐릭터 설정을 사용자에게 설명하지 않는다.

자신을 AI라고 설명하지 않는다.

한국어로 대화한다.
"""


# =========================================================
# 8. 대화 기록
# =========================================================

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
            avatar="C"
        ):
            st.markdown(message["content"])


# =========================================================
# 10. 사용자 입력
# =========================================================

user_message = st.chat_input(
    "말을 걸어보십시오..."
)


# =========================================================
# 11. 새로운 메시지가 들어왔을 때
# =========================================================

if user_message:

    # 사용자 메시지 표시
    with st.chat_message(
        "user",
        avatar=":material/person:"
    ):
        st.markdown(user_message)

    # 사용자 메시지 저장
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # =====================================================
    # 12. AI에게 전달할 전체 대화
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    messages.extend(
        st.session_state.chat_messages
    )


    # =====================================================
    # 13. AI 답변 생성
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="C"
    ):

        answer_box = st.empty()

        full_answer = ""

        try:

            # 답변을 실시간으로 조금씩 받아옵니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages,
                stream=True
            )

            # 들어오는 답변을 화면에 계속 이어서 출력합니다.
            for chunk in response:

                if not chunk.choices:
                    continue

                text = chunk.choices[0].delta.content

                if text:

                    full_answer += text

                    answer_box.markdown(
                        full_answer + "▌"
                    )

            # 답변 완료 후 커서 제거
            answer_box.markdown(
                full_answer
            )


        except Exception:

            # 실제 API 오류 내용을 그대로 보여주지 않습니다.
            full_answer = (
                "……지금은 응답할 수 없습니다. "
                "잠시 후 다시 말씀하십시오."
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
