from services import orchestrate_graph_agents
import streamlit as st
from utils import MAP_ROUTES, TRANSLATIONS, render_sidebar

if "language" not in st.session_state:
    st.session_state.language = "English"
if 'submit_button_clicked' not in st.session_state:
    st.session_state.submit_button_clicked = False

if "roles" not in st.session_state:
    st.session_state.roles = []
if "descriptions" not in st.session_state:
    st.session_state.descriptions = []
if "report_formats" not in st.session_state:
    st.session_state.report_formats = []
if "objective" not in st.session_state:
    st.session_state.objective = ""

st.set_page_config(
    page_title=TRANSLATIONS[st.session_state.language]["page_title_helpers"],
    page_icon="👾",
    layout="wide"
)



def render_head():
    # Add role dynamically
    def add_role():
        if len(st.session_state.roles) < 5:
            st.session_state.roles= st.session_state.roles + [""]
            st.session_state.descriptions = st.session_state.descriptions + [""]

    # Remove role dynamically
    def remove_last():
        st.session_state.roles.pop()
        st.session_state.descriptions.pop()

    # Title
    st.title("Help desk configuration")

    st.session_state.objective = st.text_area("Describe the objective you want to achieve with the other roles:", st.session_state.objective)

    # Role Selection UI
    st.header("Set Up to 5 Roles")

    for i, role in enumerate(st.session_state.roles):
        st.session_state.roles[i] = st.text_input(f"Role {i+1}", value=role, key=f"role_{i}")
        st.session_state.descriptions[i]=st.text_area(f"Detailed description of the role behaviour", key=f"desc_{i}", value=st.session_state.descriptions[i])

    # Plus button for adding roles
    if len(st.session_state.roles) < 5:
        if st.button("+ Add Role"):
            add_role()
            st.rerun()
    if len(st.session_state.roles) > 0:
        if st.button("- Remove Last Role"):
            remove_last()
            st.rerun()   


    # Report Format Selection
    report_options = ["Table", "PDF", 'Sumary of the meeting']
    st.session_state.report_formats = st.multiselect("Select report formats:", report_options, default= st.session_state.report_formats)

    # Submit Button
    if st.button("Generate Solution"):
        st.write("### Configuration Summary")
        st.write(f"**Objective:** {st.session_state.objective}")
        st.write("**Roles & Descriptions:**")   
        for role in st.session_state.roles:
            st.write(f"- **{role}:** {st.session_state.descriptions[st.session_state.roles.index(role)]}")
        if len(st.session_state.report_formats) > 0:
            st.write("**Report Formats:**", ", ".join(st.session_state.report_formats))
        st.session_state.submit_button_clicked = True
        result = orchestrate_graph_agents(st.session_state.roles, st.session_state.descriptions, st.session_state.report_formats, st.session_state.objective, st.session_state.language)
        st.markdown(result, unsafe_allow_html=True,)

 

def render_chat():
    st.write("### ")
    st.title("Let's see how your roles are thinking about")
    st.write("At the end of ther 'meeting' you will see a summary of the meeting, or the report you selected")

    st.progress(0, text="")
    conversation = [
        {"agent": "assistant", "message": "Let's plan the roadmap for the landing page project."},
        {"agent": "Manager", "message": "We need to define the goals and timeline first."},
        {"agent": "Operator1", "message": "I can start working on the wireframes."},
        {"agent": "Operator2", "message": "I'll handle the backend integration."},
        {"agent": "assistant", "message": "Great! Let's set a deadline for the first draft."},
    ]

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = conversation.copy()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["agent"]):
            st.markdown(message["message"])

    # React to user input
    if prompt := st.chat_input("They have a question for you, answer it!"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"agent": "user", "message": prompt})

        response = f"Echo: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"agent": "assistant", "message": response})



def main():
    render_sidebar(MAP_ROUTES["home"])
    render_head()
    if st.session_state.submit_button_clicked:
        render_chat()

if __name__ == "__main__":
    main()