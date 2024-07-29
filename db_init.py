import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Global variable for Firestore database client
db = None

# Ensure that the 'init_db' function is called if needed
def init_db():
    global db

    # Check if Firebase app is already initialized
    if not firebase_admin._apps:
        # Load Firebase service account credentials from Streamlit secrets
        key_dict = json.loads(st.secrets["textkey"])

        # Initialize Firebase Admin SDK with the credentials and proper options
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred, options={
            'projectId': key_dict['project_id'],
            'databaseURL': 'https://{}.firebaseio.com'.format(key_dict['project_id']),
        })

    # Initialize the Firestore database if not already done
    if db is None:
        db = firestore.client()
    return db

# Function to initialize user data in session state if not already initialized
def init_user_data():
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {
            'name': '',
            'bot_name': '',
            'preferences': '',
            'camera_permission': False,
            'imgur_link': ''
        }

