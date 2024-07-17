import streamlit as st
import speech_building as sb
import os
import time
import companion_building as cb
import video_generation as vg
from streamlit_extras.switch_page_button import switch_page
import db_init as di
from utilities import logo

logo()

value=0
# Initialize session state
di.init_user_data()
st.title("Welcome to the AI Assistant!")
print("Here")
st.subheader("Please enter your name:")
print("Name and value is 0")

#sb.text_to_speech("Please enter your name")
name = st.text_input("Name:")
if name:
    print("Name has been defined")
    st.session_state['user_data']['name'] = name
    st.success(f"Hello {name}!")

    
st.subheader("Please enter your preferences:")
#sb.text_to_speech("Please enter your preferences")
preferences = sb.speech_to_text()
if preferences:
    st.session_state['user_data']['preferences'] = preferences
    st.success(f"Preferences noted: {preferences}")

            

if st.session_state['user_data']['name'] and st.session_state['user_data']['preferences']:
    print("here session1")
    if st.button("Submit"):
        print("here session")
        # Store data in the database
        # du.update_user_data(
        #     name=st.session_state['user_data']['name'],
        #     preferences=st.session_state['user_data']['preferences']
        # )
        print("here session2")
        switch_page('Create Me')


