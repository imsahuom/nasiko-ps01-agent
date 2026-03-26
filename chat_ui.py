import streamlit as st
import requests
import uuid

API_URL = "http://localhost:5000/"

st.set_page_config(page_title="Aura Support Agent")

st.title("Aura Customer Support")
st.write("Ask any question related to billing, returns, or technical issues.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context_id" not in st.session_state:
    st.session_state.context_id = None


def send_query(text, context_id):

    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        },
        "id": 1
    }

    if context_id:
        payload["params"]["contextId"] = context_id

    response = requests.post(API_URL, json=payload).json()

    return response


user_input = st.chat_input("Type your question here...")

if user_input:

    st.session_state.messages.append(("user", user_input))

    response = send_query(user_input, st.session_state.context_id)

    try:
        agent_reply = response["result"]["artifacts"][0]["parts"][0]["text"]
        st.session_state.context_id = response["result"]["contextId"]

    except:
        agent_reply = "Error getting response"

    st.session_state.messages.append(("agent", agent_reply))


for role, message in st.session_state.messages:

    if role == "user":
        st.chat_message("user").write(message)

    else:
        st.chat_message("assistant").write(message)