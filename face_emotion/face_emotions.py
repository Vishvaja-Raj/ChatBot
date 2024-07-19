import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io

model = load_model('model.h5')

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def face_emotion_detection():
    # Load pre-trained model


    # Initialize Streamlit components
    st.title("Real-Time Mood Recognition")

    # Initialize webcam video capture
    camera = st.camera_input("Capture Video")

    if camera:
    # Convert the uploaded video frame to an OpenCV image

        video_bytes = camera.read()
        if video_bytes:
            # Convert video bytes to numpy array
            image = Image.open(io.BytesIO(video_bytes))
            frame = np.array(image)
            
            # Process the frame for emotion recognition
            processed_frame = predict_emotion(frame)
            
            # Convert the processed frame back to an image format for Streamlit
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            st.image(processed_frame, caption="Mood Recognition", use_column_width=True)

def predict_emotion(frame):
    """Function to predict emotion in a given frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    for (x, y, w, h) in faces:
        # Extract face region
        face = gray[y:y+h, x:x+w]
        
        # Resize and normalize
        face = cv2.resize(face, (48, 48))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)
        
        # Predict emotion
        prediction = model.predict(face)
        emotion = emotion_labels[np.argmax(prediction)]
        
        # Draw rectangle around the face and label it with the emotion
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    return frame


