"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""
import streamlit as st

# Set wide display, if not done before
try:
    st.set_page_config(
        layout="wide",
        page_title="Industry Sprint Workshop",
        page_icon="🚚",
        initial_sidebar_state="expanded",)
except:
    pass

# Hide the menu and the footer
# Add header {visibility: hidden;}
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title('Industry Sprint Workshop')

with st.sidebar:
    # Upload files
    st.header('Sidebar')


# Display the session state
st.write('Session state: ',st.session_state)