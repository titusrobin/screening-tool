import streamlit as st
from pages import recruiter  # Import Tab 1

# Set Streamlit Page Config
st.set_page_config(page_title="Applicant Screening", layout="wide")

# Sidebar for Navigation
st.sidebar.title("Navigation")
tab_selection = st.sidebar.radio("Go to:", ["Recruiter Interface", "Applicant Interface", "Recruiter Dashboard"])

# Route to the correct page
if tab_selection == "Recruiter Interface":
    recruiter.show_page()  # Call the function from recruiter.py
elif tab_selection == "Applicant Interface":
    st.write("Applicant Interface (Tab 2) - Coming Soon...")
elif tab_selection == "Recruiter Dashboard":
    st.write("Recruiter Dashboard (Tab 3) - Coming Soon...")
