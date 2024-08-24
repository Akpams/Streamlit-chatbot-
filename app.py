import streamlit as st
from openai import OpenAI
import shelve
import datetime

from dotenv import load_dotenv
def home():
    load_dotenv()
    user = "🕵🏻‍♂️"
    bot = "🤶🏻"
    def inject_css():
        st.markdown("""
            <style>
                h1 {
                    color: darkgray;
                    text-align: center;
                    block:
                }
                .css-1w3y7u5 {
                    background-color: lightblue; 
                }
            </style>
        """, unsafe_allow_html=True)


    inject_css()
    st.title("Akpam Chat Bot")

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
    )

    def load_chat_history(name=None):
        with shelve.open("chat_history") as db:
            if name:
                return db.get(name, [])
            return []

    def save_chat_history(messages, name):
        with shelve.open("chat_history") as db:
            db[name] = messages

    def get_saved_conversations():
        with shelve.open("chat_history") as db:
            return list(db.keys())

    with st.sidebar:
        saved_conversations = get_saved_conversations()
        if st.button("New Chat"):
            st.session_state.messages = []
            st.session_state.conversation_name = None
        selected_conversation = st.selectbox("Load Conversation", saved_conversations)
        if st.button("Load"):
            st.session_state.messages = load_chat_history(selected_conversation)
            st.session_state.conversation_name = selected_conversation
        # if st.button("settings"):
        #     theme =st.radio("select theme",("light", "dark"))
        #     select_theme(theme)
        #     inject_css()
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_name = None

    for message in st.session_state.messages:
        avatar = user if message["role"] == "user" else bot
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Say something..."):
        if not st.session_state.conversation_name:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.session_state.conversation_name = f"{prompt[:20]}"
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=user):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar=bot):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_chat_history(st.session_state.messages, st.session_state.conversation_name)
if __name__=="__main__":
    home()