import os
import numpy as np
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from ibm_watsonx_ai import APIClient, Credentials
from langchain_core.prompts import ChatPromptTemplate
import requests
from langgraph.constants import Send, START, END
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
import operator
from langchain.schema import SystemMessage, HumanMessage
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings
import torch
from sentence_transformers.util import cos_sim
import tiktoken


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
    watsonx_embedding = WatsonxEmbeddings(
        model_id="ibm/granite-embedding-278m-multilingual",
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id_watsonx,
        params=embed_params,
    ) 

    return watsonx_llm  , watsonx_embedding

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



def orchestrate_graph_agents(roles, descriptions,  objective, language):

    llm, watsonx_embedding = set_up_watsonx()
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
            SystemMessage(content=f"You are a helpfully {role}. Contribute to the given objective taking into account the next behaviour and description that defines your role: {state['description']}. Your conrtributions mustn't be with questions, since your position and role, you will try to solve that in the best way. Based on that information, provide your criteria to fulfill what user is asking for. You must answer always to the user in the language: " + language),
            HumanMessage(content=f"Objective: {state['objective']}"),
        ])
        return {"contributions": [contribution]}

    def synthesizer(state: State):
        """Synthesizes final output from contributions"""
        summary = "\n\n---\n\n".join(state["contributions"])
        conclusion = llm.invoke([
            SystemMessage(content=f"You are a helpfully AI that is going to provide a solution to the user based on the contributions of the roles, taking into account the most relevant information provided by each section, not just the last one part. Remember the objective that you will enfatize {state['objective']}. You must answer with concise information, roudmap, guidelines, list of items and so, but never answer with questions. You must answer always to the user in the language: " + language),
            HumanMessage(content=f"This is the text that you must organize and bastract the main ideas and guidelines: {summary}"),
        ])
        return {"final_summary": summary + "\n\n🔽------*****------🔽\n\n" + conclusion}

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
    


def get_ollama_embedding(texts, model):
    embeddings = []
    for text in texts:
        #response = ollama.embeddings(model=model, prompt=text)
        response = model.embed_query(text)
        embeddings.append(response)
    
    # Find the maximum length of the embeddings
    max_length = max(len(embedding) for embedding in embeddings)
    
    # Pad all embeddings to the maximum length
    padded_embeddings = [embedding + [0] * (max_length - len(embedding)) for embedding in embeddings]
    
    return torch.tensor(np.array(padded_embeddings), dtype=torch.float32)

def split_text_into_chunks(text, model="gpt-3.5-turbo", chunk_size=150):
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = tokenizer.encode(text)

    # Split tokens into chunks of chunk_size
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]

    # Decode tokens back into text
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]

    return text_chunks


def orchestate_graph_agents_evaluating(guide_input, text_input):

    llm, watsonx_embedding = set_up_watsonx()
    if llm == None or watsonx_embedding == None:
        print("Error setting up WatsonX")
        return
        
    chunks = split_text_into_chunks(text_input)
    scores=["very bad feedback", "bad feedback", "neutral feedback", "good feedback", "very good feedback"]

    scores_embeddings = get_ollama_embedding(scores, watsonx_embedding)
     
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", f"You are an expert in the next script and document that is showing bellow: {guide_input} \n\n It shows the guidelines of how must be the behaviour and culture of the customer support workers. Based on that you are going to create a feedback like, 'The worker has addressed correctly the connversation', 'The worker is not following correctly the guidelines', 'The worker seems like it was not a worker from the company, is deficent' and so, about the fragment of text that the user provide, taking into account the behaviour of the agent or worker involved in the conversation and how many the worker does fit with the guide or items provided, regardless of whether or not it was possible to solve the problem. You must thing about how is the customer or client, and how is the agent or worker, and provide feedback just to what agent/worker say, and how is he handle the customer/client disposition"), ("user", "{chunk}")]
    )

    scores_array = []
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        
        try:
            prompt = prompt_template.invoke({"chunk": chunk})
            prompt.to_messages()

            feedback = llm.invoke(prompt)
            feedback_embedding = get_ollama_embedding([feedback], watsonx_embedding)
            similarity_scores = cos_sim(scores_embeddings, feedback_embedding)
            how_good = scores[similarity_scores.argmax()]
            #index of scores
            index = scores.index(how_good)
            scores_array.append(index)
        except Exception as e:
            print(f"Error processing chunk {i+1}: {e}")
            continue
            
    #set average score
    print(scores_array)
    average = np.mean(scores_array)
    return average




            


