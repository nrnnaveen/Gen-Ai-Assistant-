import streamlit as st
import os
from openai import OpenAI
from utils.pdf_utils import extract_pdf_text
from utils.voice_utils import record_voice

# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title=" Nrn AI ", layout="wide")

st.title("👾 Nrn AI Assistant")

# -------- INPUT SECTION --------
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_area("📚 Ask your question:")

    if st.button("🎤 Speak"):
        voice_text = record_voice()
        if voice_text:
            st.success(f"You said: {voice_text}")
            user_input = voice_text

with col2:
    uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

    if uploaded_file:
        pdf_text = extract_pdf_text(uploaded_file)
        st.success("PDF Loaded!")

        if st.button("📄 Summarize PDF"):
            user_input = f"Summarize this in simple points:\n{pdf_text[:3000]}"

# -------- ACTION BUTTONS --------
col3, col4 = st.columns(2)

with col3:
    generate = st.button("🤖 Generate Answer")

with col4:
    quiz = st.button("🧠 Generate Quiz")

# -------- AI RESPONSE --------
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant. Explain in simple and clear way."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if generate and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
        st.subheader("📖 Answer")
        st.write(answer)

if quiz and user_input:
    with st.spinner("Generating quiz..."):
        quiz_prompt = f"Create 5 quiz questions with answers from this topic:\n{user_input}"
        quiz_output = get_ai_response(quiz_prompt)
        st.subheader("🧠 Quiz")
        st.write(quiz_output)

# -------- FOOTER --------
st.markdown("---")
st.caption("Built with ❤️ for AI Expo")
