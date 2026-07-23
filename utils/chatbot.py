"""
chatbot.py
"Ask NeoCare" — a retrieval-based assistant that answers questions using
ONLY the knowledge base built from this project's own notebook, dataset,
and app behavior (utils/knowledge_base.py). It runs fully offline with
TF-IDF + cosine similarity, so it can't hallucinate facts that aren't in
that knowledge base, and it never needs an API key.

If you want more natural, free-form phrasing instead of returning the
matched knowledge chunk verbatim, you can optionally wire in the
Anthropic API (see `answer_with_claude` below) by providing an API key —
this is entirely optional and the app works fully without it.
"""

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.knowledge_base import build_knowledge_base

MATCH_THRESHOLD = 0.15  # below this similarity, treat as "no good match"
MARGIN_THRESHOLD = 1.15  # top match must beat the runner-up by at least this ratio

SUGGESTED_QUESTIONS = [
    "What is NeoCare?",
    "How accurate is the model?",
    "Why was Random Forest chosen?",
    "How does the prediction work?",
    "Which features affect prediction?",
    "What dataset was used?",
    "What preprocessing was performed?",
    "What's a normal oxygen saturation for a newborn?",
    "What counts as a fever in a newborn?",
    "What is a normal heart rate?",
    "What is a normal body temperature?",
    "What should I do if my baby is flagged At Risk?",
    "How does the growth tracker work?",
    "What is newborn health monitoring?",
    "Can NeoCare replace a doctor?"
]


@st.cache_resource(show_spinner=False)
def _build_index():
    chunks = build_knowledge_base()
    # Repeat the topic + example question phrasings so they carry more
    # retrieval weight than the longer answer content (which uses more
    # varied wording that doesn't always match how people ask).
    corpus = [
        (c["topic"] + " ") * 2 + (c.get("questions", "") + " ") * 3 + c["content"]
        for c in chunks
    ]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    matrix = vectorizer.fit_transform(corpus)
    return chunks, vectorizer, matrix


def answer_question(query: str) -> dict:
    """Return the best-matching knowledge chunk for a free-text question."""
    chunks, vectorizer, matrix = _build_index()
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, matrix)[0]

    ranked = sims.argsort()[::-1]
    best_idx = ranked[0]
    best_score = float(sims[best_idx])
    second_score = float(sims[ranked[1]]) if len(ranked) > 1 else 0.0

    # Reject if the match is weak OR if it isn't clearly better than the
    # runner-up (a sign the question doesn't cleanly belong to any one topic)
    is_confident = best_score >= MATCH_THRESHOLD and (
        second_score < 1e-6 or best_score / second_score >= MARGIN_THRESHOLD
    )



    if not is_confident:
        return {
            "answer": (
                "I don't have a confident answer for that in what I've learned from "
                "this project's notebook, dataset, and app. Try asking about the "
                "model's accuracy, which features matter most, typical vital-sign "
                "ranges, newborn care basics, or what to do if a baby is flagged At "
                "Risk — or check the Care Guide page for broader guidance."
            ),
            "matched_topic": None,
            "confidence": best_score,
        }

    return {
        "answer": chunks[best_idx]["content"],
        "matched_topic": chunks[best_idx]["topic"],
        "confidence": best_score,
    }


