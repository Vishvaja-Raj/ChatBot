import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

import json
import db_init as di
from datetime import datetime
import bcrypt
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

def insert_medical_history(message, username, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow()

    try:
        # Create a new document in the 'medical_history' collection
        doc_ref = db.collection('medical_history').add({
            'message': message,
            'username': username,
            'timestamp': timestamp  # Firestore will automatically handle the datetime object
        })

        print(f"Document written with ID: {doc_ref.id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_user(name, password):
    """
    Creates a new user document in the Firestore `users` collection.
    
    Args:
        username (str): The user's username.
        name (str): The user's full name.
        password (str): The user's plain text password.

    Returns:
        None
    """
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create the user document
    user_doc_ref = db.collection('users').document(name)
    user_doc_ref.set({
        'name': name,
        'password': hashed_password.decode('utf-8'),  # Store the hashed password as a string
        'timestamp': datetime.utcnow()  # Add timestamp
    })

def check_user_credentials(name, password):
    """
    Checks if the provided username and password match the stored credentials in Firestore.
    
    Args:
        username (str): The user's username.
        password (str): The user's plain text password.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    try:
        # Fetch the user document
        user_doc_ref = db.collection('users').document(name)
        user_doc = user_doc_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            stored_hashed_password = user_data.get('password', '')

            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Error checking user credentials: {e}")
        return False

# Function to retrieve conversation history for a given name
def get_conversation_history(name):
    conversations = db.collection('conversations').where('name', '==', name).stream()
    history = [(conv.get('message'), conv.get('response')) for conv in conversations]
    return history

# Function to update user data in Firestore
def update_user_data(name,bot_name, preferences, imgur_link, camera_permission=None):
    doc_ref = db.collection('memory').document(name)
    user_data = {
        'name': name,
        'bot_name': bot_name,
        'preferences': preferences,
        'imgur_link': imgur_link,
        'camera_permission': camera_permission,
        'timestamp': datetime.utcnow()  # Add/update the timestamp
    }
    doc_ref.set(user_data, merge=True)

# Function to fetch user data from Firestore
# Function to fetch user data from Firestore based on username
def get_user_data(username):
    print(f"Fetching User Data for: {username}")
    try:
        # Query Firestore to find the user data based on the given username
        user_ref = db.collection('memory').where('name', '==', username).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).stream()
        
        for user in user_ref:
            user_data = user.to_dict()
            print("User Data Retrieved: " + str(user_data))
            return {
                'name': user_data.get('name', ''),
                'bot_name': user_data.get('bot_name', ''),
                'preferences': user_data.get('preferences', ''),
                'camera_permission': user_data.get('camera_permission', False),
                'imgur_link': user_data.get('imgur_link', '')
            }
        
        print("No user data found for the given username.")
        return None
    
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None



# Function to initialize session state from Firestore
def initialize_session_state_from_db(username):
    print("User 1")
    user_data = get_user_data(username)
    if user_data:
        st.session_state['user_data'] = user_data




    
