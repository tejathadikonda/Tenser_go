import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import speech_recognition as sr
from gtts import gTTS
import tempfile

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="😼",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🎙️ Gemini Pro - Voice ChatBot")

# Function to recognize speech from the microphone
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            user_prompt = r.recognize_google(audio)
            st.write(f"You said: {user_prompt}")
            return user_prompt
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.write("Could not request results from the recognition service.")
            return None

# Function to convert text to speech and play it using Streamlit's st.audio
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    try:
        tts.save(temp_file.name)
        st.audio(temp_file.name, format='audio/mp3')
    finally:
        temp_file.close()  # Ensure the file is closed before deleting
        os.remove(temp_file.name)

# Button to start speech recognition
if st.button("Speak"):
    user_prompt = recognize_speech()
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response and play it
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
        speak_text(gemini_response.text)

# Add an "About Me" button
st.markdown(
    """
    <div style="text-align: right;">
        <a href="https://tejathadikonda.github.io/portfolio/#" target="_blank">
            <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;">
                About Me
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
