import streamlit as st
import requests
import time
did_api_key = st.secrets["did_api_key"]  # Ensure you have this secret defined in Streamlit secrets
placeholder = st.empty()
from utilities import logo
# Function to generate video based on the prompt and avatar selection
def generate_video(text, image_url, gender):
    print("Hello")
    url = "https://api.d-id.com/talks"
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization" : "Basic "+did_api_key
    }
    if gender == "Female":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                },
                "ssml": "false",
                "input":text
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": image_url
        }

    if gender == "Male":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-BrandonNeural"
                },
                "ssml": "false",
                "input":text
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": image_url
        }
    
    try:
        print("Hello2")
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(response.text)
            res = response.json()
            id = res["id"]
            print("Id" + str(id))
            status = "created"
            while status == "created":
                getresponse =  requests.get(f"{url}/{id}", headers=headers)
                print(getresponse)
                if getresponse.status_code == 200:
                    status = res["status"]
                    res = getresponse.json()
                    print(res)
                    if res["status"] == "done":
                        video_url =  res["result_url"]
                    else:
                        time.sleep(10)
                else:
                    status = "error"
                    video_url = "error"
        else:
            print("error:")
            print(response.text)
            video_url = "error"   
    except Exception as e:
        print(e)      
        video_url = "error"      
        
    return video_url


def video_response(uploaded_image_url, user_input):

    if st.button("Generate Video Response"):
        if user_input or uploaded_image_url:
            text = user_input
            voice = "default"  # Replace with the selected voice or user's choice
            img_url = uploaded_image_url if uploaded_image_url else "https://example.com/default_image.jpg"
            video_url = generate_video(text,img_url,"Male")
            if video_url:
                st.video(video_url)
            else:
                st.error("Failed to generate video response")

def video_show(uploaded_image_url, user_input):
    if user_input or uploaded_image_url:
        text = user_input
        placeholder.empty()
        img_url = uploaded_image_url if uploaded_image_url else "https://example.com/default_image.jpg"
        video_url = None
        video_url = generate_video(text, img_url, "Male")
        if video_url:
            logo()
            container_id = "video_container"
            video_html = f"""
            <h1> Chat with me </h1>
            <div id="{container_id}">
                <video width="320" height="240" controls autoplay id="video_element">
                  <source src="{video_url}" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
            </div>
            """
            placeholder.markdown(video_html, unsafe_allow_html=True) 
            
        else:
            st.error("Failed to generate video response")