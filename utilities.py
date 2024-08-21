from streamlit_extras.app_logo import add_logo
from st_pages import Page, show_pages, add_page_title
import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from streamlit_extras.switch_page_button import switch_page


def logo():
    add_logo("uploads/grt-health.png", height=300)

# Optional -- adds the title and icon to the current page

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def sidebar_login():
    with st.sidebar:
        st.image("uploads/grt-health.png", width=250)
        st.write("")
        st.write("")
        st.page_link("capture_photo.py",label = "Register", icon="®️")
        st.page_link("pages/face_identity.py",label = "Login", icon="🔐")

def make_sidebar():
    with st.sidebar:
        st.image("uploads/grt-health.png", width=250)
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", True):

            st.page_link("pages/STEP1.py", label="Enter your details", icon="🏠")
            st.page_link("pages/STEP2.py", label="Create Me", icon="🧑")
            st.page_link("pages/STEP3.py", label="Chat With Me", icon="🤖")
            st.page_link("pages/STEP4.py", label="Click a Photo", icon="🕵️")
            st.page_link("pages/STEP5.py", label="Emergency Alert", icon="🆘")
            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "face_identity.py":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("face_identity.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    switch_page("face identity")