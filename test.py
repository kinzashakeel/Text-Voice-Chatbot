import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import tempfile
import google.generativeai as genai
import openai
load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

#Model Initiation

model= genai.GenerativeModel("gemini-1.5-flash")

def getResponse(user_input):
    response=model.generate_content(user_input)
    return response.text


def main():


    st.title("🎤 :blue[Urdu Voice Chatbot] 💬🤖")
    st.subheader('اپنی آواز ریکارڈ کریں اور "اے آئی وائس باٹ" سے جواب حاصل کریں', divider='rainbow')

    urdu_recorder = audio_recorder(text='بولیۓ', icon_size="2x", icon_name="microphone-lines", key="urdu_recorder")

    if urdu_recorder is not None:
        
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                # Display the audio file
                st.header('🧑')                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                st.audio(urdu_recorder)

                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_urdu_recording:
                    temp_urdu_recording.write(urdu_recorder)
                    temp_urdu_recording_path = temp_urdu_recording.name
                
                # Convert audio file to text
                
                text = Urdu_audio_to_text(temp_urdu_recording_path)
                st.success( text)

                # Remove the temporary file
                os.remove(temp_urdu_recording_path)


        response_text = llmModelResponse(text)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Convert the response text to speech
                response_audio_html = response_to_urdu_audio(response_text)

                st.header('🤖')
                st.markdown(response_audio_html, unsafe_allow_html=True)

                st.info(response_text)


def Urdu_audio_to_text(temp_urdu_recording_path):
    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_urdu_recording_path) as source:
        urdu_recoded_voice = recognizer.record(source)
        try:
            text = recognizer.recognize_google(urdu_recoded_voice, language="ur")
            return text
        except sr.UnknownValueError:
            return "آپ کی آواز واضح نہیں ہے"
        except sr.RequestError:
            return "Sorry, my speech service is down"

def response_to_urdu_audio(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    tts_audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    tts.save(tts_audio_path)

    # Get the base64 string of the audio file
    audio_base64 = get_audio_base64(tts_audio_path)

    # Autoplay audio using HTML and JavaScript
    audio_html = f"""
    <audio controls autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html

# Function to encode the audio file to base64
def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return base64.b64encode(audio_bytes).decode()


if __name__ == "__main__":
    main()
