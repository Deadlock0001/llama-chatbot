import streamlit as st
import requests
import time
import uuid

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="CHAT-BOT",
    page_icon="💬",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.current_chat = new_id

# ---------------- CUSTOM CSS (UNCHANGED UI) ---------------- #
st.markdown("""
<style>
.stApp { background-color: #212121; }

section[data-testid="stSidebar"] {
    width: 320px !important;
    background-color: #171717;
}

.block-container {
    padding-top: 25px;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100% !important;
}

h1 {
    margin-left: 0.5rem;
    font-weight: 600;
    color: white;
}

[data-testid="stChatMessage"] {
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 12px;
    font-size: 15px;
}

[data-testid="stChatMessage"][aria-label="user message"] {
    background-color: #2b2b2b;
    color: white;
}

[data-testid="stChatMessage"][aria-label="assistant message"] {
    background-color: #303030;
    color: #e5e5e5;
}

.typing span {
  animation: blink 1.4s infinite both;
  font-size: 22px;
}
.typing span:nth-child(2) { animation-delay: .2s; }
.typing span:nth-child(3) { animation-delay: .4s; }

@keyframes blink {
  0% { opacity: .2; }
  20% { opacity: 1; }
  100% { opacity: .2; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- BACKEND ---------------- #
BACKEND_URL = "http://localhost:9001/vllmchat"
MODELS_URL = "http://localhost:9001/models"

try:
    models_response = requests.get(MODELS_URL)
    available_models = models_response.json().get("models", [])
except:
    available_models = ["No models available"]

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.current_chat = new_id

    st.divider()

    for chat_id, chat_data in list(st.session_state.chats.items()):
        col1, col2 = st.columns([4,1])

        with col1:
            if st.button(chat_data["title"], key=f"select_{chat_id}"):
                st.session_state.current_chat = chat_id

        with col2:
            if st.button("🗑", key=f"delete_{chat_id}"):
                del st.session_state.chats[chat_id]

                if st.session_state.current_chat == chat_id:
                    if st.session_state.chats:
                        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                    else:
                        new_id = str(uuid.uuid4())
                        st.session_state.chats[new_id] = {
                            "title": "New Chat",
                            "messages": []
                        }
                        st.session_state.current_chat = new_id

                st.rerun()

    st.divider()
    st.subheader("⚙ Model")
    model = st.selectbox("Select Model", available_models)

# ---------------- CURRENT CHAT ---------------- #
current_chat = st.session_state.chats[st.session_state.current_chat]
messages = current_chat["messages"]

# ---------------- HEADER ---------------- #
st.title("CHAT-BOT")

# ---------------- DISPLAY CHAT (STABLE CONTAINER) ---------------- #
chat_container = st.container()

with chat_container:
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- INPUT ---------------- #
user_input = st.chat_input("Message CHAT-BOT...")

if user_input:

    # Append user immediately
    messages.append({"role": "user", "content": user_input})

    if current_chat["title"] == "New Chat":
        current_chat["title"] = user_input[:30] + ("..." if len(user_input) > 30 else "")

    with st.chat_message("user"):
        st.markdown(user_input)

    # Create assistant container instantly (prevents fade gap)
    assistant_container = st.chat_message("assistant")
    placeholder = assistant_container.empty()

    placeholder.markdown("""
    <div class="typing">
        <span>.</span><span>.</span><span>.</span>
    </div>
    """, unsafe_allow_html=True)

    # Backend call
    try:
        response = requests.post(
            BACKEND_URL,
            json={
                "model": model,
                "messages": messages,
            },
            timeout=120,
        )

        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "No reply received.")
        else:
            reply = f"Backend error: {response.status_code}"

    except Exception as e:
        reply = f"Frontend Error: {str(e)}"

    # Smooth typewriter without layout shift
    full_text = ""
    for char in reply:
        full_text += char
        placeholder.markdown(full_text + "▌")
        time.sleep(0.006)

    placeholder.markdown(full_text)

    messages.append({"role": "assistant", "content": reply})
