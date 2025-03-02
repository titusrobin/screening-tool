import streamlit as st
from utils.openai_api import extract_evaluation_categories

def show_page():
    st.title("Recruiter Interface")

    mode = st.radio("Select Interview Mode:", ["Conversational", "Question/Answer"])
    st.divider()

    evaluation_categories = None  # Store extracted categories

    if mode == "Conversational":
        st.subheader("Conversational Mode")

        # Job Description Input
        job_description = st.text_area(
            "Enter job description or relevant context to guide AI:",
            placeholder="Describe the job role, required skills, and expectations..."
        )

        # Button to Trigger API Call
        if st.button("Process Job Description"):
            if job_description:
                with st.spinner("Analyzing Job Description... ⏳"):
                    evaluation_categories = extract_evaluation_categories(job_description)  # OpenAI API Call
                
                st.success("Evaluation categories extracted! ✅")

                # Store in session state to persist data
                st.session_state["evaluation_categories"] = evaluation_categories
            else:
                st.warning("Please enter a job description before submitting.")

    # Editable Multi-Select Tags for Categories
    if "evaluation_categories" in st.session_state:
        st.subheader("🔍 AI-Generated Evaluation Categories")
        
        # Multi-Select Input (Recruiters Can Modify)
        selected_categories = st.multiselect(
            "Modify Categories:", 
            options=st.session_state["evaluation_categories"],  # AI suggestions
            default=st.session_state["evaluation_categories"]   # Preselected values
        )

        # Save modified categories back to session state
        st.session_state["evaluation_categories"] = selected_categories

    st.divider()

    if st.button("Submit Interview Setup"):
        st.success("Interview setup submitted! ✅")
