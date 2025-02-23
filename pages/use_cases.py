
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
    
    st.session_state.objective = "Organize a marketing event for the launch of a new product. This product is a new software that helps sport enthusiasts to track their progress and improve their performance. Our budget is $10,000 and we want to reach between 1000 and 10000 people."
    st.switch_page("app.py")

def generating_tasks_for_payment_gateway_development():
    st.session_state.roles = ["Project Manager", "Software Developer", "Quality Assurance Engineer", "UX/UI Designer", "Technical Writer"]
    st.session_state.descriptions = [
        "The project manager is responsible for overseeing the development of the payment gateway. This is the person who acts as a planner too (Plans project milestones and deadlines and Coordinates team meetings and progress reports).",
        "The software developer is responsible for coding the payment gateway. This is the person who acts as a problem solver too (Troubleshoots code issues and Implements new features and updates).",
        "The quality assurance engineer is responsible for testing the payment gateway. This is the person who acts as a researcher too (Researches best testing practices and Identifies bugs and issues in the code).",
        "The UX/UI designer is responsible for designing the user interface of the payment gateway. This is the person who acts as a creative too (Creates wireframes and mockups and Designs user-friendly interfaces and experiences).",
        "The technical writer is responsible for creating documentation for the payment gateway. This is the person who acts as a communicator too (Writes user guides and manuals and Communicates technical information clearly and concisely)."
    ]
    
    st.session_state.objective = "Develop a payment gateway for an e-commerce platform. The gateway should support multiple payment methods, including credit cards, PayPal, and cryptocurrency. The project has a deadline of 3 months and a budget of $50,000."
    st.switch_page("app.py")

def product_release_checklist():
    st.session_state.roles = ["Product Manager", "Software Developer", "Quality Assurance Engineer", "Technical Writer", "Customer Support Specialist"]
    st.session_state.descriptions = [
        "The product manager is responsible for overseeing the release of the product. This is the person who acts as a planner too (Plans product milestones and deadlines and Coordinates team meetings and progress reports).",
        "The software developer is responsible for coding new features and updates for the product. This is the person who acts as a problem solver too (Troubleshoots code issues and Implements new features and updates).",
        "The quality assurance engineer is responsible for testing the product. This is the person who acts as a researcher too (Researches best testing practices and Identifies bugs and issues in the code).",
        "The technical writer is responsible for creating documentation for the product. This is the person who acts as a communicator too (Writes user guides and manuals and Communicates technical information clearly and concisely).",
        "The customer support specialist is responsible for providing support to customers after the product release. This is the person who acts as a listener too (Listens to customer feedback and Addresses customer concerns and issues)."
    ]

    st.session_state.objective = "Release a new version of a software product. The release includes new features, bug fixes, and performance improvements. The product has a deadline of 1 month and a budget of $20,000."
    st.switch_page("app.py")

    

SCRIPT_GUIDE = """**Quality Guide for Conversation Evaluation in a Payment Gateway**

        ---

        ## **1. Introduction**
        This quality guide aims to provide a detailed reference framework for evaluating customer service in an online payment platform, similar to PayPal. It focuses on ensuring that interactions between agents and customers are effective, aligned with the company’s culture and image, and proactively resolve users' needs.

        ---

        ## **2. General Evaluation Criteria**
        Interactions must meet the following fundamental criteria:

        ### **2.1 Professionalism and Courtesy**
        - Use appropriate and professional language.
        - Avoid excessive slang or informal expressions.
        - Maintain a cordial, empathetic, and respectful tone.
        - Do not interrupt the customer and demonstrate patience.

        ### **2.2 Accuracy and Clarity of Information**
        - Provide precise and verifiable answers.
        - Explain financial or technical terms in a simple manner.
        - Confirm that the customer understands the provided information.

        ### **2.3 Proactivity and Problem Resolution**
        - Anticipate possible customer doubts.
        - Offer viable and quick solutions.
        - Avoid generic responses; personalize according to the case.
        - Properly escalate the case if necessary.

        ### **2.4 Compliance with Policies and Security**
        - Correctly validate the customer’s identity without skipping security steps.
        - Do not provide confidential information to unauthorized individuals.
        - Follow the protocol for verifying suspicious transactions.
        - Properly document each interaction according to internal regulations.

        ---

        ## **3. Detailed Conversation Evaluation**

        ### **3.1 Conversation Start**
        - Proper greeting according to the communication channel.
        - Identify the agent and their willingness to help.
        - Verify the customer's issue or inquiry.

        ### **3.2 Conversation Development**
        - Active listening: do not interrupt, demonstrate understanding.
        - Ask clear and direct questions to better understand the issue.
        - Avoid excessive wait times without updating the customer.
        - Proper use of resources to resolve the case without errors.

        ### **3.3 Conversation Closure**
        - Confirm that the issue has been resolved.
        - Explain the next steps if necessary.
        - Thank the customer and end the conversation cordially.

        ---

        ## **4. Evaluation of Key Indicators**
        For accurate evaluation, each interaction should be analyzed based on the following indicators:

        1. **Response time**: speed of initial attention and case resolution.
        2. **Empathy**: demonstrating genuine understanding and concern for the customer.
        3. **Accuracy**: clear responses aligned with company policies.
        4. **Efficiency**: resolution in the shortest possible time without compromising quality.
        5. **Compliance with protocols**: security, verifications, and correct documentation.
        6. **Customer satisfaction**: positive perception in surveys or comments.

        ---

        ## **5. Example of Evaluation Scale**
        Each interaction will be rated on a scale of 1 to 5:

        | Score | Description |
        |------------|-------------|
        | 5 | Exceptional: Meets all criteria and exceeds expectations. |
        | 4 | Good: Meets main criteria with minor areas for improvement. |
        | 3 | Acceptable: Meets minimum requirements but has significant room for improvement. |
        | 2 | Deficient: Fails to meet several key criteria. |
        | 1 | Unacceptable: Poor service, serious errors, or policy violations. |

        ---

        ## **6. Corrective Actions and Continuous Improvement**
        - Review cases with low scores to identify error patterns.
        - Train agents in areas where deficiencies are detected.
        - Reinforce security policies and effective communication.
        - Implement continuous feedback with review sessions.

        ---

        ## **7. Conclusion**
        This guide is designed to ensure excellence in customer service within the payment platform. Its rigorous application will help improve user experience and strengthen the company's reputation in the market.


        """

