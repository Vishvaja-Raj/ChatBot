import streamlit as st
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from utilities import make_sidebar

# Setup sidebar and title
make_sidebar()
# Twilio credentials (replace these with your actual credentials]
ACCOUNT_SID = st.secrets["ACCOUNT_SID"]
AUTH_TOKEN = st.secrets["AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"]
EMERGENCY_PHONE_NUMBER = '+16479381240'

# Initialize the Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_emergency_message():
    try:
        message = client.messages.create(
            body="This is an emergency message for XYZ.Kindly call them.",
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_PHONE_NUMBER
        )
        return f"Message sent! SID: {message.sid}"
    except TwilioRestException as e:
        return f"Failed to send message: {e}"

def make_emergency_call():
    try:
        call = client.calls.create(
            twiml='<Response><Say>This is an emergency. Call them.</Say></Response>',
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_PHONE_NUMBER
        )
        return f"Call initiated! SID: {call.sid}"
    except TwilioRestException as e:
        return f"Failed to initiate call: {e}"

# Streamlit app layout
st.title("Emergency Alert System")

st.write("Click the button below to send an emergency message or make a phone call.")

if st.button("Send Emergency Alert Message "):
    # Uncomment the function you want to use
    # result = send_emergency_message()
    result = send_emergency_message()
if st.button("Send Emergency Call"):
    # Uncomment the function you want to use
    # result = send_emergency_message()
    result = make_emergency_call()
    st.success(result)
