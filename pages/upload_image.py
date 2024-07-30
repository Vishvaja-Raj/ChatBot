import streamlit as st
import video_generation as vg
import companion_building as cb
import database_updates as du

from utilities import make_sidebar

# Setup sidebar and title
make_sidebar()

st.title("Upload an Image")
image_url = cb.image_upload()
st.session_state['user_data']['imgur_link'] = image_url

# Video response function call
vg.video_response(image_url, "Hello World")

# Display the next button only after image upload
if st.button("Next"):
    st.session_state.step = 'conversation'
    du.update_user_data(
        name=st.session_state['user_data']['name'],
        bot_name=st.session_state['user_data']['bot_name'],
        preferences=st.session_state['user_data']['preferences'],
        imgur_link=st.session_state['user_data']['imgur_link']
    )
    st.write("USER DATA: " + str(st.session_state['user_data']))
    st.switch_page("pages/STEP3.py")