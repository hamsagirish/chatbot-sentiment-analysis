import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from textblob import TextBlob  # For sentiment analysis

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_mood' not in st.session_state:
    st.session_state.user_mood = "Neutral"

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to generate chatbot response
def generate_chatbot_response(user_message):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return "I'm sorry, I couldn't process that."

# Streamlit UI
st.title("AI Chatbot with Sentiment Analysis")

# Display chat history
st.markdown("## Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"*You:* {chat['user']}")
    st.markdown(f"*Bot:* {chat['bot']}")
    st.markdown(f"Mood: {chat['mood']}")

# Display current user mood
st.sidebar.markdown("## Current User Mood")
st.sidebar.markdown(f"### {st.session_state.user_mood}")

# User input
user_message = st.text_input("You: ")

if st.button("Send"):
    if user_message:
        # Analyze sentiment of user message
        mood = analyze_sentiment(user_message)
        st.session_state.user_mood = mood

        # Generate chatbot response
        bot_response = generate_chatbot_response(user_message)

        # Update chat history
        st.session_state.chat_history.append({
            'user': user_message,
            'bot': bot_response,
            'mood': mood
        })
        st.experimental_rerun()  # Rerun to update the chat history and mood display

# pip install streamlit textblob google-generativeai python-dotenv
# streamlit run main.py
