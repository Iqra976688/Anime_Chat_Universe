import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("❌ GROQ_API_KEY missing. Please set it in .env.")
    st.stop()

client = Groq(api_key=API_KEY)

# --- CHARACTER DATA ---
CHARACTERS = {
    "Naruto Uzumaki 🍜": {
        "prompt": "You are Naruto Uzumaki - energetic, inspirational, friendly. Speak boldly and never give up.",
        "image": "images/naruto.png",
        "accent": "#FFB6B6"
    },
    "Roronoa Zoro ⚔️": {
        "prompt": "You are Roronoa Zoro - serious, loyal, blunt. Keep replies short and stoic.",
        "image": "images/zoro.png",
        "accent": "#B6FFCE"
    },
    "Satoru Gojo 🕶️": {
        "prompt": "You are Satoru Gojo - confident, witty, slightly teasing. Use clever remarks.",
        "image": "images/gojo.png",
        "accent": "#C6D6FF"
    },
    "Monkey D. Luffy 🍖": {
        "prompt": "You are Monkey D. Luffy - cheerful, loves food, simple-minded. Talk about adventures and meat.",
        "image": "images/luffy.png",
        "accent": "#FFF1B6"
    },
    "Levi Ackerman ⚔️": {
        "prompt": "You are Levi Ackerman - calm, blunt, disciplined, but protective. Use short sentences.",
        "image": "images/levi.png",
        "accent": "#D6D6D6"
    }
}

# --- STYLING ---
st.set_page_config(page_title="Anime Chat Universe 🌸", page_icon="🎴", layout="centered")

page_bg = """
<style>
/* Background gradient with subtle motion */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #1b1b2f, #16213e, #1a1a2e);
    color: #EEE;
    animation: gradientMove 10s ease infinite alternate;
}
@keyframes gradientMove {
    from {background-position: left;}
    to {background-position: right;}
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(30, 30, 45, 0.7);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
[data-testid="stSidebar"] img {
    border-radius: 20px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.15);
}

/* Titles & text */
h1, h2, h3, p, div {
    font-family: 'Poppins', sans-serif;
}

/* Chat bubble animations */
.chat-bubble {
    border-radius: 16px;
    padding: 12px 16px;
    margin: 10px 0;
    line-height: 1.5;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    animation: fadeIn 0.6s ease;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* User bubble */
.chat-bubble-user {
    background: linear-gradient(135deg, #22577E, #5584AC);
    color: #EFFFFA;
    margin-left: auto;
    width: fit-content;
    max-width: 80%;
}

/* Bot bubble */
.chat-bubble-bot {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #E3E3E3;
    backdrop-filter: blur(8px);
    width: fit-content;
    max-width: 80%;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #48CFCB);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 8px 20px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.25);
    font-weight: bold;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #48CFCB, #6C63FF);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align:center; color:#FFD1DC;'>🌸 Anime Chat Universe 🎴</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#CFCFCF;'>Relax, chat, and vibe with your favorite anime characters 🌙</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
selected_character = st.sidebar.selectbox("🎭 Choose a Character", list(CHARACTERS.keys()))
char_data = CHARACTERS[selected_character]
st.sidebar.image(char_data["image"], use_column_width=True)
st.sidebar.markdown(
    f"<div style='text-align:center; color:{char_data['accent']}; font-size:16px; font-weight:bold;'>{selected_character}</div>",
    unsafe_allow_html=True
)

# --- CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- INPUT AREA ---
col1, col2, col3 = st.columns([7, 1.5, 1.5])
with col1:
    user_input = st.text_input("💬 Type here...", key="input_box", placeholder="Say something cozy...")
with col2:
    send = st.button("✨ Send")
with col3:
    reset = st.button("🧹 Reset")

# --- SEND LOGIC ---
if send and user_input.strip():
    st.session_state.chat_history.append(("You", user_input))
    personality = CHARACTERS[selected_character]["prompt"]

    messages = [{"role": "system", "content": personality}]
    for sender, msg in st.session_state.chat_history[-20:]:
        role = "user" if sender == "You" else "assistant"
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": user_input})

    with st.spinner(f"{selected_character.split()[0]} is typing..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"[Error: {e}]"

    st.session_state.chat_history.append((selected_character, reply))
    st.rerun()

# --- RESET BUTTON ---
if reset:
    st.session_state.chat_history = []
    st.rerun()

# --- DISPLAY CHAT ---
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"<div class='chat-bubble chat-bubble-user'><b>{speaker}:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble chat-bubble-bot'><b>{speaker}:</b> {msg}</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<hr><p style='text-align:center; color:gray;'>Made with 💫 cozy vibes & Streamlit + Groq</p>", unsafe_allow_html=True)
