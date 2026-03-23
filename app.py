import streamlit as st
import os
from google import genai
from utils.pdf_utils import extract_pdf_text

# -------- CONFIG --------
st.set_page_config(page_title="Nrn AI", layout="wide")

# -------- CUSTOM CSS (PREMIUM LOOK) --------
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #2b313e;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: right;
    color: white;
}
.chat-bubble-ai {
    background-color: #1e1e1e;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: left;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.title("👾 Nrn AI Assistant")
st.caption("Your Smart Study Partner 🚀")

# -------- GEMINI SETUP --------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key missing")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------- SESSION STATE --------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hi! I'm Nrn AI. Ask me anything or upload notes!"}
    ]

# -------- DISPLAY CHAT --------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

# -------- INPUT AREA --------
col1, col2 = st.columns([8,1])

with col1:
    user_input = st.text_input("Type your message...", label_visibility="collapsed")

with col2:
    send = st.button("➤")

# -------- PDF UPLOAD --------
uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

if uploaded_file:
    pdf_text = extract_pdf_text(uploaded_file)
    st.success("PDF uploaded!")

    if st.button("Summarize PDF"):
        user_input = f"Summarize this in simple way:\n{pdf_text[:2000]}"

# -------- AI FUNCTION --------
def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"You are a helpful study assistant. Reply clearly:\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"❌ {str(e)}"

# -------- HANDLE MESSAGE --------
if send and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        reply = get_ai_response(user_input)

    # Add AI message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()

# -------- FOOTER --------
st.markdown("---")
st.caption("⚡ Powered by Gemini | Developed by Naveen & Team 🚀")
