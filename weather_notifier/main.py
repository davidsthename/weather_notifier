import streamlit as st  # Imports the streamlit framework library
from ui import show_app  # Imports the main UI function from ui.py

# Configure the browser tab title and icon
st.set_page_config(
    page_title="Weather Alert System",
    page_icon="Cloud",  # the favicon
    layout="centered"
)
show_app()