def customer_support_qa_success_validation():
    st.session_state.roles = []
    st.session_state.descriptions = []
    
    st.session_state.objective = """

    **Agent:** Good morning, welcome to [Company Name] customer support. My name is Carlos. How can I assist you today?

    **Customer:** Hi, I have a problem with a payment I made yesterday. The transaction appears as completed, but the recipient says they haven’t received the money.

    **Agent:** I understand the situation. Let me check the transaction details. Could you provide me with the transaction ID or the email address associated with the account?

    **Customer:** Sure, the ID is 123456789, and my email is customer@email.com.

    **Agent:** Thank you. I'm reviewing the information... I see that the transaction was processed successfully, but the recipient has not yet claimed it. In some cases, the recipient’s bank may take a few hours to reflect the balance.

    **Customer:** I see, but they told me they haven't received anything, and it’s been more than 24 hours.

    **Agent:** I understand your concern. In this case, we will conduct a detailed transaction trace. I will need to ask you a few questions to complete the internal form.

    **Customer:** Okay.

    **Agent:** Is the recipient using the same email address associated with the transaction?

    **Customer:** Yes, I confirmed with them that they are using recipient.email@email.com.

    **Agent:** Perfect. Now, has the recipient checked their spam folder or blocked notifications?

    **Customer:** I'm not sure. I’ll ask them to check.

    **Agent:** Excellent. If the recipient cannot find the email, they can also try logging directly into their account on our platform and check if they have any pending funds to accept.

    **Customer:** I will contact them to do that.

    **Agent:** In the meantime, I will generate a tracking report. I will send you an email confirming the process along with a reference number for follow-up.

    **Customer:** How long does this process usually take?

    **Agent:** Generally, tracking takes between 24 and 48 hours. However, in many cases, the recipient finds the payment before the process is completed. If you need an update, you can reply to the email I will send you.

    **Customer:** Okay, that reassures me a bit.

    **Agent:** I'm glad to hear that. Is there anything else I can help you with?

    **Customer:** No, that would be all. Thank you so much for your help.

    **Agent:** You're very welcome. Thank you for reaching out to us, and have a great day.


    """
    st.session_state.guide_input = SCRIPT_GUIDE
    st.switch_page("pages/how_to.py")

