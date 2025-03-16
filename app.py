import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# IMPORTANT:  Replace with your actual Gemini API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


# Set Streamlit Theme to Dark Mode (or a custom theme)
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Theme and Better Readability
st.markdown(
    """
    <style>
    body {
        color: #fff;  /* Set default text color to white */
        background-color: #1e1e1e; /* Dark background color */
    }
    .stTextInput>div>div>input {
        color: #fff;
        background-color: #333;
    }
    .stTextArea>div>div>textarea {
        color: #fff;
        background-color: #333;
    }
    p {
        color: #fff; /* Ensure paragraph text is white */
    }
    .stErrorMessage {
        color: #ffa07a; /* Light salmon color for error messages */
    }
    .stWarning {
        color: #f0ad4e; /* Amber color for warning messages */
    }
    .stSuccess {
        color: #32cd32; /* Lime green for success messages */
    }
    /* Style for chat bubbles */
    .user-message {
        background-color: #333;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        color: #fff; /* White text for user messages */
    }
    .gemini-message {
        background-color: #444;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        color: #fff; /* White text for Gemini messages */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configure Gemini
def configure_gemini():
    genai.configure(api_key=GOOGLE_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Try 'gemini-1.0-pro' first
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        st.error(f"Error initializing Gemini with 'gemini-1.5-flash': {e}")
        try:
            model = genai.GenerativeModel('gemini-pro') # Fallback to 'gemini-pro' if available
            chat = model.start_chat(history=[])
            return chat
        except Exception as e:
            st.error(f"Error initializing Gemini with 'gemini-pro': {e}.  Please check your API key and model availability.")
            return None # Handle the case where no model can be initialized


# Streamlit app
def main():
    st.title("Gemini AI Chatbot")

    # Initialize chat in session state (if not already)
    if "chat" not in st.session_state:
        st.session_state.chat = configure_gemini()

    # Check if chat was successfully initialized
    if st.session_state.chat is None:
        st.warning("Gemini failed to initialize. Please check your API key and model availability.")
        return # Stop the app if Gemini initialization failed


    # Display chat history
    for message in st.session_state.chat.history:
        if message.role == 'user':
            st.markdown(f'<div class="user-message"><b>You:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="gemini-message"><b>Gemini:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

    # Get user input
    prompt = st.text_input("Ask me anything:", key="prompt")

    # Handle user input
    if prompt:
        try:
            # Get response from Gemini
            response = st.session_state.chat.send_message(prompt)

            # Display the response immediately (for a better user experience)
            st.markdown(f'<div class="gemini-message"><b>Gemini:</b> {response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during chat: {e}")


if __name__ == "__main__":
    main()
