import streamlit as st
import requests

st.set_page_config(page_title="LangGraph AI Agent", layout="centered")

API_URL = "http://127.0.0.1:8000/chat"

MODEL_NAMES = [
    
]

st.title('LangGraph Chatbot Agent')
st.subheader('Chat with your LangGraph Agent')
given_system_prompt = st.text_area("Define your AI Agent :", height=10, placeholder="Enter your system prompt here!")
selected_model = st.selectbox("Select a model", MODEL_NAMES)
user_input = st.text_area("Enter your message:", height=150, placeholder="Enter your message here!")
if st.button('Submit'):
    if user_input.strip():
        try:
            payload = {"messages":{user_input}, "model_name": selected_model, "system_prompt": given_system_prompt}
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    ai_responses = [
                        message.get("content","")
                        for message in response_data("messages",[])
                        if message.get("type") == "ai"
                    ]
                    if ai_responses:
                        st.subheader("Agent response :")
                        st.markdown({ai_responses[-1]})
                    else:
                        st.warning("No AI responses found.")
            else:
                st.error(f"Request failed with status code - {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred : {str(e)}")
    else:
        st.warning("Please enter a message before submitting.")

