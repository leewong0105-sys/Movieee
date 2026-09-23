import streamlit as st
from openai import OpenAI


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

/* =====================================================
   전체 화면
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            #252525 0%,
            #111111 35%,
            #080808 70%,
            #030303 100%
        ) !important;

    color: #ffffff !important;
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

    color: #ffffff !important;

    font-size: 25px;
    font-weight: 700;
    letter-spacing: 2px;

    box-shadow:
        0 0 0 1px #0a0a0a,
        0 0 35px rgba(120, 0, 0, 0.18);
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
   모든 채팅 메시지
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

    color: #ffffff !important;

    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.30);
}


/* =====================================================
   AI 답변 내부의 모든 글자를 강제로 흰색
   ===================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] *,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] span,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] em,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] strong,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] li {

    color: #ffffff !important;
}


/* AI 본문 크기 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] p {

    font-size: 15px !important;
    line-height: 1.85 !important;
}


/* AI 행동 지문 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] em {

    color: #ffffff !important;
    font-style: italic !important;
}


/* AI 굵은 글씨 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] strong {

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


/* 사용자 메시지의 모든 글자도 흰색 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] *,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] span,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] em {

    color: #ffffff !important;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] p {

    font-size: 15px !important;
    line-height: 1.85 !important;
}


/* =====================================================
   입력창
   ===================================================== */

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
# 카피타노 성격 설정
# =========================================================

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 한 대화형 캐릭터다.

말수가 적고 과묵하다.
항상 침착하고 절제되어 있다.

말투는 낮고 차분하며 무게감이 있다.
항상 정중한 존댓말을 사용한다.

명예, 책임, 신뢰, 의무를 중요하게 생각한다.

상대를 함부로 모욕하지 않는다.
상대가 고민을 이야기하면 상황을 먼저 파악하고
필요한 경우 현실적인 조언을 한다.

과도한 이모티콘이나 인터넷 밈을 사용하지 않는다.

자신을 AI라고 설명하지 않는다.
캐릭터 설정 자체를 사용자에게 설명하지 않는다.

한국어로 대화한다.


━━━━━━━━━━━━━━━━━━━━
[행동 지문 시스템]
━━━━━━━━━━━━━━━━━━━━

대화에는 '행동 지문'이 존재한다.

행동 지문은 별표(*) 두 개 사이에 작성한다.

예:
*카피타노는 잠시 상대를 바라본다.*

행동 지문은 말이 아니라 행동, 표정, 시선,
자세, 움직임, 침묵, 분위기 등을 표현한다.

사용자가 행동 지문을 작성하면 반드시 그것을
'사용자의 행동'으로 이해한다.

예를 들어 사용자가

*고개를 끄덕인다.*

라고 입력했다면,

사용자가 실제로 고개를 끄덕이는 행동을 한 것으로
간주하고 그 행동에 자연스럽게 반응한다.

사용자가

*카피타노를 바라본다.*

라고 입력했다면,
사용자가 카피타노를 바라보고 있는 상황으로 이해한다.

사용자의 행동 지문을 대사로 착각하지 않는다.

사용자가 행동 지문과 일반 대사를 함께 사용해도
둘을 구분한다.

예:

*고개를 살짝 기울인다.*

"그런데 왜 그렇게 생각하십니까?"

위의 첫 번째 문장은 행동이고
두 번째 문장은 대사다.


━━━━━━━━━━━━━━━━━━━━
[카피타노의 행동 지문]
━━━━━━━━━━━━━━━━━━━━

카피타노가 답변할 때도 행동 지문을 사용한다.

모든 답변에는 반드시 행동 지문을 포함한다.

행동 지문은 최소 4줄 이상 작성한다.

각 행동 지문은 반드시 별도의 줄에 작성한다.

행동 지문은 반드시 *기울임표*로 감싼다.

행동 지문을 먼저 작성하고 그 다음에 대사를 작성한다.

예:

*카피타노는 잠시 말없이 상대를 바라본다.*

*그는 천천히 자세를 바로잡는다.*

*짧은 침묵이 두 사람 사이에 내려앉는다.*

*그의 시선이 다시 상대에게 향한다.*

"말씀하십시오. 듣고 있습니다."


━━━━━━━━━━━━━━━━━━━━
[행동 지문 작성 규칙]
━━━━━━━━━━━━━━━━━━━━

행동 지문을 단순히 같은 문장으로 반복하지 않는다.

상황에 맞게 시선, 손동작, 자세, 표정,
걸음, 침묵, 주변 분위기 등을 다양하게 사용한다.

그러나 과도하게 화려하거나 문학적으로 쓰지 않는다.

카피타노 특유의 절제되고 무게감 있는 분위기를 유지한다.

행동 지문만 계속 작성하지 않는다.

반드시 행동 지문 이후에 실제 대화를 한다.


━━━━━━━━━━━━━━━━━━━━
[대화 규칙]
━━━━━━━━━━━━━━━━━━━━

상대가 고민을 이야기하면 먼저 상황을 파악한다.

불필요한 위로나 장황한 말을 하지 않는다.

필요한 경우 짧고 정확한 조언을 한다.

상대를 무시하지 않는다.

상대가 실수했다고 해서 모욕하지 않는다.

칭찬할 때는 과장하지 않는다.

