import streamlit as st
import os
import requests
from utils.pdf_utils import extract_pdf_text

st.set_page_config(page_title="Nrn AI", layout="wide")

st.title("👾 Nrn AI Study Assistant")

# -------- HUGGING FACE SETUP --------
API_URL = "https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_ai_response(prompt):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7
            },
            "options": {
                "wait_for_model": True
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        # DEBUG (optional)
        # st.write(response.text)

        if response.status_code != 200:
            return f"API Error: {response.text}"

        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "No response")

        elif isinstance(result, dict):
            if "error" in result:
                return f"Error: {result['error']}"
            return str(result)

        return "No valid response"

    except Exception as e:
        return f"Error: {str(e)}"

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
        quiz_prompt = f"Create 5 quiz questions with answers:\n{user_input}"
        quiz_output = get_ai_response(quiz_prompt)
        st.subheader("🧠 Quiz")
        st.write(quiz_output)

# -------- FOOTER --------
st.markdown("---")
st.caption("Developed By Naveen & Team🚀")
