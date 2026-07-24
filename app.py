import os

import streamlit as st
from openai import OpenAI


MODEL = "gpt-4o-mini"


def get_api_key() -> str | None:
    """Read the key from Streamlit secrets first, then local environment."""
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def build_client() -> OpenAI | None:
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


st.set_page_config(page_title="OpenAI 챗봇", page_icon="💬")

st.title("OpenAI 챗봇")
st.caption(f"사용 모델: {MODEL}")

with st.sidebar:
    st.header("설정")
    system_prompt = st.text_area(
        "시스템 메시지",
        value="너는 친절하고 명확하게 답변하는 한국어 AI assistant야.",
        height=120,
    )

    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        "Streamlit Community Cloud의 **Settings > Secrets**에 "
        "`OPENAI_API_KEY`를 등록해서 사용하세요."
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    client = build_client()

    if client is None:
        with st.chat_message("assistant"):
            st.error("OPENAI_API_KEY가 설정되어 있지 않습니다.")
        st.stop()

    messages_for_api = [{"role": "system", "content": system_prompt}]
    messages_for_api.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages_for_api,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as exc:
            full_response = f"오류가 발생했습니다: {exc}"
            st.error(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
