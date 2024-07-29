import face_recognition
import numpy as np
import os
from PIL import Image
import streamlit as st
import database_updates as du
from time import sleep

def load_known_faces(database_path):
    """Load known faces from images in the specified directory."""
    known_face_encodings = []
    known_face_names = []
    
    for image_name in os.listdir(database_path):
        image_path = os.path.join(database_path, image_name)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(image_name)[0])  # Name from image filename
    
    return known_face_encodings, known_face_names

def compare_faces(known_face_encodings, known_face_names, unknown_image_path):
    """Compare the uploaded image with known faces."""
    state = 0
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    
    if not unknown_face_encodings:
        st.warning("No faces found in the unknown image.")
        return
    
    for unknown_face_encoding in unknown_face_encodings:
        results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
        
        for i, match in enumerate(results):
            if match:
                st.success(f"Hello {known_face_names[i]} !!")
                password = st.text_input("Please enter your password:", type="password")
                if password:
                    if du.check_user_credentials(known_face_names[i],password):
                        st.success("Password correct! Access granted.")
                        st.session_state.logged_in = True
                        sleep(0.5)
                        st.switch_page("pages/step1.py")
                    else:
                        st.error("Incorrect password. Access denied.")
                return  # Exit the function after processing the first match
            else:
                state+=1
        if state>0:
            st.warning("Image not present in database")




