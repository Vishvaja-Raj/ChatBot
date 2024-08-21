import streamlit as st
import joblib

# Load the saved model and vectorizer
model = joblib.load('model_files/medical_model.pkl')
vectorizer = joblib.load('model_files/vectorizer.pkl')

# Function to classify text
def classify_text(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    return 'Medical' if prediction[0] == 1 else 'Non-Medical'

# Streamlit app
def main():
    st.title("Medical Text Classification")

    st.write("Enter a text to classify as Medical or Non-Medical:")

    user_input = st.text_area("Input Text")

    if st.button("Classify"):
        if user_input:
            classification = classify_text(user_input)
            st.write(f"The text is classified as: **{classification}**")
        else:
            st.warning("Please enter some text to classify.")

if __name__ == "__main__":
    main()
