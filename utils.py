import streamlit as st

def set_language(language):
    if "language" not in st.session_state:
        st.session_state.language = "English"
    st.session_state.language = language
    st.rerun()

def render_sidebar(current_page):
    with st.sidebar:

        st.title(TRANSLATIONS[st.session_state.language]["navegation"])
        if st.button(("✅ " if current_page == "home" else "") + TRANSLATIONS[st.session_state.language]["page_title_helpers"]+" 👾"):
            st.switch_page("app.py")
        if st.button(("✅ " if current_page == "how_to" else "") + TRANSLATIONS[st.session_state.language]["page_title_how_to"]+" 🤔"):
            st.switch_page("pages/how_to.py")
        if st.button(("✅ " if current_page == "use_cases" else "") + TRANSLATIONS[st.session_state.language]["page_title_use_cases"]+" ☑️"):
            st.switch_page("pages/use_cases.py")
        
        
        st.title(TRANSLATIONS[st.session_state.language]["language"])
        if st.button(("✅ " if st.session_state.language == "Español" else "") + TRANSLATIONS["Español"]["current_language"]):
            set_language("Español")
        if st.button(("✅ " if st.session_state.language == "English" else "") + TRANSLATIONS["English"]["current_language"]):
            set_language("English")
        if st.button(("✅ " if st.session_state.language == "Français" else "") + TRANSLATIONS["Français"]["current_language"]):
            set_language("Français")
        if st.button(("✅ " if st.session_state.language == "Deutsch" else "") + TRANSLATIONS["Deutsch"]["current_language"]):
            set_language("Deutsch")
        if st.button(("✅ " if st.session_state.language == "Português" else "") + TRANSLATIONS["Português"]["current_language"]):
            set_language("Português")
            

MAP_ROUTES = {
    "home": "home",
    "how_to": "how_to",
    "use_cases": "use_cases",
}

TRANSLATIONS = {
    "Español": {
        "current_language": "Español",
        "select_language": "Select a language for IA answer you",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "QA Help Desk CX",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",
    },
    "English": {
        "current_language": "English",
        "select_language": "Select a language for IA answer you",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "QA Help Desk CX",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",
    },
    "Français": {
        "current_language": "Français",
        "select_language": "Select a language for IA answer you",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "QA Help Desk CX",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",   
    },
    "Português": {
        "current_language": "Português",
        
        "select_language": "Select a language for IA answer you",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "QA Help Desk CX",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",
    },
    "Deutsch": {
        "current_language": "Deutsch",
        
        "select_language": "Select a language for IA answer you",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "QA Help Desk CX",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",
    }
}

