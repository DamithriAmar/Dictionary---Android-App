# app.py
import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import random

# --- Load CSV ---
@st.cache_data
def load_data():
    df = pd.read_csv("dictionary.csv")
    return df.dropna()

df = load_data()

# --- Streamlit page config ---
st.set_page_config(page_title="✨ Cute Word Finder ✨", page_icon="💖", layout="wide")

# --- Playful sky-blue gradient background ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# --- Sparkling purplish sidebar for options ---
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #a18cd1, #fbc2eb);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 2px 2px 8px rgba(131, 58, 180, 0.3);
}
/* Sidebar text color */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Options + Random Word ---
st.sidebar.header("⚙️ Options")

# Friendly language names
source_lang = st.sidebar.selectbox(
    "From",
    ["word", "translation"],
    format_func=lambda x: "English" if x == "word" else "Korean"
)
target_lang = st.sidebar.selectbox(
    "To",
    ["translation", "word"],
    format_func=lambda x: "Korean" if x == "translation" else "English"
)

# Fuzzy search always enabled
use_fuzzy = True

# Random Word of the Day
if "word_of_day" not in st.session_state or st.session_state.get("word_of_day_dir") != (source_lang, target_lang):
    random_word = df.sample(1).iloc[0]
    st.session_state.word_of_day = random_word
    st.session_state.word_of_day_dir = (source_lang, target_lang)

st.sidebar.markdown("### 🌸 Word of the Day")
st.sidebar.markdown(f"""
<div style="
    border:2px solid #ff69b4; 
    border-radius:15px; 
    padding:10px; 
    margin-bottom:10px; 
    background:#fff0f5;
    box-shadow: 2px 2px 6px rgba(255,105,180,0.2);
">
    <span style='font-weight:bold; font-size:1.2em; color:#ff1493;'>{st.session_state.word_of_day[source_lang]}</span><br>
    <span style='color:#ff69b4;'>{st.session_state.word_of_day[target_lang]}</span>
</div>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>✨💖 Cute Word Finder 💖✨</h1>", unsafe_allow_html=True)

# --- Layout with two columns ---
left, right = st.columns([1, 2])

# --- LEFT: Cute Search Bar + Selected word ---
with left:
    query = st.text_input("", placeholder="💖 Type a word...", key="query_input")

    st.markdown("""
    <style>
    div.stTextInput>div>input {
        height: 45px;
        font-size: 1.2em;
        border-radius: 15px;
        border: 2px solid #ff69b4;
        padding: 10px;
        box-shadow: 2px 2px 6px rgba(255,105,180,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    selected_word = st.session_state.get("selected_word", None)
    selected_translation = st.session_state.get("selected_translation", None)

    if query:
        # Show translation instantly if exact match
        exact_match = df[df[source_lang].str.lower() == query.lower()]
        if not exact_match.empty:
            st.session_state.selected_word = exact_match.iloc[0][source_lang]
            st.session_state.selected_translation = exact_match.iloc[0][target_lang]
            selected_word = st.session_state.selected_word
            selected_translation = st.session_state.selected_translation

    if selected_word:
        st.markdown(f"""
        <div style="
            margin-top:20px; 
            font-size:1.4em; 
            font-weight:bold; 
            border:2px solid #ff69b4; 
            border-radius:15px; 
            padding:15px; 
            background:#fff0f5;
            box-shadow: 2px 2px 6px rgba(255,105,180,0.2);
        ">
            💖✨ You picked:<br>
            <span style="color:#ff69b4; font-size:1.6em;">{selected_word}</span> 🌸<br>
            <span style="font-size:1.2em; color:#ff1493;">Translation: {selected_translation}</span>
        </div>
        """, unsafe_allow_html=True)

# --- RIGHT: Suggestions (clean cards, no buttons) ---
with right:
    st.subheader("✨ Suggestions")
    results = pd.DataFrame()

    if query:
        matches = process.extract(query, df[source_lang].tolist(), limit=10)
        matched_words = [m[0] for m in matches if m[1] > 60]
        results = df[df[source_lang].isin(matched_words)]

    if not results.empty:
        for i, row in results.iterrows():
            word = row[source_lang]
            translations = [t.strip() for t in row[target_lang].split(",")]
            translations_html = "<br>".join([f"🌸 {t}" for t in translations])

            st.markdown(f"""
            <div style="
                border:2px solid #ff69b4; 
                border-radius:15px; 
                padding:10px; 
                margin-bottom:10px; 
                background:#fff0f5;
                box-shadow: 2px 2px 6px rgba(255,105,180,0.2);
            ">
                <span style="font-weight:bold; color:#ff1493;">{word}</span><br>
                <span style="font-size:0.9em; color:#ff69b4;">{translations_html}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        if query:
            st.markdown("<p style='color:#999;'>No matches found 💔</p>", unsafe_allow_html=True)
