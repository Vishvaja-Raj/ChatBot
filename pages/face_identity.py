import streamlit as st
import face_recognition
import numpy as np
import os
from PIL import Image
import cv2
import io
import face_detect as fd

from utilities import sidebar_login

sidebar_login()

# Streamlit interface
st.title("Login To Continue")

uploaded_image = st.camera_input("Take a picture")

if uploaded_image:
    video_bytes = uploaded_image.read()
    if video_bytes:
        # Convert video bytes to numpy array
        image = Image.open(io.BytesIO(video_bytes))
        # Paths to the known faces database and the uploaded photo
        database_path = os.path.join(os.getcwd(), "data")  # Path to your image database
        save_path = os.getcwd()  # Path to save the image
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        image_path = os.path.join(save_path, "sample.jpg")
        image.save(image_path)
        # Load known faces
        known_face_encodings, known_face_names = fd.load_known_faces(database_path)

        # Compare the uploaded image with known faces
        fd.compare_faces(known_face_encodings, known_face_names, image_path)
