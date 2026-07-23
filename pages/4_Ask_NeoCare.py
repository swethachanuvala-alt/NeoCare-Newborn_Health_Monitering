import streamlit as st

from utils.styles import inject_css, hero, footer
from utils.chatbot import answer_question, SUGGESTED_QUESTIONS

st.set_page_config(page_title="NeoCare · Ask NeoCare", page_icon="💬", layout="wide")
inject_css()

hero(
    "💬 Ask NeoCare",
    "Questions answered from this project's own notebook, dataset, and app — not a generic bot.",
)

with st.sidebar:
    st.markdown("### About this assistant")
    st.write(
        "This chatbot only answers from a knowledge base built out of NeoCare's "
        "own training data, trained model stats, and care guidance — it won't "
        "make things up outside of that."
    )
    

st.warning(
    "⚕️ This assistant shares general information only — it doesn't diagnose. "
    "For anything urgent, see the Care Guide page or contact a pediatrician."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("#### Try asking:")
cols = st.columns(3)
for i, q in enumerate(SUGGESTED_QUESTIONS):
    if cols[i % 3].button(q, use_container_width=True, key=f"suggest_{i}"):
        st.session_state.pending_question = q

st.write("")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about the model, your baby's vitals, or newborn care...")
pending = st.session_state.pop("pending_question", None)
query = user_input or pending

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
        
                result = answer_question(query)
                answer = result["answer"]
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})

if st.session_state.chat_history:
    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

footer()