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

# ✅ Load Ken's system prompt from prompt.txt
if os.path.exists("prompt.txt"):
    with open("prompt.txt", "r") as f:
        system_prompt = f.read()
else:
    st.error("❌ Missing 'prompt.txt'. Please add the file with Ken's system prompt.")
    st.stop()

# ✅ Ask for user name/email ONCE per session
if "user_id" not in st.session_state:
    user_id_input = st.text_input(
        "👤 Enter your name or email to start:",
        placeholder="e.g., alice@niu.edu"
    )
    if user_id_input:
        st.session_state.user_id = user_id_input
        st.session_state.messages = []
        user_id = st.session_state.user_id  # Set user_id immediately
    else:
        st.stop()  # 🛑 Stop here until user provides email
else:
    user_id = st.session_state.user_id

# Sanitize user_id for safe file names
safe_user_id = user_id.replace("@", "_at_").replace(".", "_dot_").replace(" ", "_")
history_file = f"history_{safe_user_id}.json"

# ✅ Load user history if it exists
if "messages" not in st.session_state or not st.session_state.messages:
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]

# 📝 Display chat history
chat_transcript = ""  # To store full conversation text
for msg in st.session_state.messages[1:]:  # Skip system prompt
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
        chat_transcript += f"You: {msg['content']}\n"
    elif msg["role"] == "assistant":
        st.markdown(f"**Ken:** {msg['content']}")
        chat_transcript += f"Ken: {msg['content']}\n"

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

# 🔄 Reset + 📋 Copy Conversation Buttons Side by Side
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]
        # Save reset state
        with open(history_file, "w") as f:
            json.dump(st.session_state.messages, f)
        st.rerun()

with col2:
    if st.button("📋 Copy Conversation"):
        st.text_area("📋 Conversation Transcript:", chat_transcript, height=300)
        st.markdown("""
            <script>
            navigator.clipboard.writeText(`""" + chat_transcript.replace('`', '\`') + """`);
            </script>
        """, unsafe_allow_html=True)
        st.success("✅ Conversation copied to clipboard!")
