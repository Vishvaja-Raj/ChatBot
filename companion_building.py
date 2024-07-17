import streamlit as st
import requests
import base64
import os

imgur_client_id = st.secrets["imgur_client_id"]  # Ensure you have this secret defined in Streamlit secrets

# Function to upload image to Imgur
def upload_image_to_imgur(image_path, client_id):
    url = "https://api.imgur.com/3/image"
    headers = {'Authorization': f'Client-ID {client_id}'}
    
    try:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        payload = {'image': base64.b64encode(img_data)}
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'data' in response_data and 'link' in response_data['data']:
                return response_data['data']['link']
            else:
                st.error(f"Unexpected response structure: {response_data}")
                return None
        else:
            response_data = response.json()
            error_message = response_data.get('data', {}).get('error', 'Unknown error')
            st.error(f"Error uploading image: {error_message}")
            return None
    
    except Exception as e:
        st.error(f"An exception occurred: {e}")
        return None


def image_upload():
    # Image upload section
    uploaded_image = st.file_uploader("Upload an image for video response (optional):", type=["jpg", "png"])
    image_url = None
    
    if uploaded_image:
        print("Image upload started.")
        # Ensure the 'uploads' directory exists
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        print("Uploads directory ensured.")
        
        img_path = os.path.join("uploads", uploaded_image.name)
        with open(img_path, "wb") as f:
            print("Saving uploaded image.")
            f.write(uploaded_image.getbuffer())
        
        # Uncomment this line if you want to display the image in Streamlit
        # st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        image_url = upload_image_to_imgur(img_path, imgur_client_id)
        if image_url:
            st.session_state.user_data['imgur_link'] = image_url
            print("Result is " + str(image_url))
    else:
        print("Error: No image uploaded.")
    
    return image_url


