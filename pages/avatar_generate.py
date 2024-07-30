import streamlit as st
import video_generation as vg
import database_updates as du
import companion_building as cb
from utilities import make_sidebar

# Setup sidebar and title
make_sidebar()

st.title("Create your avatar now")
text = st.text_input("Enter your description", "")

if text:  # Ensure text is not empty
    st.write("Generating your avatar...")
    try:
        image_url = cb.create_avatar(text)
        st.image(image_url, caption='Your Avatar', use_column_width=True)
        st.session_state['user_data']['imgur_link'] = image_url
        st.write(f"Generated avatar URL: {image_url}")
        vg.video_response(image_url, "Hello World")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter a description before clicking the button.")

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