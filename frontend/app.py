import streamlit as st
import requests

st.title("🤖 LLaMA 3.1 Chatbot")

BACKEND_URL = "http://backend:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    response = requests.post(
        BACKEND_URL,
        json={"messages": st.session_state.messages}
    )

    reply = response.json()["reply"]

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)
