
import streamlit as st
from groq import Groq

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Groq AI Chatbox",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Groq AI Chatbox")

# -------------------------------------------------
# Sidebar - Settings
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # Groq API Key
    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="Enter your Groq API key"
    )

    st.markdown(
        "Get your free API key from "
        "[Groq Console](https://console.groq.com/keys)"
    )

    # Model selection
    MODEL = st.selectbox(
        "🤖 Select Model",
        [
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    # Temperature control
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Lower values give more focused answers. Higher values make responses more creative."
    )

    st.write(f"Current temperature: **{temperature:.1f}**")

    # Max tokens
    max_tokens = st.slider(
        "📝 Maximum Tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256
    )

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful, concise assistant."
            }
        ]
        st.rerun()


# -------------------------------------------------
# Initialize Conversation History
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, concise assistant."
        }
    ]


# -------------------------------------------------
# Display Previous Messages
# -------------------------------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------------------------------
# Chat Input
# -------------------------------------------------
user_text = st.chat_input("Type your message here...")


# -------------------------------------------------
# Process User Message
# -------------------------------------------------
if user_text:

    # Check API key
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()

    # Display user message
    st.chat_message("user").markdown(user_text)

    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_text
        }
    )

    try:
        # Create Groq client
        client = Groq(api_key=api_key)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                ai_text = response.choices[0].message.content

                st.markdown(ai_text)

        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_text
            }
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
