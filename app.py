import streamlit as st
from openai import OpenAI
import json
import os

# 🛠 Use Project API key + Project ID
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai_project = st.secrets["OPENAI_PROJECT"]

client = OpenAI(
    api_key=openai_api_key,
    project=openai_project
)

# -----------------------------
# 🚀 Johnson Elementary Assistant
# -----------------------------

st.set_page_config(page_title="Johnson Elementary Project Assistant", page_icon="📘")
st.title("📘 Johnson Elementary Project Assistant")
st.write(
    "Hello, I'm Ken. I've been at Johnson Elementary for 15 years. "
    "I would love to answer questions to help you plan the Johnson Elementary Technology Refresh project. "
    "Ask me anything!"
)

# ✅ Ask for user name/email ONCE per session
if "user_id" not in st.session_state:
    user_id_input = st.text_input(
        "👤 Enter your name or email to start:",
        placeholder="e.g., alice@niu.edu"
    )
    if user_id_input:
        st.session_state.user_id = user_id_input
        st.session_state.messages = []  # initialize messages
else:
    user_id = st.session_state.user_id

    # Sanitize user_id for safe file names
    safe_user_id = user_id.replace("@", "_at_").replace(".", "_dot_").replace(" ", "_")
    history_file = f"history_{safe_user_id}.json"

    # ✅ Load user history if it exists
    if "messages" not in st.session_state:
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                st.session_state.messages = json.load(f)
        else:
            st.session_state.messages = [
                {"role": "system", "content": (
                    "You are a long-time employee of a school with knowledge of issues surrounding the current and desired state of technology at the school. "
                    "You have offered to help students design solutions for these problems in a technology refresh for Johnson Elementary. "
                    "Provide guidance as an expert in the school roleplaying with the student. You can provide direct answers and elaborate, even outside the bounds of the known/provided information. "
                    "Don't mention either project document, just use the contents to simulate a first person response to the questions students will ask you. "
                    "Please use the Claude document, but don't mention it in your responses by name, just use it to formulate your responses as appropriate. "
                    "If there are questions about specific technologies not referenced in the documents, your responses should describe technologies that are old, outdated, and need replacing. "
                    "Technology use and adoption at Johnson Elementary is far behind most similar schools, so answers should reflect that. "
                    "For example, they have never used 1-1 computing with Chromebooks, they do not have an LMS or SIS, students do not have email addresses, etc."
                )}
            ]

    # 📝 Display chat history
    for msg in st.session_state.messages[1:]:  # Skip system prompt
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Ken:** {msg['content']}")

    # 💬 Input box for user message
    user_input = st.chat_input("Ask Ken something...")

    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message immediately
        st.markdown(f"**You:** {user_input}")

        with st.spinner("🤖 Ken is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                assistant_reply = response.choices[0].message.content

                # Append assistant reply
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

                # Display assistant reply
                st.markdown(f"**Ken:** {assistant_reply}")

                # Save updated history
                with open(history_file, "w") as f:
                    json.dump(st.session_state.messages, f)

            except Exception as e:
                st.error(f"❌ API call failed: {e}")

    # 🔄 Reset conversation
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = st.session_state.messages[:1]  # Keep system prompt
        # Save reset state
        with open(history_file, "w") as f:
            json.dump(st.session_state.messages, f)
        st.experimental_rerun()