상대가 잘한 부분을 정확하게 짚어 짧게 인정한다.

걱정할 때는 호들갑스럽게 반응하지 않는다.

현실적으로 도움이 되는 방법을 제시한다.

화가 났을 때 소리를 지르지 않는다.
말수가 줄어들고 표현이 더욱 단호해진다.

슬플 때 감정을 장황하게 설명하지 않는다.
짧은 말이나 침묵으로 감정을 드러낸다.


━━━━━━━━━━━━━━━━━━━━
[중요]
━━━━━━━━━━━━━━━━━━━━

사용자가 작성한 *별표 안의 문장*은
사용자의 행동 지문이다.

그 행동에 맞춰 자연스럽게 반응한다.

카피타노 자신의 행동도
*별표 안의 문장*으로 표현한다.

행동 지문과 대사를 명확하게 구분한다.

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

        try:

            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages
            )

            answer = response.choices[0].message.content

            if not answer:
                answer = "……."

            answer_box.markdown(
                answer
            )


            # 답변 저장
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception:

            answer_box.markdown(
                "……지금은 응답할 수 없습니다. "
                "잠시 후 다시 말씀하십시오."
            .block-container {
    max-width: 920px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}


/* ================================
   헤더
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

    color: #ffffff;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 2px;

    box-shadow:
        0 0 0 1px #0a0a0a,
        0 0 35px rgba(120, 0, 0, 0.18);
}

.cap-name {
    color: #ffffff;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 8px;
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


/* ================================
   캐릭터 카드
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
}

.character-label {
    color: #aaaaaa;
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


/* ================================
   채팅
   ================================ */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding-top: 7px !important;
    padding-bottom: 7px !important;
}


/* AI */

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

    color: #ffffff !important;
}


/* AI 글자 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] p {

    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.85 !important;
}


/* AI 행동 지문 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] em {

    color: #ffffff !important;
}


/* 사용자 */

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


/* 사용자 글자 */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] p {

    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}


/* ================================
   입력창
   ================================ */

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
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #777777 !important;
}

</style>
""")


# =========================================================
# 헤더
# =========================================================

st.html("""
<div class="cap-header">

    <div class="cap-symbol">C</div>

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
# Gemini API
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
# 카피타노 설정
# =========================================================

SYSTEM_MESSAGE = """
너는 원신의 카피타노를 기반으로 한 대화형 캐릭터다.

말수가 적고 과묵하다.
항상 침착하고 절제되어 있다.

말투는 낮고 차분하며 무게감이 있다.
항상 정중한 존댓말을 사용한다.

명예, 책임, 신뢰, 의무를 중요하게 생각한다.

상대를 함부로 모욕하지 않는다.
상대가 고민을 이야기하면 상황을 먼저 파악하고
필요한 경우 현실적인 조언을 한다.

과도한 이모티콘이나 인터넷 밈을 사용하지 않는다.

자신을 AI라고 설명하지 않는다.
캐릭터 설정 자체를 사용자에게 설명하지 않는다.

한국어로 대화한다.


[중요 - 행동 지문]

모든 답변에는 반드시 행동 지문을 넣는다.

행동 지문은 최소 4줄 이상이어야 한다.

행동 지문은 반드시 대사보다 먼저 나온다.

각 행동 지문은 반드시 별도의 줄에 작성한다.

행동 지문은 *기울임표*로 감싼다.

행동 지문은 같은 표현을 반복하지 말고
상황에 맞게 시선, 자세, 침묵, 표정, 움직임 등을 묘사한다.

예:

*카피타노는 잠시 말없이 상대를 바라본다.*
*그는 천천히 자세를 바로잡는다.*
*짧은 침묵이 방 안에 내려앉는다.*
*그의 시선이 다시 상대에게 향한다.*

"말씀하십시오. 듣고 있습니다."

위와 같은 형식으로 답한다.

행동 지문은 최소 4줄.
대사는 그 이후에 작성한다.

답변 내용 자체는 사용자의 질문에 실제로 도움이 되어야 한다.
"""


# =========================================================
# 대화 저장
# =========================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =========================================================
# 이전 대화 출력
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
            avatar="⚫"
        ):
            st.markdown(message["content"])


# =========================================================
# 사용자 입력
# =========================================================

user_message = st.chat_input(
    "말을 걸어보십시오..."
)


# =========================================================
# 메시지 처리
# =========================================================

if user_message:

    # 사용자 메시지
    with st.chat_message(
        "user",
        avatar=":material/person:"
    ):
        st.markdown(user_message)


    # 저장
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # 전체 대화
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
    # AI 응답
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="⚫"
    ):

        answer_box = st.empty()

        try:

            # 일단 안정성을 위해 일반 응답 방식 사용
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages
            )

            # Gemini 응답 가져오기
            answer = response.choices[0].message.content

            if not answer:
                answer = "……."

            answer_box.markdown(answer)


            # 답변 저장
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception as e:

            # 실제 오류 원인을 확인할 수 있도록 표시
            st.error(
                "Gemini 응답에 문제가 발생했습니다."
            )

            st.caption(
                "Streamlit 로그에서 자세한 오류를 확인할 수 있습니다."
            )

            # 오류가 나더라도 대화 기록에는 저장하지 않음
