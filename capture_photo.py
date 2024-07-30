import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io
import sys
from streamlit_extras.switch_page_button import switch_page

from utilities import sidebar_login

sidebar_login()

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database_updates as du

# Create a directory to store images if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def save_image(image, name):
    # Convert the image to PIL format and save
    image_pil = Image.fromarray(image)
    file_path = os.path.join(data_dir, f"{name}.png")
    image_pil.save(file_path)
    st.success(f"Image saved as {file_path}")

st.title("Register Here")

# Input field for the name of the person
name = st.text_input("Enter the name (username) of the person:")
password = st.text_input("Enter a password", type="password")
camera = st.camera_input("Click Photo")
if camera:
    video_bytes = camera.read()
    if video_bytes:
        # Convert video bytes to numpy array
        image = Image.open(io.BytesIO(video_bytes))
        frame = np.array(image)
    
        st.image(frame, caption="Photo Clicked", use_column_width=True)
        if name and password:
            save_image(frame,name)
            du.create_user(name,password)
            st.success("User Created")
            switch_page("face identity")