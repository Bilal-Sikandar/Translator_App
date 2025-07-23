import streamlit as st
from translate import Translator
from gtts import gTTS
import base64
import os
from PIL import Image
import io

# ---------- CONFIG ----------
st.set_page_config(
    page_title="BoltTranslate",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Create custom CSS file if it doesn't exist
if not os.path.exists("styles.css"):
    with open("styles.css", "w") as f:
        f.write("""
        /* Base styles */
        body {
            font-family: 'Times New Roman', serif;
            font-weight: 500;
        }
        
        /* Light mode */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to right, #424242 80%, #008B8B 20%);
            background-attachment: fixed;
        }
        
        .main .block-container {
            background-color: rgba(50, 50, 50, 0.92);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            padding: 2rem;
            position: relative;
            overflow: hidden;
            color: white;
        }
        
        .main .block-container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><path d="M30,10 L40,50 L20,60 L70,10 L60,50 L80,40 Z" fill="none" stroke="%23008B8B" stroke-width="0.5" opacity="0.1"/></svg>');
            background-size: 200px;
            opacity: 0.3;
            z-index: -1;
        }
        
        /* Dark mode */
        .dark [data-testid="stAppViewContainer"] {
            background: linear-gradient(to right, #212121 80%, #006064 20%);
        }
        
        .dark .main .block-container {
            background-color: rgba(30, 30, 30, 0.95);
        }
        
        .dark .main .block-container::before {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><path d="M30,10 L40,50 L20,60 L70,10 L60,50 L80,40 Z" fill="none" stroke="%2300CED1" stroke-width="0.5" opacity="0.1"/></svg>');
        }
        
        /* Text styles */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Times New Roman', serif;
            font-weight: 600;
            color: #00CED1 !important;
        }
        
        .dark h1, .dark h2, .dark h3, .dark h4, .dark h5, .dark h6 {
            color: #00FFFF !important;
        }
        
        /* Button styles */
        .stButton>button {
            font-family: 'Times New Roman', serif;
            font-weight: 600;
            border-radius: 6px !important;
            animation: wobble 2s infinite;
        }
        
        .stButton>button[kind="primary"] {
            background-color: #008B8B !important;
            color: white !important;
            border: none;
        }
        
        .dark .stButton>button[kind="primary"] {
            background-color: #00CED1 !important;
            color: #121212 !important;
        }
        
        @keyframes wobble {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(1deg); }
            50% { transform: rotate(-1deg); }
            75% { transform: rotate(1deg); }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            font-size: 0.9em;
            margin-top: 40px;
            color: #AAAAAA;
        }
        
        .dark .footer {
            color: #777777;
        }
        
        /* Text area styling */
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        
        .dark .stTextArea textarea {
            background-color: rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Logo animation */
        @keyframes boltPulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .logo-container {
            animation: boltPulse 3s infinite;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Success message */
        .stAlert {
            background-color: rgba(0, 139, 139, 0.2) !important;
            border-left: 4px solid #008B8B !important;
        }
        
        .dark .stAlert {
            background-color: rgba(0, 206, 209, 0.2) !important;
            border-left: 4px solid #00CED1 !important;
        }
        """)

local_css("styles.css")

# ---------- THEME TOGGLE ----------
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

col1, col2, col3 = st.columns([1,2,1])
with col3:
    if st.button('🌓 Toggle Theme'):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

if st.session_state.theme == 'dark':
    st.markdown('<div class="dark"></div>', unsafe_allow_html=True)

# ---------- LOGO ----------
st.markdown("""
    <div class="logo-container">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 3L6 12H10L8 21L19 10H14L16 3H11Z" fill="#008B8B" class="dark:fill-[#00CED1]"/>
        </svg>
    </div>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1 style='text-align: center;'>⚡ BoltTranslate</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Precision Language Translation for EveryBody </h4>", unsafe_allow_html=True)

# ---------- LANGUAGE CODES ----------
language_codes = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh",
    "Arabic": "ar",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt",
    "Turkish": "tr"
}

# ---------- TRANSLATION INTERFACE ----------
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", list(language_codes.keys()), index=0)
with col2:
    target_lang = st.selectbox("To", list(language_codes.keys()), index=1)

text_input = st.text_area("✏️ Enter text to translate", height=150, 
                         placeholder="Enter technical terms, research papers, or documentation...")

# ---------- TRANSLATE BUTTON ----------
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if text_input.strip():
        with st.spinner('Translating...'):
            try:
                # Translation
                translator = Translator(
                    from_lang=language_codes[source_lang], 
                    to_lang=language_codes[target_lang]
                )
                translated_text = translator.translate(text_input)
                
                # Display translation
                st.success("✅ Translation Complete")
                st.markdown(f"### {translated_text}")
                
                # Text-to-speech
                st.markdown("#### 🔊 Listen to Translation")
                tts = gTTS(translated_text, lang=language_codes[target_lang])
                tts.save("translation.mp3")
                
                audio_file = open("translation.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                os.remove("translation.mp3")
                
                # Copy to clipboard (simulated)
                st.markdown("#### 📋 Copy Translation")
                st.code(translated_text, language='text')
                
                # Add a nice animation effect
                st.balloons()
                
            except Exception as e:
                st.error(f"⚡ Translation failed: {str(e)}")
    else:
        st.warning("⚠️ Please enter some text to translate")

# ---------- FOOTER ----------
st.markdown("""
    <div class="footer">
        Made with ⚡ by Bilal Sikandar | EE Student • AI Intern
    </div>
""", unsafe_allow_html=True)