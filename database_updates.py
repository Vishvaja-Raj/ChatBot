import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json
import db_init as di
from datetime import datetime

db = di.init_db()

def get_next_conversation_id():
    counter_ref = db.collection('counters').document('conversation_counter')
    counter_doc = counter_ref.get()

    if counter_doc.exists:
        counter_data = counter_doc.to_dict()
        next_id = counter_data['current_id'] + 1
        counter_ref.update({'current_id': next_id})
    else:
        next_id = 1
        counter_ref.set({'current_id': next_id})

    return next_id

def insert_conversation(name, message, response):
    conversation_id = get_next_conversation_id()
    doc_ref = db.collection('conversations').document(str(conversation_id))
    doc_ref.set({
        'conversation_id': conversation_id,
        'name': name,
        'message': message,
        'response': response,
        'timestamp': datetime.utcnow()  # Add a timestamp
    })

# Function to retrieve conversation history for a given name
def get_conversation_history(name):
    conversations = db.collection('conversations').where('name', '==', name).stream()
    history = [(conv.get('message'), conv.get('response')) for conv in conversations]
    return history

# Function to update user data in Firestore
def update_user_data(name, preferences, imgur_link, camera_permission=None):
    doc_ref = db.collection('memory').document(name)
    user_data = {
        'name': name,
        'preferences': preferences,
        'imgur_link': imgur_link,
        'camera_permission': camera_permission,
        'timestamp': datetime.utcnow()  # Add/update the timestamp
    }
    doc_ref.set(user_data, merge=True)

# Function to fetch user data from Firestore
def get_user_data():
    print("Fetching User Data")
    try:
        user_ref = db.collection('memory').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).stream()
        for user in user_ref:
            user_data = user.to_dict()
            print("User Data Retrieved: " + str(user_data))
            return {
                'name': user_data.get('name', ''),
                'preferences': user_data.get('preferences', ''),
                'camera_permission': user_data.get('camera_permission', False),
                'imgur_link': user_data.get('imgur_link', '')
            }
        print("No user data found.")
        return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None


# Function to initialize session state from Firestore
def initialize_session_state_from_db():
    print("User 1")
    user_data = get_user_data()
    if user_data:
        st.session_state['user_data'] = user_data




    
