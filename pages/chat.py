import streamlit as st
from openai import OpenAI
import html
import re


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="CAPITANO",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 화면 디자인
# =========================================================

st.html("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            #252525 0%,
            #111111 35%,
            #080808 70%,
            #030303 100%
        ) !important;
}

.block-container {
    max-width: 920px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}


/* =====================================================
   헤더
   ===================================================== */

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

    color: #ffffff !important;

    font-size: 25px;
    font-weight: 700;
    letter-spacing: 2px;
}

.cap-name {
    color: #ffffff !important;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 8px;
}

.cap-subtitle {
    margin-top: 8px;
    color: #999999 !important;
    font-size: 11px;
    letter-spacing: 3px;
}

.cap-line {
    width: 100%;
    height: 1px;
    margin-bottom: 30px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #292929 25%,
            #651818 50%,
            #292929 75%,
            transparent
        );
}


/* =====================================================
   캐릭터 카드
   ===================================================== */

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
}

.character-label {
    color: #aaaaaa !important;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    margin-bottom: 9px;
}

.character-description {
    color: #ffffff !important;
    font-size: 13px;
    line-height: 1.8;
}


/* =====================================================
   채팅 전체
   ===================================================== */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;

    padding-top: 7px !important;
    padding-bottom: 7px !important;

    opacity: 1 !important;
}


/* =====================================================
   사용자 / AI 메시지 내용
   ===================================================== */

.chat-bubble-text {
    color: #ffffff !important;

    font-size: 15px !important;
    line-height: 1.85 !important;

    opacity: 1 !important;

    -webkit-text-fill-color: #ffffff !important;

    white-space: normal;

    word-break: break-word;
}

.chat-bubble-text * {
    color: #ffffff !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #ffffff !important;
}

.chat-action {
    color: #ffffff !important;

    font-style: italic;

    opacity: 1 !important;

    -webkit-text-fill-color: #ffffff !important;
}

.chat-dialogue {
    color: #ffffff !important;

    opacity: 1 !important;

    -webkit-text-fill-color: #ffffff !important;
}


/* =====================================================
   사용자 메시지 박스
   ===================================================== */

.user-bubble {
    background:
        linear-gradient(
            135deg,
            #242424,
            #181818
        );

    border: 1px solid #303030;
    border-radius: 4px;

    padding: 14px 18px;

    color: #ffffff !important;

    opacity: 1;
}


/* =====================================================
   AI 메시지 박스
   ===================================================== */

.ai-bubble {
    background:
        linear-gradient(
            135deg,
            #191919,
            #0e0e0e
        );

    border: 1px solid #292929;
    border-left: 2px solid #641919;

    border-radius: 4px;

    padding: 14px 18px;

    color: #ffffff !important;

    opacity: 1;

    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.30);
}


/* =====================================================
   입력창
   ===================================================== */

[data-testid="stChatInput"] {
    opacity: 1 !important;
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
}

