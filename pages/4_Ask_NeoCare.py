import time

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

USER_AVATAR = "🧑"
BOT_AVATAR = "🩺"

# ---- floating bot bubble anchored to the chat input, Snapchat-style ----
st.markdown(
    """
    <style>
    .neocare-bot-bubble {
        position: fixed;
        bottom: 78px;
        left: 24px;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.25);
        z-index: 9999;
        animation: neocare-bob 2.4s ease-in-out infinite;
    }
    @keyframes neocare-bob {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    /* push chat input text so it doesn't sit under the bubble */
    [data-testid="stChatInput"] textarea {
        padding-left: 44px !important;
    }
    </style>
    <div class="neocare-bot-bubble">🩺</div>
    """,
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.toast("NeoCare assistant is ready", icon="🩺")

st.markdown("#### Try asking:")
cols = st.columns(3)
for i, q in enumerate(SUGGESTED_QUESTIONS):
    if cols[i % 3].button(q, use_container_width=True, key=f"suggest_{i}"):
        st.session_state.pending_question = q

st.write("")

# render past messages with role-based avatars
for msg in st.session_state.chat_history:
    avatar = BOT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about the model, your baby's vitals, or newborn care...")
pending = st.session_state.pop("pending_question", None)
query = user_input or pending

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(query)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("NeoCare is reviewing..."):
            result = answer_question(query)
            answer = result["answer"]

        # typed-out reveal, doctor-consult style
        placeholder = st.empty()
        typed = ""
        for word in answer.split(" "):
            typed += word + " "
            placeholder.markdown(typed + "▌")
            time.sleep(0.02)
        placeholder.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # small celebratory flourish for risk/score related answers
    if any(word in query.lower() for word in ["risk", "score", "predict"]):
        st.balloons()

if st.session_state.chat_history:
    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

footer()