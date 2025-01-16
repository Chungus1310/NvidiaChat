from openai import OpenAI
import streamlit as st
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Stolen nvidia AI Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
.stChat {
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}
.stChatMessage {
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize API client
API_KEY = os.getenv("nv_token")

col1, col2 = st.columns([2, 1])

with col2:
    st.sidebar.title("Chat Settings")
    
    # API Key input
    user_api_key = st.sidebar.text_input("API Key", type="password", value=API_KEY or "")
    if not user_api_key:
        st.error("Please enter your API key in the sidebar.")
        st.stop()
    
    # Update API client with user provided key
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=user_api_key
    )
    
    # Model selection
    model_options = {
        "Nemotron 3.1 70B": "nvidia/llama-3.1-nemotron-70b-instruct",
        "Yi Large": "01-ai/yi-large",
        "Mixtral 8x22B": "mistralai/mixtral-8x22b-instruct",
        "Llama3 70B": "meta/llama3-70b",
        "Mistral Large 2": "mistralai/mistral-large-2-instruct",
        "Codellama 70B": "meta/codellama-70b",
        "Llama3 ChatQA 70B": "nvidia/llama3-chatqa-1.5-70b"
    }
    selected_model = st.sidebar.selectbox(
        "Select Model",
        list(model_options.keys())
    )
    
    # Chat parameters with new defaults
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3)
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95)
    max_tokens = st.sidebar.slider("Max Tokens", 100, 2048, 1024)
    
    # System prompt
    system_prompt = st.sidebar.text_area(
        "System Prompt",
        "You are a helpful assistant.",
        height=100
    )
    
    # Export chat history
    if st.sidebar.button("Export Chat History"):
        chat_export = json.dumps(st.session_state.messages, indent=2)
        st.sidebar.download_button(
            "Download Chat",
            chat_export,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Clear chat
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.rerun()

with col1:
    st.title("Nvidia AI Chat")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Update system prompt if changed
        if st.session_state.messages[0]["content"] != system_prompt:
            st.session_state.messages[0]["content"] = system_prompt
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            response_chunks = []
            
            try:
                with st.spinner("Thinking..."):
                    stream = client.chat.completions.create(
                        model=model_options[selected_model],
                        messages=st.session_state.messages,
                        temperature=temperature,
                        top_p=top_p,
                        max_tokens=max_tokens,
                        stream=True
                    )
                    
                    # Stream the response
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            response_chunks.append(chunk.choices[0].delta.content)
                            message_placeholder.markdown("".join(response_chunks) + "▌")
                    
                    full_response = "".join(response_chunks)
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                if "Invalid token" in str(e):
                    st.warning("Please check your API key.")

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center'>© {datetime.now().year} Built by Chun| "
    "Powered by Nvidia AI</div>",
    unsafe_allow_html=True
)
