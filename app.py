import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Chat With PDF", page_icon="📄")
st.header("Chat With PDF")

# Create a session state object
session_state = st.session_state
if not hasattr(session_state, "database_created"):
    session_state.database_created = False

data_folder = "data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Upload multiple files
uploaded_files = st.file_uploader("Upload PDF files", type='pdf', accept_multiple_files=True)

if uploaded_files is not None and uploaded_files != []:
    for uploaded_file in uploaded_files:
        # Get the file name
        file_name = os.path.join(data_folder, uploaded_file.name)
        
        # Save the file locally
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
    # Run create_db.py after files are uploaded only if the database has not been created yet
    if not session_state.database_created:
        subprocess.run(["python", "create_database.py"])
        session_state.database_created = True  # Set the flag to True after database creation

# Run query_data.py with command-line arguments
query_text = st.text_input("Ask Question From PDF:")
            
if st.button("Submit"):
    # Run query_data.py with query_text as argument and capture output
    process = subprocess.Popen(["python", "query_data.py", query_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # Check if there's any output
    if stdout:
        st.write(stdout)
