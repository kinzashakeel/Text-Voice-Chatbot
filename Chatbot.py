import google.generativeai as genai
import streamlit as st
from streamlit_chat import message
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import pydub
from io import BytesIO
import requests
from gtts import gTTS
import time
import os
import base64
import pyttsx3
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

GEMINI_API_KEY = 'AIzaSyAKIq-OXzVZC7lTYtnZMdDFqiHDQ_a3L3o'
genai.configure(api_key=GEMINI_API_KEY)

#Model Initiation

model= genai.GenerativeModel("gemini-1.5-flash")

def getResponse(user_input):
    response=model.generate_content(user_input)
    return response.text

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# Initialize recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    """Function to recognize speech from microphone input."""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Wait...")
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, I'm having trouble with the speech recognition service."

def speak_text(text):
    """Function to convert text to speech and play it."""
    tts = gTTS(text=text, lang='en')
    
    # Use a context manager to handle the temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        tts.save(temp_file.name)
        temp_file_path = temp_file.name  # Store the file path for later use
    
    # Play the audio file and then clean up
    st.audio(temp_file_path, format='audio/mp3')
    
    # Ensure the file is properly closed before deleting
    os.remove(temp_file_path)



def handle_text_input(user_input):
    
    st.session_state.text_input = ""
   
              
            # Generate chatbot response
    response = getResponse(user_input)
            
    print(response)
            # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})
            
    st.text_input = ""
    
        
            

def handle_voice_input():

    if st.button("Speak"):
        speech_text = recognize_speech()
        st.session_state.messages.append({"role": "user", "content": speech_text})
        response = getResponse(speech_text)
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Speak the response
        speak_text(response)

def main():
    """Main function to run the Streamlit app."""
    st.title("Text and Voice Chatbot using Gemini-1.5-flash & Streamlit")

    # Initialize session state for chat history and text input
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    


    # Handle text and voice input
    user_input = st.chat_input("Type your message:", key="text_input_field")
    if user_input:
        handle_text_input(user_input)
    handle_voice_input()
   
    # Display previous chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            st.text_input = ""


    

if __name__ == "__main__":
    main()
