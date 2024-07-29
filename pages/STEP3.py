import streamlit as st
import speech_building as sb
import database_updates as du
import preferences_set as ps
import db_init as di
from utilities import make_sidebar

make_sidebar()
# Load conversation chain
di.init_user_data()
# Ensure the session state for input and show_past is initialized
st.session_state.step = 'conversation'
def third_step():
    if 'input' not in st.session_state:
        st.session_state.input = ""

    if 'show_past' not in st.session_state:
        st.session_state.show_past = False

    if 'past' not in st.session_state:
        st.session_state.past = []

    if 'generated' not in st.session_state:
        st.session_state.generated = []
    Conversation = sb.load_conversation()
# Load conversation chain
    #sb.conversation_bot(Conversation)
    sb.chatbot_text_interface(Conversation)
    
    
    if st.session_state.show_past:
        st.info("Past Conversations:")
        for i in range(len(st.session_state.generated) - 2, -1, -1):
            st.info(st.session_state.past[i], icon="👨‍🎓")
            st.success(st.session_state.generated[i], icon="🤖")
            st. experimental_rerun()

def step3():
    if st.session_state.step == 'conversation':
            du.initialize_session_state_from_db()
            print("User Data is"+ str(st.session_state['user_data']))
            st.title("Chat with the AI Assistant")
            third_step()

step3()