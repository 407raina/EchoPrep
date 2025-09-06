import requests
import io
import os
import tempfile
from gtts import gTTS
import streamlit as st
import base64
import json

# Hugging Face API configuration
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HF_STT_MODEL = "openai/whisper-base"
HF_TTS_MODEL = "microsoft/speecht5_tts"

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
        print(f"Error in text-to-speech: {e}")
        return None

def text_to_speech_huggingface(text: str) -> bytes:
    """Convert text to speech using Hugging Face API (fallback option)"""
    if not HUGGINGFACE_API_TOKEN:
        return text_to_speech(text)  # Fallback to gTTS
    
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
        
        # Use a simpler TTS model
        api_url = f"https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
        
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": text}
        )
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"Hugging Face TTS API error: {response.status_code}")
            return text_to_speech(text)  # Fallback to gTTS
            
    except Exception as e:
        print(f"Error in Hugging Face TTS: {e}")
        return text_to_speech(text)  # Fallback to gTTS

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
            print(f"Hugging Face STT API error: {response.status_code}")
            return "Could not transcribe audio. Please type your response."
            
    except Exception as e:
        print(f"Error in speech-to-text: {e}")
        return "Error transcribing audio. Please type your response."

def create_audio_player(audio_data: bytes, autoplay: bool = False) -> str:
    """Create HTML audio player for Streamlit"""
    if not audio_data:
        return ""
    
    # Encode audio data to base64
    audio_base64 = base64.b64encode(audio_data).decode()
    
    # Create HTML audio element
    audio_html = f"""
    <audio {"autoplay" if autoplay else ""} controls style="width: 100%;">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    
    return audio_html

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
