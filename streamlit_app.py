import requests
import streamlit as st

from database import init_db, read_history, save_results

API_URL = "http://localhost:8000/analyze"

init_db()

st.title("Review Analyzer")

if "results" not in st.session_state:
    st.session_state.results = []

reviews_text = st.text_area("Enter reviews, one per line", height=200)

if st.button("Analyze"):
    reviews = [line.strip() for line in reviews_text.splitlines() if line.strip()]
    if not reviews:
        st.warning("Please enter at least one review.")
    else:
        results = []
        progress = st.progress(0, text="Analyzing reviews...")
        for i, review in enumerate(reviews, start=1):
            try:
                response = requests.post(API_URL, json={"text": review}, timeout=60)
                response.raise_for_status()
                results.append({"review": review, **response.json()})
            except requests.RequestException as e:
                st.error(f"Failed to analyze: {review}\n\n{e}")
            progress.progress(i / len(reviews), text=f"Analyzed {i} of {len(reviews)}")
        progress.empty()
        st.session_state.results = results

if st.session_state.results:
    st.subheader("Results")
    st.dataframe(st.session_state.results, width="stretch")

    if st.button("Save"):
        for result in st.session_state.results:
            save_results(result["review"], result["label"], result["theme"], result["score"])
        st.success(f"Saved {len(st.session_state.results)} results.")
        st.session_state.results = []

st.subheader("History")
history = read_history()
if history:
    st.dataframe(history, width="stretch")
else:
    st.info("No saved reviews yet.")
