from crewai import Agent, Task, Crew, LLM, Process
import os
import re
import json
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from ibm_watsonx_ai import APIClient, Credentials
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from IPython.display import Markdown
from utils import GENERAL_PROMPT
import requests
from langgraph.constants import Send, START, END
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Literal
import operator
from pydantic import BaseModel, Field
from langchain.schema import SystemMessage, HumanMessage
from IPython.display import Image, Markdown
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings


""" import logging

# Configure logging to capture HTTP requests
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging for requests
import http.client
http.client.HTTPConnection.debuglevel = 1 """

load_dotenv()

endpoint_watsonx = os.getenv('WATSONX_URL')
api_key_watsonx = os.getenv('WATSONX_APIKEY')
project_id_watsonx = os.getenv('WATSONX_PROJECT_ID')
endpoint_mistralai = os.getenv('MISTRALAI_URL')
api_key_mistralai = os.getenv('MISTRALAI_APIKEY')

def set_up_watsonx():
    token_watsonx = authenticate_watsonx()
    if token_watsonx == None:
        return None
    parameters = {
        "max_new_tokens": 1500,
        "min_new_tokens": 1,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 1,
    }

    embed_params = {
        EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
        EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
    }

    credentials = Credentials(
        url = endpoint_watsonx,
        api_key = api_key_watsonx,
    )

    client = APIClient(credentials, project_id=project_id_watsonx)

    client.set_token(token_watsonx)

    watsonx_llm = WatsonxLLM(
        #model_id="ibm/granite-13b-instruct-v2",
        model_id="ibm/granite-34b-code-instruct",
        watsonx_client=client,
        params = parameters
    )

    """ watsonx_crew_llm = LLM(
        model="watsonx/ibm/granite-13b-instruct-v2",
        base_url= "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29",
        api_key= api_key_watsonx,
    ) """
    """ watsonx_crew_llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.5,
        max_tokens=2000,
        mistral_api_key=api_key_mistralai,
        endpoint=endpoint_mistralai
    ) """

    """ os.environ["AZURE_AI_API_KEY"] = api_key_mistralai
    os.environ["AZURE_AI_API_BASE"] = endpoint_mistralai
    watsonx_crew_llm = LLM(
        model="azure_ai/mistral-large-latest",
        base_url= endpoint_mistralai,
        api_key= api_key_mistralai,
    ) """
    """ llm_aux = ChatOllama(
        model = "llama3:8b",
        temperature = 0.8,
        num_predict = 256,
    ) """
    return watsonx_llm

def authenticate_watsonx():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key_watsonx
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        os.environ["WATSONX_TOKEN"] = token
        return token
    else:
        print("Authentication failed. Status code:", response.status_code)
        print("Response:", response.text)
        return None



def orchestrate_graph_agents(roles, descriptions, report_formats, objective, language):

    llm= set_up_watsonx()
    if llm == None:
        print("Error setting up WatsonX")
        return
        

    # Graph state
    class State(TypedDict):
        objective: str  # Shared objective
        roles: list[str]  # Dynamic list of roles
        descriptions: list[str]  # Descriptions of each role
        contributions: Annotated[list, operator.add]  # Contributions from each role
        final_summary: str  # Final synthesized output

    # Worker state
    class WorkerState(TypedDict):
        role: str
        objective: str
        description: str
        contributions: Annotated[list, operator.add]

    # Nodes
    def orchestrator(state: State):
        """Orchestrator that assigns objectives to roles"""
        return {"roles": state["roles"]}

    def role_worker(state: WorkerState):
        """Each worker contributes based on its role"""
        role = state["role"]
        contribution = llm.invoke([
            SystemMessage(content=f"You are a {role}. Contribute to the given objective taking into account the next behaviour and description that defines your role: {state['description']}. Based on that information, provide your criteria to fulfill what user is asking for."),
            HumanMessage(content=f"Objective: {state['objective']}"),
        ])
        return {"contributions": [contribution]}

    def synthesizer(state: State):
        """Synthesizes final output from contributions"""
        summary = "\n\n---\n\n".join(state["contributions"])
        return {"final_summary": summary}

    def assign_workers(state: State):
        """Dynamically assigns workers based on roles"""
        return [Send("role_worker", {"role": role, "objective": state["objective"], "description": description}) for role, description in zip(state["roles"], state["descriptions"])]
    # Build workflow
    workflow_builder = StateGraph(State)

    # Add nodes
    workflow_builder.add_node("orchestrator", orchestrator)
    workflow_builder.add_node("role_worker", role_worker)
    workflow_builder.add_node("synthesizer", synthesizer)

    # Add edges
    workflow_builder.add_edge(START, "orchestrator")
    workflow_builder.add_conditional_edges("orchestrator", assign_workers, ["role_worker"])
    workflow_builder.add_edge("role_worker", "synthesizer")
    workflow_builder.add_edge("synthesizer", END)

    # Compile workflow
    workflow = workflow_builder.compile()

    # Invoke
    state = workflow.invoke({
        "objective": objective,
        "roles": roles,
        "descriptions": descriptions,
    })

    return state["final_summary"]
    

