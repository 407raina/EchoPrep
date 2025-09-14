import requests
import io
import os
import tempfile
from gtts import gTTS
import streamlit as st
import base64
import json
import speech_recognition as sr
from audiorecorder import audiorecorder

# Hugging Face API configuration
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HF_STT_MODEL = "openai/whisper-base"

def text_to_speech(text: str) -> bytes:
    """Convert text to speech using gTTS (Google Text-to-Speech)"""
    try:
        # Use gTTS as it's free and reliable
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            
            # Read the audio data
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.unlink(tmp_file.name)
            
            return audio_data
            
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

def create_audio_player(audio_data: bytes, autoplay: bool = False) -> str:
    """Create HTML audio player for Streamlit"""
    if not audio_data:
        return ""
    
    # Encode audio data to base64
    audio_base64 = base64.b64encode(audio_data).decode()
    
    # Create HTML audio element
    autoplay_attr = "autoplay" if autoplay else ""
    
    audio_html = f"""
    <div class="audio-player">
        <audio controls {autoplay_attr} style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    </div>
    """
    
    return audio_html

def get_audio_recorder():
    """Get audio recorder widget with better UI"""
    from streamlit_audiorecorder import audiorecorder
    
    st.markdown("### 🎤 Voice Response")
    st.markdown("Click the record button below to record your answer:")
    
    # Use the audiorecorder component
    audio = audiorecorder("🎤 Start Recording", "⏹️ Stop Recording")
    
    return audio

def speech_to_text_local(audio_data) -> str:
    """Convert speech to text using local speech recognition"""
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        
        # If audio_data is from audiorecorder, save it to a temporary file
        if hasattr(audio_data, 'export'):
            # Export audio to wav format
            audio_data.export("temp_audio.wav", format="wav")
            
            # Use speech recognition on the file
            with sr.AudioFile("temp_audio.wav") as source:
                audio = r.record(source)
                
            # Clean up temporary file
            os.remove("temp_audio.wav")
            
            # Recognize speech using Google Speech Recognition
            text = r.recognize_google(audio)
            return text
            
        else:
            return "Could not process audio. Please try again or type your response."
            
    except sr.UnknownValueError:
        return "Could not understand audio. Please try again or type your response."
    except sr.RequestError as e:
        return f"Could not request results; {e}. Please type your response."
    except Exception as e:
        st.error(f"Error in speech recognition: {e}")
        return "Error processing audio. Please type your response."

def speech_to_text_huggingface(audio_data: bytes) -> str:
    """Convert speech to text using Hugging Face Whisper API"""
    if not HUGGINGFACE_API_TOKEN:
        return "Speech-to-text requires Hugging Face API token. Please provide a response in the text box below."
    
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
        
        api_url = f"https://api-inference.huggingface.co/models/{HF_STT_MODEL}"
        
        response = requests.post(
            api_url,
            headers=headers,
            data=audio_data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', 'Could not transcribe audio')
        else:
            st.error(f"Hugging Face STT API error: {response.status_code}")
            return "Could not transcribe audio. Please type your response."
            
    except Exception as e:
        st.error(f"Error in speech-to-text: {e}")
        return "Error transcribing audio. Please type your response."

def play_audio_streamlit(audio_data: bytes, autoplay: bool = True):
    """Play audio in Streamlit using st.audio"""
    if audio_data:
        st.audio(audio_data, format='audio/mp3', autoplay=autoplay)

def get_microphone_input():
    """Get microphone input using streamlit-webrtc (placeholder implementation)"""
    # This is a placeholder for microphone input functionality
    # In a full implementation, you would use streamlit-webrtc or similar
    st.info("🎤 Microphone input feature requires additional WebRTC setup.")
    st.write("For now, please use the text input below to provide your response.")
    return None

def process_audio_file(uploaded_file) -> str:
    """Process uploaded audio file for speech-to-text"""
    if uploaded_file is not None:
        # Read the uploaded file
        audio_data = uploaded_file.read()
        
        # Convert to text using Hugging Face API
        return speech_to_text_huggingface(audio_data)
    
    return ""
