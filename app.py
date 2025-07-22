import streamlit as st
from utils.pdf_reader import extract_quran_text
from utils.rag_chain import build_rag_chain
from utils.voice import speak_text
from utils.history import save_to_history, get_history
import os

# ---------- Config & Style ----------
st.set_page_config(page_title="📖 Quran RAG Chatbot", page_icon="🕌")

# Inject custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f8;
        }
        .stTextInput>div>div>input {
            border: 2px solid #00897b;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #00897b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
        .question-box {
            background-color: #e0f2f1;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .answer-box {
            background-color: #ffffff;
            border-left: 5px solid #00897b;
            padding: 15px;
            border-radius: 10px;
        }
        .history-title {
            margin-top: 30px;
            font-size: 20px;
            color: #00897b;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 style='text-align: center;'>📖 Quran AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Ask any question related to the Holy Quran</p>", unsafe_allow_html=True)

# ---------- Load Model ----------
if "qa_chain" not in st.session_state:
    if not os.path.exists("Quran-English.pdf"):
        st.error("❌ Please add 'Quran-English.pdf' in the root folder.")
    else:
        with st.spinner("Loading Quran into memory..."):
            quran_text = extract_quran_text("Quran-English.pdf")
            st.session_state.qa_chain = build_rag_chain(quran_text)

# ---------- Input Box ----------
question = st.text_input("💬 Ask your question:")

if st.button("🔍 Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = st.session_state.qa_chain.run(question)
            speak_text(answer)
            save_to_history(question, answer)

            # Show Answer
            st.markdown("<div class='question-box'><b>Q:</b> " + question + "</div>", unsafe_allow_html=True)
            st.markdown("<div class='answer-box'><b>A:</b> " + answer + "</div>", unsafe_allow_html=True)

# ---------- Show History ----------
st.markdown("<div class='history-title'>🕑 Previous Questions</div>", unsafe_allow_html=True)
for q, a in get_history():
    st.markdown(f"<div class='question-box'><b>Q:</b> {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='answer-box'><b>A:</b> {a}</div>", unsafe_allow_html=True)
