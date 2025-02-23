from services import orchestate_graph_agents_evaluating
import streamlit as st
from utils import MAP_ROUTES, TRANSLATIONS, render_sidebar

if "language" not in st.session_state:
    st.session_state.language = "English"
if "objective" not in st.session_state:
    st.session_state.objective = ""
if "guide_input" not in st.session_state:
    st.session_state.guide_input = ""
st.set_page_config(
    page_title=TRANSLATIONS[st.session_state.language]["page_title_how_to"],
    page_icon="🤔",
    layout="wide"
)

def render_how_to():
    st.title("QA Help Desk CX")
    st.write("Set in the first Text Area the QA Guide you want to use to evaluate the conversations/transcriptions, and in the second Text Area the conversations/transcriptions you want to evaluate.")
    st.text_area("Guide", value=st.session_state.guide_input)
    st.text_area("Text", value=st.session_state.objective)
    if st.button("Evaluate"):
        average=orchestate_graph_agents_evaluating(st.session_state.guide_input, st.session_state.objective)
        st.write(f"Average between 0-4: {average}")


def main():
    render_sidebar(MAP_ROUTES["how_to"])
    render_how_to()

if __name__ == "__main__":
    main()