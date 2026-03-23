import streamlit as st
import os
from google import genai
from utils.pdf_utils import extract_pdf_text

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Nrn AI", layout="wide")
st.title("👾 Nrn AI Study Assistant")

# -------- GEMINI SETUP --------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Add it in Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------- AI FUNCTION --------
def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",  # ✅ FIXED
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"
        
# -------- INPUT SECTION --------
user_input = st.text_area("📚 Ask your question or paste notes:")

uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

if uploaded_file:
    pdf_text = extract_pdf_text(uploaded_file)
    st.success("PDF Loaded!")

    if st.button("📄 Summarize PDF"):
        user_input = f"Summarize this in simple points:\n{pdf_text[:2000]}"

# -------- BUTTONS --------
col1, col2 = st.columns(2)

with col1:
    generate = st.button("🤖 Generate Answer")

with col2:
    quiz = st.button("🧠 Generate Quiz")

# -------- OUTPUT --------
if generate and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
        st.subheader("📖 Answer")
        st.write(answer)

if quiz and user_input:
    with st.spinner("Generating quiz..."):
        quiz_prompt = f"""
        Create 5 quiz questions with answers from this topic:
        {user_input}
        """
        quiz_output = get_ai_response(quiz_prompt)
        st.subheader("🧠 Quiz")
        st.write(quiz_output)

# -------- FOOTER --------
st.markdown("---")
st.caption("Developed By Naveen & Team 🚀")
