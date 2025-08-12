import streamlit as st
import random
import streamlit.components.v1 as components
import json

def speak_now(text: str):
    js_str = json.dumps(text)  # safe JS string literal
    components.html(f"""
        <script>
          (function() {{
            const text = {js_str};
            if (!text) return;
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            setTimeout(() => window.speechSynthesis.speak(u), 0);
          }})();
        </script>
    """, height=0)

def reset_game():
    st.session_state.first_number = 10
    st.session_state.second_number = random.randint(0, st.session_state.first_number - 1)
    st.session_state.user_number = ""
    st.session_state.result_to_speak = ""

def check_answer():
    user_input_val = int(st.session_state.user_number) if st.session_state.user_number.isdigit() else 0
    if user_input_val + st.session_state.second_number == st.session_state.first_number:
        st.toast("Correct!", icon="✅")
        st.session_state.result_to_speak = (
            f"{st.session_state.user_name}, Good Job! "
            f"{user_input_val} + {st.session_state.second_number} = {st.session_state.first_number}"
        )
    else:
        st.toast("Incorrect.", icon="❌")
        st.session_state.result_to_speak = f"{st.session_state.user_name}, Try again!"
        # Clear the box for the next round
        st.session_state.user_number = ""
    speak_now(st.session_state.result_to_speak)

st.set_page_config(page_title="Sum Checker", layout="centered")
st.title("Simple Sum Checker App")

# Styling for text areas
st.markdown("""
    <style>
    textarea {
        font-size: 48px !important;
        height: 100px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Init session state
if "first_number" not in st.session_state:
    st.session_state.first_number = 10
if "second_number" not in st.session_state:
    st.session_state.second_number = random.randint(0, st.session_state.first_number - 1)
if "result_to_speak" not in st.session_state:
    st.session_state.result_to_speak = ""
if "user_number" not in st.session_state:
    st.session_state.user_number = ""

name = st.text_area("Enter your name:", key="user_name", value="Bethany")

# First number display
st.markdown(
    f"<h1 style='text-align: center; color: blue; font-size:100px;'>{st.session_state.first_number}</h1>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"<h2 style='text-align: center; color: green; font-size:80px;'>{st.session_state.second_number}</h2>",
        unsafe_allow_html=True
    )
with col2:
    st.text_area("", key="user_number")

# Buttons with callbacks
st.button("Check Answer", on_click=check_answer)
st.button("Try again", on_click=reset_game)
