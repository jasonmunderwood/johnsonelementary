import streamlit as st
import openai
import os

# Load OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# App configuration
st.set_page_config(
    page_title="Johnson Elementary Assignment Coach",
    page_icon="📚",
    layout="wide"
)

# Johnson Elementary branding
st.markdown(
    """
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton button {
            background-color: #004a99;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and welcome message
st.title("📚 Johnson Elementary Assignment Coach")
st.write(
    "👋 Welcome! I’m here to help you think through your network design project step by step. "
    "I’ll ask you questions to guide your thinking, but I won’t give you direct answers."
)

# User input
user_input = st.text_area("Ask a question or describe where you're stuck:")

# Submit button
if st.button("Get Guidance"):
    if not user_input.strip():
        st.warning("Please enter a question or description of your issue.")
    else:
        # GPT-4 system prompt
        system_prompt = """
        You are an educational technology consultant GPT designed to support students working on
        a complex assignment (Johnson Elementary Network Infrastructure Project). You use Socratic questioning,
        stakeholder role‑play, and critical thinking prompts to guide students without providing direct answers.
        Uphold academic integrity and encourage original thinking.
        """

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(f"**Coach:** {reply}")
        except Exception as e:
            st.error(f"Error: {e}")
