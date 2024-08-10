import google.generativeai as genai
import streamlit as st
from streamlit_chat import message
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np

from io import BytesIO
import requests
from gtts import gTTS
import time
import base64
import pyttsx3
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

#Model Initiation

model= genai.GenerativeModel("gemini-1.5-flash")

def getResponse(user_input):
    response=model.generate_content(user_input)
    return response.text

import tempfile


def recognize_speech(temp_urdu_recording_path):
    
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(temp_urdu_recording_path) as source:
                        urdu_recoded_voice = recognizer.record(source)
                        try:
                            text = recognizer.recognize_google(urdu_recoded_voice, language="en")
                            return text
                        except sr.UnknownValueError:
                            return "آپ کی آواز واضح نہیں ہے"
                        except sr.RequestError:
                            return "Sorry, my speech service is down"
                        '''
    # Initialize recognizer
    recognizer = sr.Recognizer()

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
        '''
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
    
        
            

def handle_voice_input(speech_text):

    #if st.button("Speak"):
    #   speech_text = recognize_speech()
        print(speech_text)
        
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
    

    recorder = audio_recorder(text='بولیۓ', icon_size="2x", icon_name="microphone-lines", key="recorder")
    # Handle text and voice input
    user_input = st.chat_input("Type your message:", key="text_input_field")
    if user_input:
        handle_text_input(user_input)
    elif recorder is not None:
            
            with st.container():
                col1, col2 = st.columns(2)

                with col2:
                    # Display the audio file
                    st.header('🧑')                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                    st.audio(recorder)

                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_urdu_recording:
                        temp_urdu_recording.write(recorder)
                        temp_urdu_recording_path = temp_urdu_recording.name
                    
                    # Convert audio file to text
                    
                    #text = Urdu_audio_to_text(temp_urdu_recording_path)
                    #st.success( text)
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(temp_urdu_recording_path) as source:
                        urdu_recoded_voice = recognizer.record(source)
                        try:
                            speech_text = recognizer.recognize_google(urdu_recoded_voice, language="en")
                        except sr.UnknownValueError:
                            return "آپ کی آواز واضح نہیں ہے"
                        except sr.RequestError:
                            return "Sorry, my speech service is down"
                    
                    # Remove the temporary file
                    os.remove(temp_urdu_recording_path)
                    #speech_text= recognize_speech(temp_urdu_recording_path)
                    handle_voice_input(speech_text)
   
    # Display previous chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            st.text_input = ""

if __name__ == "__main__":
    main()
    

