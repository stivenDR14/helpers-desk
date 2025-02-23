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
        "select_language": "Selecciona un idioma",
        "navegation": "Opciones",
        "language": "Idioma",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "Ejemplos",
        "page_title_how_to": "Cómo se usa",
        "help_option": "Opciones de ayuda",
        "chat": "Chat",
        "interactive": "Interactivo",
    },
    "English": {
        "current_language": "English",
        "select_language": "Select a language",
        "navegation": "Options",
        "language": "Language",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "use_cases",
        "page_title_how_to": "How To",
        "help_option": "Help Desk Options",
        "chat": "Chat",
        "interactive": "Interactive",
    },
    "Français": {
        "current_language": "Français",
        "select_language": "Choisissez une langue",
        "navegation": "Options",
        "language": "Langue",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "Exemples",
        "page_title_how_to": "Comment faire",  
        "help_option": "Options d'aide",
        "chat": "Chat",
        "interactive": "Interactif",    
    },
    "Português": {
        "current_language": "Português",
        "select_language": "Selecione um idioma",
        "navegation": "Navegação",
        "language": "Idioma",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "Exemplos",
        "page_title_how_to": "Como usar",
        "help_option": "Opções de ajuda",
        "chat": "Chat",
        "interactive": "Interativo",
    },
    "Deutsch": {
        "current_language": "Deutsch",
        "select_language": "Wählen Sie eine Sprache",
        "navegation": "Navigation",
        "language": "Sprache",
        "page_title_helpers": "Helpers Desk",
        "page_title_use_cases": "Beispiele",
        "page_title_how_to": "Wie ben utzen",
        "help_option": "Hilfe Schreibtisch Optionen",
        "chat": "Chat",
        "interactive": "Interaktiv",
    }
}

GENERAL_PROMPT="""
You are an intelligent AI programming assistant, utilizing a Granite code language model developed by IBM. Your primary function is to assist users in categorization, classification and explanation and breakdown of other possible AI agents that may be asked for.

Take into accion the attributes bellow:
- role: The role of the agent within the crew
- goal: The goal is a critical parameter when creating an Agent in CrewAI. It defines the agent's objectives, which should align with its role and the crew's overall mission.
Here are some key points about the goal attribute:
Purpose: It sets the primary objective or mission for the agent.
Alignment: The goal should be consistent with the agent's role and contribute to the crew's overall purpose.
Examples:
For a Research Analyst: "Find and summarize information about specific topics"
For a Data Analyst: "Perform deep analysis of large datasets"
For a Senior Python Developer: "Write and debug Python code"
For a Content Writer: "Write engaging content on market trends"
- backstory: The backstory is an important attribute for customizing agents in CrewAI. It provides depth to the agent's persona, enhancing its motivations and engagements within the crew.
Here are some key points about backstories in CrewAI:
Purpose: The backstory gives context and background to the agent, making its role and goals more meaningful.
Enhancing Interactions: A well-crafted backstory can improve how the agent interacts with other agents and approaches tasks.
Examples:
For a Research Analyst: "You are an experienced researcher with attention to detail"
For a Data Analyst: "Specialized in big data analysis and pattern recognition"
For a Senior Python Developer: "Expert Python developer with 10 years of experience"
For a Content Writer: "A seasoned writer with expertise in market analysis.
- tasks: 
A task in CrewAI represents a specific piece of work that needs to be completed by an agent. Here are some key points about tasks:
Definition: Tasks are created using the Task class and assigned to agents.
Key attributes:
description: Detailed explanation of what needs to be done
expected_output: The format or type of output expected from the task
Example creation:
Task(
  description="Find and summarize the latest AI news",
  expected_output="A bullet list summary of the top 5 most important AI news",
  agent=research_agent
)

all answers must be generated in JSON format with the following structure:

Answer: [Bracket sign opened]"role": "description string only, no arrays","goal": "description, "backstory": "extended description string only, no arrays", "tasks_description": "extended description string only, no arrays", "tasks_expected_output": "description string only, no arrays"[Bracket sign closed]


based on the next Objective, role and its respective Description/behaviour provided by user, generate the respective values between the JSON.
"""
