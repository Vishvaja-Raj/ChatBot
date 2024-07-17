import streamlit as st
import preferences_set as ps
import database_updates as du
import companion_building as cb
import mood_recognition as mr
import video_generation as vg
import speech_building as sb

# Initialize session states and database
ps.initialise_session_state()
du.init_db()
st.title("Memory Bot")

# Load conversation chain
Conversation = sb.load_conversation()

# Set camera state
mr.camera_state()

# Ensure the session state for input and show_past is initialized
if 'input' not in st.session_state:
    st.session_state.input = ""

if 'show_past' not in st.session_state:
    st.session_state.show_past = False

# Function to handle user input and update conversation
def handle_user_input(user_input):
    if user_input:
        output = Conversation.run(input=user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        du.insert_conversation(st.session_state['stored_session'], user_input, output)  # Record conversation
        ps.preferences_setting(user_input, output)

# Layout organization
left_column, right_column = st.columns([1, 2])

# Text Input with on_change callback
with left_column:
    user_input = st.text_input(
        "You: ",
        key="input",
        placeholder="Your AI Assistant here! Ask me anything ..."
    )

    # Handle submission when Enter key is pressed
    if st.session_state.input and st.session_state.input != "":
        handle_user_input(st.session_state.input)

# Button to show past conversations (positioned in top left corner)
with left_column:
    show_past_button = st.button("Show Past Conversations", key="show_past_button", help="Click to show/hide past conversations")
    if show_past_button:
        st.session_state.show_past = not st.session_state.show_past

# Display the last conversation
with right_column:
    if st.session_state.generated:
        st.info("Last Conversation:")
        st.success(st.session_state.past[-1], icon="👨‍🎓")
        st.success(st.session_state.generated[-1], icon="🤖")

# Display past conversations if the button is clicked
if st.session_state.show_past:
    st.info("Past Conversations:")
    for i in range(len(st.session_state.generated) - 2, -1, -1):
        st.info(st.session_state.past[i], icon="👨‍🎓")
        st.success(st.session_state.generated[i], icon="🤖")

# Speech-to-Text Input with output on the left and button on the right
user_input_speech = sb.conversation_bot(Conversation)

# Example function calls for companion and video response
image_url = cb.image_upload()
vg.video_response(st.session_state.input, user_input_speech, image_url)
