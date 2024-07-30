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

make_sidebar()

st.title("Upload an Image")
image_url = cb.image_upload()
print(image_url)
st.session_state['user_data']['imgur_link'] = image_url
vg.video_response(image_url,"Hello World")
if st.button("Next"):
    st.session_state.step = 'conversation'
    du.update_user_data(
                name=st.session_state['user_data']['name'],
                bot_name = st.session_state['user_data']['bot_name'],
                preferences=st.session_state['user_data']['preferences'],
                imgur_link=st.session_state['user_data']['imgur_link']
            )
    print("USER DATA"+str(st.session_state['user_data']))
    st.switch_page('pages/STEP3.py')


