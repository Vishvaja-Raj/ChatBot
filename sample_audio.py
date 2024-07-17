import streamlit as st
import sqlite3
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import pyttsx3
import speech_recognition as sr
import os

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
        'camera_permission': False
    }

# Database functions
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
                    session_id TEXT,
                    message TEXT,
                    response TEXT
                 )''')
    conn.commit()
    conn.close()

def insert_conversation(session_id, message, response):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO conversations (session_id, message, response) VALUES (?, ?, ?)', 
              (session_id, message, response))
    conn.commit()
    conn.close()

def get_conversation_history(session_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT message, response FROM conversations WHERE session_id = ?', (session_id,))
    history = c.fetchall()
    conn.close()
    return history

def update_user_data(name=None, preferences=None, camera_permission=False):
    st.session_state['user_data']['name'] = name
    st.session_state['user_data']['preferences'] = preferences
    st.session_state['user_data']['camera_permission'] = camera_permission

# Initialize the database
init_db()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak into the microphone...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand your speech.")
        return ""
    except sr.RequestError as e:
        st.error(f"Request error from Google Speech Recognition service: {e}")
        return ""

st.title("Memory Bot")

api_key = os.environ['API_KEY']
if api_key:
    llm = OpenAI(
        temperature=0.5,
        openai_api_key=api_key,
        model="gpt-3.5-turbo-instruct"
    )
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)

        # Fetch conversation history and load into entity memory
        conversation_history = get_conversation_history(st.session_state['stored_session'])
        for message, response in conversation_history:
            st.session_state.entity_memory.save_context({"input": message}, {"output": response})
            st.session_state.past.append(message)
            st.session_state.generated.append(response)

        # Restore user data if available
        if 'name' in st.session_state['user_data'] and st.session_state['user_data']['name']:
            st.session_state.entity_memory.save_context({"input": "My name is " + st.session_state['user_data']['name']}, {"output": "Nice to meet you, " + st.session_state['user_data']['name']})

        if 'preferences' in st.session_state['user_data'] and st.session_state['user_data']['preferences']:
            st.session_state.entity_memory.save_context({"input": "My preferences are " + st.session_state['user_data']['preferences']}, {"output": "I'll remember that you like " + st.session_state['user_data']['preferences']})

        if st.session_state['user_data']['camera_permission']:
            st.session_state.entity_memory.save_context({"input": "Allow camera"}, {"output": "I can access your camera."})

    Conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory,
    )
else:
    st.error("No API Key Found")
    st.stop()

# Camera option
if st.button("Open Camera"):
    st.session_state['camera_open'] = True

if st.session_state['camera_open']:
    RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    webrtc_streamer(key="example", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIGURATION)

# Speech-to-Text Input with output on the left and button on the right
col1, col2 = st.columns([2, 1])
with col1:
    with st.expander("Conversation"):
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            if i < len(st.session_state["past"]) and i < len(st.session_state["generated"]):
                st.info(st.session_state["past"][i], icon="👨‍🎓")
                st.success(st.session_state["generated"][i], icon="🤖")

with col2:
    st.info("Click the microphone button and start speaking...")
    if st.button("Start Recording"):
        user_input_speech = speech_to_text()
        if user_input_speech:
            st.text_area("You", value=user_input_speech, key='input_text_speech', height=100, max_chars=None, help="Your AI Assistant here! Ask me anything ...")
            # Automatically run conversation with the speech input
            output = Conversation.run(input=user_input_speech)
            st.session_state.past.append(user_input_speech)
            st.session_state.generated.append(output)
            insert_conversation(st.session_state['stored_session'], user_input_speech, output)  # Record conversation

            # Update user data based on conversation context
            if "my name is" in user_input_speech.lower() and len(user_input_speech.split()) > 3:
                name = user_input_speech.split("my name is", 1)[1].strip()
                update_user_data(name=name)
                st.session_state.entity_memory.save_context({"input": "My name is " + name}, {"output": "Nice to meet you, " + name})

            if "my preferences are" in user_input_speech.lower() and len(user_input_speech.split()) > 4:
                preferences = user_input_speech.split("my preferences are", 1)[1].strip()
                update_user_data(preferences=preferences)
                st.session_state.entity_memory.save_context({"input": "My preferences are " + preferences}, {"output": "I'll remember that you like " + preferences})

            if "allow camera" in user_input_speech.lower():
                update_user_data(camera_permission=True)
                st.session_state.entity_memory.save_context({"input": "Allow camera"}, {"output": "I can access your camera."})

            # Save current interaction to memory
            st.session_state.entity_memory.save_context({"input": user_input_speech}, {"output": output})

            # Record the conversation in the database
            insert_conversation(st.session_state['stored_session'], user_input_speech, output)

            # Use pyttsx3 for text-to-speech
            engine = pyttsx3.init()
            engine.say(output)
            engine.runAndWait()
            print(f"Spoken output from speech input: {output}")  # Debug statement
