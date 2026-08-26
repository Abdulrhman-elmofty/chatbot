import streamlit as st
from groq import Groq
st.title("My chat bot")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown("---")

audio = st.audio_input("Record your message")

prompt = st.chat_input("write your message")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt:
    st.session_state.messages.append({"role" : "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                messages = [{"role" : "system", "content":"you are a helpful assistant"}]
                for msg in st.session_state.messages:
                    messages.append({"role": msg['role'], "content": msg['content']})
                response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                max_tokens=500,
                temperature=0.7
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = e
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})