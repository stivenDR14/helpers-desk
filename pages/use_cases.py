
import streamlit as st
from utils import MAP_ROUTES, TRANSLATIONS, render_sidebar

if "language" not in st.session_state:
    st.session_state.language = "English"

st.set_page_config(
    page_title=TRANSLATIONS[st.session_state.language]["page_title_use_cases"],
    page_icon="☑️",
    layout="wide"
)

def roadmap_for_marketing_event():
    st.session_state.roles = ["Marketing Manager", "Content Creator", "Adversiting designer", "Social media manager", "Event planner"]
    st.session_state.descriptions = [
        "The marketing manager is responsible for the overall marketing strategy of the event. This is the person who acts as a solver too (Responsible for solving strategic challenges and marketing problems and Makes critical decisions about campaign effectiveness).",
        "The content creator is responsible for creating the content that will be used in the event. This is the person who acts as an explorer too (Discovers new content opportunities and Researches trends and audience preferences).",
        "The adversiting designer is responsible for creating the ads that will be used to promote the event. This is the person who acts as analyst too (Analyzes design effectiveness and studies market trends and visual impact).",
        "The social media manager is responsible for managing the social media accounts of the event. this is the person who acts as a motiator too (engages with audience and builds community and encourages interaction).",
        "The event planner is responsible for planning the event. This is the person who acts as a team manager too (Coordinates with multiple stakeholders and manages resources and timeline)."
    ]
    st.session_state.report_formats = ["PDF"]
    st.session_state.objective = "Organize a marketing event for the launch of a new product. This product is a new software that helps sport enthusiasts to track their progress and improve their performance. Our budget is $10,000 and we want to reach between 1000 and 10000 people."
    st.switch_page("app.py")

def customer_support_qa_validation():
    st.session_state.roles = ["QA Manager", "Customer Support Manager", "Conversation analyst"]

def account_waste_and_incomes_data_entry():
    st.session_state.roles = ["Accountant","Financial Analyst"]
    st.session_state.descriptions = [
        "The accountant is responsible for managing the financial records provided. This person is clear about how all types of expenses and income should be categorized, distributed and named. On this way, each record must be categorized with the right name and description, without abbreviations or acronyms, if is an income or an expense, if is done by credit card, debid card, digital wallet or cash, if is a payment, debt, borrowing, loan, investment, if is a purchase or sale, if is a donations, salary, bonus, etc.",
        "The financial analyst is responsible for analyzing the financial data provided. This is the person who acts as an clasiffier, breaking down the concept of the income/expense in all the attributes/categories given by the accountant."
    ]
    st.session_state.report_formats = ["Table"]
    st.session_state.objective = "Generic data and description will be provided, this data must be structured and classified in a defined structure of columns. data: 'Today I bougth to the provider X 10 units of product Y for $1000. I paid with company cash.'"
    st.switch_page("app.py")
        

def sales_mockup_generation():
    st.session_state.roles = ["Sales Manager", "Sales Representative", "Sales Analyst", "Sales Support", "Sales Engineer"]

def render_use_cases():
    st.title("Use cases for applying in the helpers desk")
    st.write("Here are different use cases for the helpers desk:")
    if st.button("Roadmap for marketing event"):
        roadmap_for_marketing_event()
    if st.button("Generating tasks for payment gateway development"):
        st.switch_page("app.py")
    if st.button("Customer support QA validation"):
        customer_support_qa_validation()
        st.switch_page("app.py")
    if st.button("Product release checklist"):
        st.switch_page("app.py")
    if st.button("User onboarding checklist"):
        
        st.switch_page("app.py")
    if st.button("Account waste and incomes data entry"):
        account_waste_and_incomes_data_entry()
        st.switch_page("app.py")
    if st.button("Financial calculations of future values and interests"):
        st.switch_page("app.py")
    if st.button("Sales mockup generation"):
        sales_mockup_generation()
        st.switch_page("app.py")


def main():
    render_sidebar(MAP_ROUTES["use_cases"])
    render_use_cases()

if __name__ == "__main__":
    main()