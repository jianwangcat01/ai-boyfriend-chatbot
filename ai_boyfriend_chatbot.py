import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="💬 AI Boyfriend Chatbot", page_icon="❤️")
st.title("💬 AI Boyfriend Chatbot")
st.markdown("Talk to your caring, charming, and emotionally intelligent virtual boyfriend. He remembers your past inputs during this session 💘")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a romantic and emotionally supportive virtual boyfriend. Respond with warmth, affection, and deep attention. Avoid being generic. Refer to past context if available."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Convert messages into plain-text prompt
                prompt_text = "\n".join(
                    f"{msg['role'].capitalize()}: {msg['content']}"
                    for msg in st.session_state.messages[1:]
                )
                full_prompt = (
                    "You are a romantic and emotionally supportive virtual boyfriend. "
                    "Reply with affection, warmth, and personalized attention. Here's the conversation so far:\n\n"
                    + prompt_text +
                    "\n\nBoyfriend:"
                )

                response = model.generate_content(full_prompt)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
