import streamlit as st
import os
import time
from google import genai
from utils.pdf_utils import extract_pdf_text

# -------- CONFIG --------
st.set_page_config(page_title="Gen AI", layout="wide")

# -------- GEMINI --------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key missing")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------- SESSION --------
if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}
    st.session_state.current_chat = "New Chat"

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("## 👾Gen AI")

    if st.button("✨ New Chat"):
        name = f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name

    st.markdown("### 💬 Chats")
    for chat in st.session_state.chats:
        if st.button(chat):
            st.session_state.current_chat = chat

# -------- CURRENT CHAT --------
messages = st.session_state.chats[st.session_state.current_chat]

# -------- INSANE CSS --------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0f0f, #1a1a2e);
    color: white;
}

/* Chat container */
.chat-container {
    max-height: 75vh;
    overflow-y: auto;
    padding-bottom: 100px;
}

/* Glass effect */
.user {
    background: rgba(43, 49, 62, 0.7);
    backdrop-filter: blur(10px);
    padding: 12px;
    border-radius: 15px;
    margin: 6px;
    text-align: right;
}
.ai {
    background: rgba(30, 30, 30, 0.7);
    backdrop-filter: blur(10px);
    padding: 12px;
    border-radius: 15px;
    margin: 6px;
    text-align: left;
}

/* Input bar */
.input-container {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: rgba(15,15,15,0.8);
    backdrop-filter: blur(15px);
    padding: 10px;
}

/* Buttons */
.stButton button {
    border-radius: 50%;
    height: 45px;
    width: 45px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("# 👾 Gen AI")
st.caption("Students AI Assistant 🚀")

# -------- CHAT DISPLAY --------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not messages:
    st.markdown("<div class='ai'>👋 Welcome! Ask anything, upload files, or explore AI 🚀</div>", unsafe_allow_html=True)

for msg in messages:
    role_class = "user" if msg["role"] == "user" else "ai"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------- INPUT AREA --------
col1, col2, col3 = st.columns([7,1,1])

with col1:
    user_input = st.text_input("Type a message...", label_visibility="collapsed")

with col2:
    upload = st.file_uploader("➕", type=["pdf","txt"], label_visibility="collapsed")

with col3:
    send = st.button("➤")

# -------- AI FUNCTION --------
def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"You are a smart study assistant:\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"❌ {str(e)}"

# -------- HANDLE MESSAGE --------
if send and user_input:
    messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        reply = get_ai_response(user_input)

        # Typing animation
        temp = ""
        placeholder = st.empty()
        for char in reply:
            temp += char
            placeholder.markdown(f"<div class='ai'>{temp}</div>", unsafe_allow_html=True)
            time.sleep(0.01)

    messages.append({"role": "assistant", "content": reply})
    st.rerun()

# -------- HANDLE FILE --------
if upload:
    text = extract_pdf_text(upload)
    messages.append({"role": "user", "content": "📄 Uploaded file"})

    with st.spinner("Analyzing file..."):
        reply = get_ai_response(f"Summarize:\n{text[:2000]}")

    messages.append({"role": "assistant", "content": reply})
    st.rerun()

# -------- FOOTER --------
st.markdown("---")
st.caption("⚡ Gen AI | Built by Gen Z Coders 🚀")