def orchestate_graph_agents_evaluating(roles, descriptions, report_formats, objective, language):

    llm= set_up_watsonx()
    if llm == None:
        print("Error setting up WatsonX")
        return
        
    # Graph state
    class State(TypedDict):
        objective: str  # Shared objective
        roles: list[str]  # Dynamic list of roles
        accumulated_info: Annotated[list, operator.add]  # Information gathered
        final_summary: str  # Final synthesized output

    # Schema for structured evaluation output
    class Feedback(BaseModel):
        grade: Literal["accepted", "rejected"] = Field(
            description="Decide if the contribution meets the objective or needs improvement.",
        )
        feedback: str = Field(
            description="If rejected, provide feedback on how to improve it.",
        )

    # Augment LLM with structured evaluation output
    evaluator = llm.with_structured_output(Feedback)

    # Nodes
    def generator(state: State):
        """Generates an initial proposal for the given objective."""
        proposal = llm.invoke([
            SystemMessage(content="Generate an initial idea or approach for the given objective."),
            HumanMessage(content=f"Objective: {state['objective']}"),
        ])
        return {"accumulated_info": [proposal]}

    def role_evaluator(state: State):
        """Each evaluator critically assesses the proposal."""
        role = state["roles"].pop(0)  # Process roles one by one
        evaluation = evaluator.invoke(f"Evaluate this contribution based on the objective: {state['accumulated_info'][-1]}\nRole: {role}")
        return {"grade": evaluation.grade, "feedback": evaluation.feedback}

    def synthesizer(state: State):
        """Synthesizes the final report from all accumulated insights."""
        summary = "\n\n---\n\n".join(state["accumulated_info"])
        return {"final_summary": summary}

    def route_feedback(state: State):
        """Decide whether to iterate or finalize based on evaluation."""
        if state["grade"] == "accepted" or not state["roles"]:
            return "Accepted"
        else:
            return "Rejected + Feedback"

    def update_generator(state: State):
        """Updates the proposal based on evaluator feedback."""
        updated_proposal = llm.invoke([
            SystemMessage(content="Refine the proposal based on the given feedback."),
            HumanMessage(content=f"Feedback: {state['feedback']}\nPrevious proposal: {state['accumulated_info'][-1]}"),
        ])
        return {"accumulated_info": state["accumulated_info"] + [updated_proposal]}

    # Build workflow
    workflow_builder = StateGraph(State)

    # Add nodes
    workflow_builder.add_node("generator", generator)
    workflow_builder.add_node("role_evaluator", role_evaluator)
    workflow_builder.add_node("update_generator", update_generator)
    workflow_builder.add_node("synthesizer", synthesizer)

    # Add edges
    workflow_builder.add_edge(START, "generator")
    workflow_builder.add_edge("generator", "role_evaluator")
    workflow_builder.add_conditional_edges("role_evaluator", route_feedback, {
        "Accepted": "synthesizer",
        "Rejected + Feedback": "update_generator",
    })
    workflow_builder.add_edge("update_generator", "role_evaluator")
    workflow_builder.add_edge("synthesizer", END)

    # Compile workflow
    workflow = workflow_builder.compile()

    # Invoke in Streamlit
    state = workflow.invoke({
        "objective": "Develop a comprehensive AI ethics framework",
        "roles": ["Researcher", "Philosopher", "Engineer", "Lawyer", "Product Manager"]
    })

    return state["final_summary"]

""" 
def orchestrate_agents(roles, descriptions, report_formats, objective):
    watsonx_llm, watsonx_crew_llm = set_up_watsonx()
    if watsonx_llm == None:
        print("Error setting up WatsonX")
        return
    system_template = GENERAL_PROMPT

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    agents_array = []
    tasks_array = []
    json_array = []
    
    for cont, individual_role in enumerate(roles):  
        try:
            concatenated_role= f"Role: {individual_role}. Description/behaviour:{descriptions[cont]}. Objective: {objective}"
            prompt = prompt_template.invoke({"text": concatenated_role})
            prompt.to_messages()

            response = watsonx_llm.invoke(prompt)
            match = re.search(r'\{.*?\}', response)
            print(response)
            
            if match:
                json_content = match.group(0)
                try:
                    json_data = json.loads(json_content)
                    json_array.append(json_data)
                    current_agent = Agent(
                        llm = watsonx_crew_llm,
                        role=json_data["role"],
                        goal=json_data["goal"],
                        backstory=json_data["backstory"]
                    )
                    agents_array.append(current_agent)
                    tasks_array.append(Task(
                        description=json_data["tasks_description"],
                        expected_output=json_data["tasks_expected_output"],
                        agent= current_agent
                    ))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error orchestrating agent: {e}")
            continue
        
        
    print("Agents orchestrated successfully!")
    print(json_array)

    agents_crew = Crew(
        agents=agents_array, 
        tasks=tasks_array, 
        process=Process.hierarchical,
        manager_llm=watsonx_crew_llm,
        verbose=True 
    )

    result = agents_crew.kickoff(inputs={'input': objective})
    print(result)
    
    print("Agents orchestrated successfully!")
    
 """
