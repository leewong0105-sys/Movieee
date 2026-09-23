import streamlit as st
from openai import OpenAI


# -----------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------

st.set_page_config(
    page_title="AI 채팅",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI 채팅")
st.caption("궁금한 것을 편하게 물어보세요.")


# -----------------------------------------
# 2. Gemini API 키 가져오기
# -----------------------------------------
# API 키는 코드에 직접 적지 않고
# Streamlit Secrets의 GEMINI_API_KEY에서 가져옵니다.

if "GEMINI_API_KEY" not in st.secrets:
    st.warning("AI 채팅을 사용할 수 없습니다. 관리자에게 API 키 설정을 요청해주세요.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]


# -----------------------------------------
# 3. Gemini를 OpenAI 라이브러리로 연결
# -----------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# -----------------------------------------
# 4. AI의 성격 설정
# -----------------------------------------
# 이 문장은 화면에 표시하지 않고
# AI에게만 전달합니다.

SYSTEM_MESSAGE = """
너는 중고등학생에게 설명하는 친절한 정보 선생님이야.
어려운 말은 쉬운 말로 바꿔 주고, 반드시 순수 한국어로만 답해.
"""


# -----------------------------------------
# 5. 대화 기록 만들기
# -----------------------------------------
# st.session_state를 사용하면 페이지가 다시 실행되어도
# 현재 사용자의 대화 내용을 계속 기억할 수 있습니다.

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# -----------------------------------------
# 6. 이전 대화 화면에 표시
# -----------------------------------------

for message in st.session_state.chat_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------------------
# 7. 채팅 입력창
# -----------------------------------------

user_message = st.chat_input("메시지를 입력하세요...")


# -----------------------------------------
# 8. 사용자가 메시지를 보냈을 때
# -----------------------------------------

if user_message:

    # 사용자의 메시지를 화면에 표시
    with st.chat_message("user"):
        st.markdown(user_message)

    # 대화 기록에 사용자 메시지 저장
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # -------------------------------------
    # 9. AI에게 보낼 전체 대화 만들기
    # -------------------------------------
    # 시스템 성격 + 지금까지의 모든 대화를 함께 보냅니다.
    # 따라서 AI가 앞의 대화를 참고해서 이어서 답할 수 있습니다.

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    messages.extend(st.session_state.chat_messages)


    # -------------------------------------
    # 10. AI 답변 받기
    # -------------------------------------

    with st.chat_message("assistant"):

        answer_box = st.empty()
        full_answer = ""

        try:
            # stream=True를 사용하면 답변을 조금씩 받아올 수 있습니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages,
                stream=True
            )

            # 답변이 들어오는 대로 화면에 이어서 표시
            for chunk in response:

                if not chunk.choices:
                    continue

                text = chunk.choices[0].delta.content

                if text:
                    full_answer += text
                    answer_box.markdown(full_answer + "▌")

            # 답변이 끝나면 커서 표시 제거
            answer_box.markdown(full_answer)


        except Exception:
            # API 오류 내용을 그대로 보여주지 않고
            # 사용자에게 이해하기 쉬운 안내만 보여줍니다.

            full_answer = "잠시 문제가 생겼어요. 조금 후에 다시 질문해 주세요."
            answer_box.markdown(full_answer)


    # -------------------------------------
    # 11. AI 답변도 대화 기록에 저장
    # -------------------------------------
    # 다음 질문을 할 때 이전 답변까지 함께 전달됩니다.

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": full_answer
        }
    )
