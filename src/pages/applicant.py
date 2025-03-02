import streamlit as st
from utils.openai_api import get_ai_question  # Function to generate AI questions dynamically
from utils.recruiter_assistant import send_message

def show_page():
    st.title("Applicant Interface")

    # Step 1: Collect Applicant Information
    st.subheader("1️⃣ Enter Your Information")
    
    if "applicant_info" not in st.session_state:
        st.session_state["applicant_info"] = {"name": "", "email": "", "phone": ""}

    st.session_state["applicant_info"]["name"] = st.text_input("Full Name", value=st.session_state["applicant_info"]["name"])
    st.session_state["applicant_info"]["email"] = st.text_input("Email", value=st.session_state["applicant_info"]["email"])
    st.session_state["applicant_info"]["phone"] = st.text_input("Phone Number", value=st.session_state["applicant_info"]["phone"])

    # Step 2: Start Interview
    st.subheader("2️⃣ Start Your Interview")
    if st.button("Start Interview"):
        st.session_state["interview_started"] = True  # Mark interview as started

    # Step 3: Question / Response Conversation
    if "interview_started" in st.session_state:
        st.subheader("3️⃣ Interview Questions")

        if "applicant_responses" not in st.session_state:
            st.session_state["applicant_responses"] = []

        # Dynamic AI-Generated Questions
        if "interview_mode" in st.session_state and st.session_state["interview_mode"] == "Conversational":
            if st.button("Get Next AI Question"):
                new_question = get_ai_question()
                st.session_state["applicant_responses"].append({"question": new_question, "answer": ""})

        # Display and capture responses
        for idx, qa in enumerate(st.session_state["applicant_responses"]):
            st.write(f"**Q{idx+1}: {qa['question']}**")
            st.session_state["applicant_responses"][idx]["answer"] = st.text_area(
                f"Your Response {idx+1}",
                value=qa["answer"],
                key=f"response_{idx}"
            )

        st.divider()

        # Step 4: Final Comments
        st.subheader("4️⃣ Final Comments")
        final_comment = st.text_area("Do you have any final comments for the recruiter?")
        st.session_state["final_comment"] = final_comment

        # Step 5: Submit Response
        if st.button("Submit Interview"):
            st.session_state["interview_complete"] = True
            st.success("Your responses have been recorded! ✅")

            # Store all responses for recruiter review
            applicant_data = {
                "applicant_info": st.session_state["applicant_info"],
                "responses": st.session_state["applicant_responses"],
                "final_comment": final_comment
            }

            # Save data (Future: Store in DB)
            st.session_state["submitted_applicant_data"] = applicant_data
