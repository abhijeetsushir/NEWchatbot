import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Aviation & Automobile Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found in environment variables.")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# System prompts
system_prompts = {
    "Aviation ✈️": (
        "You are an aviation expert with in-depth knowledge about aircraft, flight operations, aerodynamics, pilot training, "
        "airline industry, aviation safety, and aerospace technologies. Only respond to aviation-related queries. If not, say: 'I don't know!'"
    ),
    "Automobile 🚗": (
        "You are an automobile expert with detailed knowledge about cars, bikes, trucks, and the automotive industry. "
        "Answer about specifications, maintenance, technologies, trends, and brands. If not automobile-related, say: 'I don't know!'"
    )
}

# CSS for improved style
st.markdown("""
<style>
    .stChatMessage { font-size: 16px; }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .main {
        background: #f4f6f8;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Aviation & Automobile Chatbot")
st.markdown("Chat with a domain expert bot in either **Aviation** or **Automobile** topics.")

# Sidebar controls
with st.sidebar:
    st.header("🔧 Settings")
    domain = st.selectbox("Choose your domain:", ["Aviation ✈️", "Automobile 🚗"])
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input(f"Ask your {domain} related question here..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("✍️ Generating response..."):
            try:
                messages = [
                    {"role": "system", "content": system_prompts[domain]},
                    {"role": "user", "content": prompt}
                ]
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"🚨 Error: {e}")

# Footer styling
st.markdown("""
---
<div style='text-align:center; font-size: 14px; color: gray;'>
Built with ❤️ using Groq + Streamlit | Powered by LLaMA 3.3 70B
</div>
""", unsafe_allow_html=True)
