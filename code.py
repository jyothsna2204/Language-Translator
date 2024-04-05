#streamlit run voice_tra.py
import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize the translator module and mixer module
translator = Translator()
pygame.mixer.init()

# Set custom CSS styles for background and select box
st.markdown(
    """
    <style>
    body {
        background-color: #7FFFD4; /* Aquamarine background color */
    }
    .stSelectbox > select {
        background-color: #f0f0f0;
        color: #0072b1;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #ff9900; /* Change background color to orange */
        color: #ffffff;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #cc7a00; /* Change hover color to darker orange */
        color:blue;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a mapping between language names and language codes
language_mapping = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy',
    'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs',
    'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo',
    'Estonian': 'et', 'Filipino': 'fil', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka',
    'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw',
    'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga',
    'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko',
    'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb',
    'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr',
    'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Nyanja (Chichewa)': 'ny', 'Odia (Oriya)': 'or',
    'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese (Portugal, Brazil)': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro',
    'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd',
    'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tagalog (Filipino)': 'tl', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th',
    'Turkish': 'tr', 'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi',
    'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, to_language):
    return translator.translate(spoken_text, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, to_language):
    with sr.Microphone() as source:
        output_placeholder.text("Listening...")
        rec = sr.Recognizer()
        rec.pause_threshold = 1
        audio = rec.listen(source, phrase_time_limit=10)
    
    try:
        output_placeholder.text("Processing...")
        spoken_text = rec.recognize_google(audio)
        
        output_placeholder.text("Translating...")
        translated_text = translator_function(spoken_text, to_language)
        
        output_placeholder.success("Translated Text:")
        st.write(translated_text.text)
        text_to_voice(translated_text.text, to_language)
    
    except Exception as e:
        output_placeholder.error(f"Error: {e}")

# UI layout
st.title("Language Translator")

# Dropdown for selecting target translation language
to_language_name = st.selectbox("Select Target Language:", list(language_mapping.keys()))

# Convert language name to language code
to_language = get_language_code(to_language_name)

# Button to trigger translation
start_button = st.button("Start Translation")
stop_button = st.button("Stop Translation")

# Placeholder for dynamic output
output_placeholder = st.empty()

# Check if "Start Translation" button is clicked
if start_button:
    main_process(output_placeholder, to_language)

# Check if "Stop Translation" button is clicked
if stop_button:
    st.stop()