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

    credentials = Credentials(
        url = endpoint_watsonx,
        api_key = api_key_watsonx,
    )

    client = APIClient(credentials, project_id=project_id_watsonx)

    client.set_token(token_watsonx)

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-20b-code-instruct",
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

    os.environ["AZURE_AI_API_KEY"] = api_key_mistralai
    os.environ["AZURE_AI_API_BASE"] = endpoint_mistralai
    watsonx_crew_llm = LLM(
        model="azure_ai/mistral-large-latest",
        base_url= endpoint_mistralai,
        api_key= api_key_mistralai,
    )
    
    return watsonx_llm, watsonx_crew_llm

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
    

