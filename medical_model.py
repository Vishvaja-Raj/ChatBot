import streamlit as st
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch


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
