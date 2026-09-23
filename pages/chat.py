import streamlit as st
from openai import OpenAI


# =========================================================
# 기본 페이지 설정
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
        );

    color: #ffffff;
}

.block-container {
    max-width: 920px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}


/* =====================================================
   상단 헤더
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

    box-shadow:
        0 0 0 1px #0a0a0a,
        0 0 35px rgba(120, 0, 0, 0.18);

    color: #ffffff;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 2px;
}

.cap-name {
    color: #ffffff;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 8px;
    margin-left: 8px;
}

.cap-subtitle {
    margin-top: 8px;
    color: #8a8a8a;
    font-size: 11px;
    letter-spacing: 3px;
}

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


/* =====================================================
   캐릭터 소개
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

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35);
}

.character-label {
    color: #a0a0a0;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    margin-bottom: 9px;
}

.character-description {
    color: #ffffff;
    font-size: 13px;
    line-height: 1.8;
}


/* =====================================================
   모든 채팅 메시지 기본
   ===================================================== */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;

    padding-top: 7px !important;
    padding-bottom: 7px !important;
}


/* =====================================================
   AI 답변 박스
   ===================================================== */

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

    color: #ffffff !important;
}


/* AI 답변 안의 모든 글자를 흰색으로 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] p {

    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}


/* AI 답변 안의 굵은 글씨 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] strong {

    color: #ffffff !important;
}


/* AI 답변 안의 기울임 글씨
   → 행동 지문 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] em {

    color: #ffffff !important;
}


/* =====================================================
   사용자 메시지
   ===================================================== */

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

    color: #ffffff !important;
}


/* 사용자 글자도 흰색 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] p {

    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}


/* =====================================================
   입력창
   ===================================================== */

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

    color: #ffffff !important;
    background: transparent !important;
    font-size: 14px !important;
}

[data-testid="stChatInput"] textarea::placeholder {

    color: #777777 !important;
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
# 상단 화면
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
# Gemini API 연결
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:

    st.warning(
        "AI를 연결할 수 없습니다. 관리자에게 API 키 설정을 확인해 주세요."
    )

    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# =========================================================
# 카피타노 성격 설정
# =========================================================

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 한 대화형 캐릭터다.

[기본 성격]

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

지나치게 딱딱한 공문서 말투는 사용하지 않는다.

인터넷 밈이나 과도한 이모티콘을 사용하지 않는다.

상대가 장난스럽게 말해도 캐릭터성을 유지하면서 자연스럽게 대응한다.


[행동 지문]

대화를 할 때 카피타노의 행동과 분위기를 함께 묘사한다.

매 답변마다 반드시 행동 지문을 포함한다.

행동 지문은 최소 4줄 이상 작성한다.

행동 지문은 반드시 각각 별도의 줄에 작성한다.

행동 지문은 *기울임표시*를 사용한다.

행동 지문은 단순히 같은 행동을 반복해서 채우지 않는다.

상황에 맞게 시선, 자세, 움직임, 침묵, 표정, 주변 분위기 등을 자연스럽게 묘사한다.

행동 지문을 과도하게 화려하게 쓰지 않는다.

카피타노의 과묵하고 절제된 분위기를 유지한다.

행동 지문을 먼저 작성한 뒤 대사를 작성한다.

예시:

*카피타노는 잠시 말없이 상대를 바라본다.*
*그는 천천히 팔짱을 끼고 자세를 바로잡는다.*
*짧은 침묵이 지나간다.*
*그의 시선은 여전히 상대에게 향해 있다.*

"말씀하십시오. 듣고 있습니다."


[대화]

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


[답변 방식]

기본적으로 답변은 간결하게 한다.

그러나 행동 지문은 반드시 최소 4줄 이상 작성한다.

사용자가 자세한 설명을 원하면 충분히 설명한다.

사용자의 질문에는 실제로 도움이 되는 답을 해야 한다.

캐릭터성을 위해 정확성을 희생하지 않는다.

모르는 사실은 아는 척하지 않는다.

캐릭터 설정을 사용자에게 설명하지 않는다.

자신을 AI라고 설명하지 않는다.

한국어로 대화한다.
"""


# =========================================================
# 대화 기록 저장
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

            st.markdown(
                message["content"]
            )

    else:

        with st.chat_message(
            "assistant",
            avatar="⚫"
        ):

            st.markdown(
                message["content"]
            )


# =========================================================
# 사용자 입력
# =========================================================

user_message = st.chat_input(
    "말을 걸어보십시오..."
)


# =========================================================
# 새로운 메시지
# =========================================================

if user_message:

    # 사용자 메시지 표시
    with st.chat_message(
        "user",
        avatar=":material/person:"
    ):

        st.markdown(
            user_message
        )


    # 사용자 메시지 저장
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # Gemini에 전달할 전체 대화
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
    # AI 답변
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="⚫"
    ):

        answer_box = st.empty()

        full_answer = ""


        try:

            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages,
                stream=True
            )


            # 실시간 답변 출력
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

            full_answer = (
                "……지금은 응답할 수 없습니다. "
                "잠시 후 다시 말씀하십시오."
            )

            answer_box.markdown(
                full_answer
            )


    # AI 답변 저장
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": full_answer
        }
    )
