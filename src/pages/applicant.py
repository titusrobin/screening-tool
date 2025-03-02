import streamlit as st
from utils.recruiter_assistant import send_message


def show_page():

    st.title("Applicant Interface")
    
    if 'new_response' not in st.session_state:
        st.session_state.new_response = ""
        
    try:
        ASSISTANT_ID = st.session_state['assistant_id']
        THREAD_ID = st.session_state['thread_id']
    except:
        st.subheader("Warning: AI Assistant has not been initialized yet, go to recruiter tab and submit a job description.")

    # Step 1: Collect Applicant Information
    st.subheader("1️⃣ Enter Your Information")
    
    if "applicant_info" not in st.session_state:
        st.session_state["applicant_info"] = {"name": "", "email": "", "phone": ""}

    st.session_state["applicant_info"]["name"] = st.text_input("Full Name", value=st.session_state["applicant_info"]["name"])
    st.session_state["applicant_info"]["email"] = st.text_input("Email", value=st.session_state["applicant_info"]["email"])
    st.session_state["applicant_info"]["phone"] = st.text_input("Phone Number", value=st.session_state["applicant_info"]["phone"])

    # Step 2: Start Interview
    st.subheader("2️⃣ Start Your Interview")

    st.button("Start Interview", on_click=start_interview)

    st.divider()

    # Step 3: Display Conversation
    st.subheader("3️⃣ Interview Conversation")

    show_chat()

    st.text_input("Your Response", key="user_input")

    st.button("Send Response", on_click=submit_response)
            
    st.divider()

def submit_response():
    if st.session_state.user_input.strip():
        # Add user message to chat history
        st.session_state["chat_history"].append({"role": "user", "content": st.session_state.user_input})

        with st.spinner("Waiting for AI response..."):
            ai_response = send_message(st.session_state['thread_id'], st.session_state['assistant_id'], st.session_state.user_input)
        
        # Store AI response
        st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})

        st.session_state.user_input = ""

def show_chat():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**AI:** {chat['content']}")

def start_interview():
    with st.spinner("Initializing AI Screening..."):
        first_response = send_message(st.session_state['thread_id'], st.session_state['assistant_id'], "start screening 3")
    st.session_state["chat_history"].append({"role": "assistant", "content": first_response})
