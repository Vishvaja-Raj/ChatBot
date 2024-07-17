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
from streamlit_extras.switch_page_button import switch_page
from utilities import logo

logo()

st.title("Upload an Image")
image_url = cb.image_upload()
print(image_url)
st.session_state['user_data']['imgur_link'] = image_url
vg.video_response(image_url,"Hello World")
if st.button("Next"):
    st.session_state.step = 'conversation'
    du.update_user_data(
                name=st.session_state['user_data']['name'],
                preferences=st.session_state['user_data']['preferences'],
                imgur_link=st.session_state['user_data']['imgur_link']
            )
    print("USER DATA"+str(st.session_state['user_data']))
    switch_page('Chat With Me')


