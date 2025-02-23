import streamlit as st
from utils import MAP_ROUTES, TRANSLATIONS, render_sidebar

if "language" not in st.session_state:
    st.session_state.language = "English"

st.set_page_config(
    page_title=TRANSLATIONS[st.session_state.language]["page_title_how_to"],
    page_icon="🤔",
    layout="wide"
)

def render_how_to():
    st.title("How to Use It")
    st.write("Instructions on how to use the application will be provided here.")

def main():
    render_sidebar(MAP_ROUTES["how_to"])
    render_how_to()

if __name__ == "__main__":
    main()