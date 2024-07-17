import streamlit as st
import database_updates as du


def initialize_session_state_from_db():
    # Query the database for existing user data
    user_data = du.get_user_data()  # Assuming this function returns a dictionary with 'name' and 'preferences' keys
    
    if user_data:
        st.session_state['user_data'] = {
            'name': user_data.get('name', ''),
            'preferences': user_data.get('preferences', ''),
            'camera_permission': False,  # Set default values for other session state variables if needed
            'imgur_link': ''
        }

def initialise_session_state():
# Initialize session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'input' not in st.session_state:
        st.session_state['input'] = ""

    if 'stored_session' not in st.session_state:
        st.session_state['stored_session'] = str(st.session_state)

    if 'camera_open' not in st.session_state:
        st.session_state['camera_open'] = False

    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {
            'name': None,
            'preferences': None,
            'camera_permission': False,
            'imgur_link': None,
        }
   
def preferences_setting(user_input, output):
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    du.insert_conversation(st.session_state['stored_session'], user_input, output)  # Record conversation

    # Update user data based on conversation context
    if "my name is" in user_input.lower() and len(user_input.split()) > 3:
        name = user_input.split("my name is")[1].strip()
        du.update_user_data(name=name)

    if "i like" in user_input.lower():
        preferences = user_input.split("i like")[1].strip()
        du.update_user_data(preferences=preferences)

    if "allow camera" in user_input.lower():
        du.update_user_data(camera_permission=True)