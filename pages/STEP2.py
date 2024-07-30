import streamlit as st
import database_updates as du
import speech_recognition as sr
from gtts import gTTS
import os
import time
import pygame
from pathlib import Path
import pyttsx3
import speech_building as sb
import companion_building as cb
import video_generation as vg
from utilities import make_sidebar

# Setup sidebar and title
make_sidebar()
st.title("Choose any One")

# Define columns for layout
col1, col2 = st.columns([1, 1])

# Column 1: Upload Image
with col1:
    if st.button("Upload an Image"):
        st.switch_page("pages/upload_image.py")
        

# Column 2: Create Avatar
with col2:
    if st.button("Generate an Avatar"):
        st.switch_page("pages/avatar_generate.py")