[data-testid="stChatInput"] textarea {

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    background: transparent !important;

    font-size: 14px !important;

    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder {

    color: #777777 !important;
    -webkit-text-fill-color: #777777 !important;
}


/* =====================================================
   스크롤바
   ===================================================== */

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
# 헤더
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
# 캐릭터 소개
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
# 메시지 표시 함수
# =========================================================

def make_message_html(text, bubble_class):
    """
    메시지를 HTML로 만들어서 표시합니다.

    *행동 지문*
    형태는 자동으로 행동 지문으로 처리합니다.
    """

    # HTML 특수문자 보호
    safe_text = html.escape(text)

    # *행동 지문* 처리
    safe_text = re.sub(
        r"\*([^*\n]+)\*",
        r'<span class="chat-action">*\1*</span>',
        safe_text
    )

    # 줄바꿈 처리
    safe_text = safe_text.replace("\n", "<br>")

    return f"""
    <div class="{bubble_class}">
        <div class="chat-bubble-text">
            {safe_text}
        </div>
    </div>
    """


# =========================================================
# Gemini API 연결
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:

    st.error(
        "GEMINI_API_KEY가 설정되어 있지 않습니다. "
        "Streamlit Secrets를 확인해 주세요."
    )

    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# =========================================================
# 카피타노 시스템 설정
# =========================================================

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 한 대화형 캐릭터다.

말수가 적고 과묵하다.

항상 침착하고 절제되어 있다.

말투는 낮고 차분하며 무게감이 있다.

항상 정중한 존댓말을 사용한다.

명예, 책임, 신뢰, 의무를 중요하게 생각한다.

상대를 함부로 모욕하지 않는다.

상대가 고민을 이야기하면 상황을 먼저 파악한다.

필요한 경우 짧고 정확한 조언을 한다.

과도한 이모티콘이나 인터넷 밈을 사용하지 않는다.

자신을 AI라고 설명하지 않는다.

캐릭터 설정 자체를 사용자에게 설명하지 않는다.

한국어로 대화한다.


━━━━━━━━━━━━━━━━━━━━
행동 지문 시스템
━━━━━━━━━━━━━━━━━━━━

행동 지문은 별표 두 개 사이에 작성한다.

예:

*카피타노는 잠시 상대를 바라본다.*

행동 지문은 행동, 표정, 시선, 자세,
움직임, 침묵, 주변 분위기를 표현한다.


[사용자의 행동]

사용자가 *별표* 안에 문장을 작성하면
그것을 사용자의 행동 지문으로 인식한다.

예:

*고개를 끄덕인다.*

이것은 사용자가 실제로 고개를 끄덕인 것이다.

예:

*카피타노를 바라본다.*

이것은 사용자가 카피타노를 바라보는 행동이다.

사용자의 행동 지문을 대사로 착각하지 않는다.

사용자가 행동 지문과 대사를 함께 작성하면
둘을 구분해서 이해한다.

예:

*고개를 살짝 기울인다.*

그런데 왜 그렇게 생각하십니까?


[카피타노의 행동]

카피타노 역시 행동 지문을 사용한다.

모든 답변에는 반드시 행동 지문을 포함한다.

행동 지문은 최소 4줄 이상 작성한다.

각 행동 지문은 반드시 별도의 줄에 작성한다.

행동 지문은 반드시 *별표*로 감싼다.

행동 지문을 먼저 작성하고 대사를 작성한다.

예:

*카피타노는 잠시 말없이 상대를 바라본다.*

*그는 천천히 자세를 바로잡는다.*

*짧은 침묵이 이어진다.*

*그의 시선이 다시 상대에게 향한다.*

"말씀하십시오. 듣고 있습니다."


[행동 지문 규칙]

같은 행동을 반복해서 사용하지 않는다.

상황에 맞게 시선, 자세, 손동작, 표정,
걸음, 침묵 등을 자연스럽게 묘사한다.

과도하게 화려한 문체를 사용하지 않는다.

카피타노 특유의 절제되고 무게감 있는 분위기를 유지한다.

행동 지문만 계속 작성하지 않는다.

행동 지문 이후 반드시 실제 대화를 한다.


[대화 규칙]

상대가 고민을 이야기하면 상황을 먼저 파악한다.

불필요한 위로나 장황한 말을 하지 않는다.

필요한 경우 현실적으로 도움이 되는 방법을 제시한다.

상대를 무시하지 않는다.

상대를 모욕하지 않는다.

칭찬할 때 과장하지 않는다.

걱정할 때 호들갑스럽게 반응하지 않는다.

화가 났을 때 소리를 지르지 않는다.

감정을 과장해서 설명하지 않는다.

한국어로 대화한다.
"""


# =========================================================
# 대화 기록
# =========================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =========================================================
# 이전 대화 표시
# =========================================================

for message in st.session_state.chat_messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar=":material/person:"
        ):

            st.html(
                make_message_html(
                    message["content"],
                    "user-bubble"
                )
            )

    else:

        with st.chat_message(
            "assistant",
            avatar="⚫"
        ):

            st.html(
                make_message_html(
                    message["content"],
                    "ai-bubble"
                )
            )


# =========================================================
# 사용자 입력
# =========================================================

user_message = st.chat_input(
    "말을 걸어보십시오..."
)


# =========================================================
# 새 메시지
# =========================================================

if user_message:

    # -----------------------------------------------------
    # 사용자 메시지 화면 표시
    # -----------------------------------------------------

    with st.chat_message(
        "user",
        avatar=":material/person:"
    ):

        st.html(
            make_message_html(
                user_message,
                "user-bubble"
            )
        )


    # -----------------------------------------------------
    # 사용자 메시지 저장
    # -----------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # -----------------------------------------------------
    # Gemini에 전달할 대화
    # -----------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    messages.extend(
        st.session_state.chat_messages
    )


    # -----------------------------------------------------
    # AI 응답
    # -----------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="⚫"
    ):

        try:

            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages
            )

            answer = response.choices[0].message.content

            if not answer:
                answer = "……."

            # AI 답변 표시
            st.html(
                make_message_html(
                    answer,
                    "ai-bubble"
                )
            )


            # AI 답변 저장
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception:

            st.html(
                make_message_html(
                    "……지금은 응답할 수 없습니다. 잠시 후 다시 말씀하십시오.",
                    "ai-bubble"
                )
)
