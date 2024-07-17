import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import time
import os
from pydub import AudioSegment
from pydub.playback import play
from langchain.llms import OpenAI
import database_updates as du
import video_generation as vg
from audiorecorder import audiorecorder

api_key = st.secrets["api_secret"]

# Initialize pyttsx3 engine

print("==")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_wav(file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(file_path) as source:
        # Listen to the audio file
        audio_data = recognizer.record(source)
        
        try:
            # Recognize the speech in the audio
            user_input = recognizer.recognize_google(audio_data)
            print("Recognized Text: ", user_input)
            return user_input
        except sr.UnknownValueError:
            st.warning("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            st.error("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

def speech_to_text():
    print("in audio")
    audio_bytes = audiorecorder("Click to record")
    if len(audio_bytes)>0:
        print("xsgbjdghha")
        audio_bytes.export("audio.wav", format="wav")
        user_input = recognize_speech_from_wav("audio.wav")
        return user_input
    
def load_conversation():
    if api_key:
        llm = OpenAI(
            temperature=0.5,
            openai_api_key=api_key,
            model="gpt-3.5-turbo-instruct"
        )
        if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)

            # Fetch conversation history and load into entity memory
            conversation_history = du.get_conversation_history(st.session_state['user_data']['name'])
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
    return Conversation

def conversation_bot(Conversation):
    # Initialize the variable to avoid UnboundLocalError
    user_input_speech = ""

    # Speech-to-Text Input with output on the left and button on the right
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Click the microphone button and start speaking...")
        if st.button("Start Recording"):
            user_input_speech = speech_to_text()
            if user_input_speech:
                st.text_area("You", value=user_input_speech, key='input_text_speech', height=100, max_chars=None, help="Your AI Assistant here! Ask me anything ...")
                # Automatically run conversation with the speech input
                output = Conversation.run(input=user_input_speech)
                st.session_state.past.append(user_input_speech)
                st.session_state.generated.append(output)
                du.insert_conversation(st.session_state['user_data']['name'], user_input_speech, output)  # Record conversation

                # Update user data based on conversation context
                if "my name is" in user_input_speech.lower() and len(user_input_speech.split()) > 3:
                    name = user_input_speech.split("my name is")[1].strip()
                    du.update_user_data(name=name)

                if "i like" in user_input_speech.lower():
                    split_input = user_input_speech.lower().split("i like")
                    if len(split_input) > 1:
                        preferences = split_input[1].strip()
                        du.update_user_data(preferences=preferences)
                else:
                    st.warning("Sorry, I could not understand your preferences.")

                if "allow camera" in user_input_speech.lower():
                    du.update_user_data(camera_permission=True)
                
                                # Use gtts to voice out the last conversation
                tts = gTTS(output)
                tts.save("output.mp3")
                time.sleep(5)
                audio_file = AudioSegment.from_file('output.mp3')

                # Play the audio
                play(audio_file)
                os.remove("output.mp3")
                st.experimental_rerun() 


    return user_input_speech

def chatbot_text_interface(Conversation):
    user_input_text = st.text_input("You: ", "", key="input_text")

    if user_input_text:
        # Run conversation with the text input
        output = Conversation.run(input=user_input_text)
        st.session_state.past.append(user_input_text)
        st.session_state.generated.append(output)
        img_link = st.session_state['user_data']['imgur_link']
        print(img_link)
        vg.video_show(img_link,output)
        du.insert_conversation(st.session_state['user_data']['name'], user_input_text, output)  # Record conversation
        if "allow camera" in user_input_text.lower():
            du.update_user_data(camera_permission=True)
            
    # Display conversation in an expandable box with the latest messages first
    with st.expander("Display the conversation"):
        conversation_html = ""
        for msg, resp in zip(reversed(st.session_state.past), reversed(st.session_state.generated)):
            conversation_html += f"""
                <div style='padding: 10px; margin: 5px 0; border-radius: 5px; background-color: #f0f0f0;'>
                    <strong style='color: #1a73e8;'>You:👨‍🎓</strong> {msg}
                </div>
                <div style='padding: 10px; margin: 5px 0; border-radius: 5px; background-color: #e0f7fa;'>
                    <strong style='color: #d32f2f;'>Bot:🤖</strong> {resp}
                </div>
            """
        st.markdown(conversation_html, unsafe_allow_html=True)