def customer_support_qa_humdrum_validation():
    st.session_state.roles = []
    st.session_state.descriptions = []
    
    st.session_state.objective = """"

    **Agent:** Good morning, welcome to [Company Name] customer support. My name is Lisa. How can I assist you today?

    **Customer:** Yeah, I’ve got a serious problem. I made a payment two days ago, and the money is gone from my account, but the recipient never received it. This is unacceptable!

    **Agent:** I understand your frustration, and I’m here to help. Let’s take a look at what happened. Could you please provide me with the transaction ID or the email associated with your account?

    **Customer:** I don’t have the transaction ID right now, but my email is frustrated.customer@email.com. I need this fixed immediately!

    **Agent:** Thank you. I’m pulling up the details now... I see that the payment was successfully processed on our end, but it appears that the recipient has not yet claimed the funds. Sometimes, the recipient’s bank takes longer to process transactions. Have they checked their account?

    **Customer:** Of course, they’ve checked! They say there’s nothing there. I don’t care whose fault it is—I just need my money to reach them or be refunded to me!

    **Agent:** I completely understand your concern. We have a process in place to investigate transactions like this. I can initiate a trace on the payment to determine exactly where the funds are. Would you like me to proceed with that?

    **Customer:** Well, obviously! But how long is this going to take? I don’t have time to sit around and wait for days.

    **Agent:** I hear you. Typically, a trace takes 24 to 48 hours to complete. However, in many cases, the recipient receives the funds before the investigation is concluded. I will also send you an email with a reference number so you can track the progress.

    **Customer:** That’s still way too long! I don’t see why this is my problem when I did everything right.

    **Agent:** I understand how frustrating this is, and I assure you we are doing everything we can to resolve it quickly. While we conduct the trace, I recommend asking the recipient to check their spam folder for any notification emails or to manually log into their account to see if the funds are pending.

    **Customer:** Fine, I’ll tell them. But I expect some real answers soon.

    **Agent:** I completely understand. As soon as we have an update, we’ll notify you immediately. Is there anything else I can do for you right now?

    **Customer:** No, just get this fixed.

    **Agent:** We will do our best. I appreciate your patience, and I’ll be in touch as soon as I have an update. Have a good day.

    **Customer:** Yeah, we’ll see.
    """

    st.session_state.guide_input = SCRIPT_GUIDE
    st.switch_page("pages/how_to.py")

def customer_support_qa_wrong_validation():
    st.session_state.roles = []
    st.session_state.descriptions = []
    st.session_state.objective = """

    Agent: Good afternoon, this is Mike from [Company Name] customer support. How can I assist you today?

    Customer: This is ridiculous! I made a payment three days ago, and the recipient hasn’t received it. I need this fixed NOW!

    Agent: I understand your frustration, and I’ll do my best to assist you. Could you provide me with the transaction ID or the email associated with your account?

    Customer: I don’t have the transaction ID, but my email is angry.customer@email.com. And honestly, I don’t see why I have to keep repeating myself every time I contact you!

    Agent: I completely understand your frustration. Let me check your transaction details... I see that the payment was processed successfully on our end. It looks like the recipient has not claimed the funds yet.

    Customer: That’s exactly what I said! So why hasn’t this been fixed already?

    Agent: I wish I had an immediate resolution, but we need to investigate further. I can initiate a trace, which typically takes 24 to 48 hours.

    Customer: 48 hours?! Are you kidding me? I’ve already waited long enough! This is unacceptable service!

    Agent: I understand that this is frustrating, but this is the process we have to follow. Have you asked the recipient to check their account or contact their bank?

    Customer: Why should I have to do that? This is your job, not mine! I paid, and I expect it to go through—end of story!

    Agent: I understand, but without the recipient’s cooperation, resolving this may take longer. I can escalate the case, but I cannot promise an immediate resolution.

    Customer: Oh, so now you’re saying there’s nothing you can do? Typical! This company is a scam!

    Agent: I assure you that’s not the case. We follow strict security measures to ensure transactions are handled properly. However, we do need to follow our investigation process.

    Customer: I don’t care about your ‘process.’ Either I get my money back or the payment goes through—right now!

    Agent: Unfortunately, I cannot guarantee that without completing the trace. If you’d like, I can connect you with a supervisor.

    Customer: Oh great, another person to tell me the same nonsense! Don’t bother. I’ll be reporting this company for fraud.

    Agent: I’m sorry to hear that. If you change your mind, we’re here to help. Have a good day.

    Customer: Whatever.
    """
    st.session_state.guide_input = SCRIPT_GUIDE
    st.switch_page("pages/how_to.py")


def render_use_cases():
    st.title("Use cases for applying in the helpers desk")
    st.write("Here are different use cases for the helpers desk:")

    if st.button("Customer support success QA validation"):
        customer_support_qa_success_validation()
    if st.button("Customer support humdrum QA validation"):
        customer_support_qa_humdrum_validation()
    if st.button("Customer support wrong QA validation"):
        customer_support_qa_wrong_validation()
    if st.button("Roadmap for marketing event"):
        roadmap_for_marketing_event()
    if st.button("Generating tasks for payment gateway development"):
        generating_tasks_for_payment_gateway_development()
    if st.button("Product release checklist"):
        product_release_checklist()


def main():
    render_sidebar(MAP_ROUTES["use_cases"])
    render_use_cases()

if __name__ == "__main__":
    main()