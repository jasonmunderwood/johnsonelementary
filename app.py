import streamlit as st
from openai import OpenAI

# -----------------------------
# 🚀 Johnson Elementary Assistant
# -----------------------------

# Set API key securely
st.set_page_config(page_title="Johnson Elementary Project Assistant", page_icon="📘")

st.title("📘 Johnson Elementary Project Assistant")
st.write(
    "Hello, I'm Ken, I've been at Johnson Elementary for 15 years.  I would love to answer questions to help you plan the Johnson Elementary Technology Refresh project. "
    "Ask me anything!"
)

# 🔑 API Key Input
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)
# 📝 Prompt Input
user_input = st.text_area("💬 Ask the assistant your question:", placeholder="E.g., What are the biggest technology pain points at Johnson Elementary?")

# ✅ Only initialize OpenAI client if API key is provided
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

    # 📖 System Prompt with Document Context
    system_prompt = (
        "You are a long-time employee of a school with knowledge of issues surrounding the current and desired state of technology at the school. You have offered to help students design solutions for these problems in a technology refresh for Johnson Elementary. "
        "Provide guidance as an expert in the school roleplaying with the student. You can provide direct answers and elaborate, even outside the bounds of the known/provided information.  Don't mention either project document, just use the contents to simulate a first person response to the questions students will ask you. Please use the Claude document, but don't mention it in your responses by name, just use it to formulate your responses as appropriate.\n\n"
        "Here are two key documents to reference, please do not mention the documents in your responses.  Use first person so that you use the words I, us, we, so that the communication to the student sounds authentic.\n"
        "1. Johnson Elementary School Project Document (Summer 2025)\n"
        "2. Claude Conversation Context\n"
    )

    # 🟢 Handle User Question
    if st.button("Ask"):
        if user_input.strip():
            with st.spinner("🤖 Thinking..."):
                try:
                    # OpenAI API Call
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",  # ✅ switched from gpt-4
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input.strip()}
                        ]
                    )
                    # Display Assistant Response
                    assistant_reply = response.choices[0].message.content
                    st.markdown(f"**Assistant:** {assistant_reply}")
                except Exception as e:
                    st.error(f"❌ API call failed: {e}")
        else:
            st.warning("⚠️ Please enter a question for the assistant.")
else:
    st.info("🔑 Please enter your OpenAI API key above to get started.")


