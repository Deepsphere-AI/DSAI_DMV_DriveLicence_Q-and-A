import streamlit as st
import os
from openai import OpenAI
from src.DSAI_Utiles.prompt import prompt
from dotenv import load_dotenv
import os
import json
import time
from src.DSAI_DMV_Scenarios_Scope.function_calling import SQL_agent_calling

load_dotenv() 
# Openai Assistant API
def conversation_for_FAQ(user_input,vAR_directory,vAR_num_pages):
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=os.environ["API_KEY"])
        st.session_state.file = st.session_state.client.files.create(
            file=open(vAR_directory, "rb"),
            purpose='assistants'
        )
        st.session_state.assistant = st.session_state.client.beta.assistants.update(
        os.environ["DMV_DriveLicence_FAQ"],
        instructions=prompt(vAR_num_pages),
        name="DMV_DriveLicence_FAQ",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[st.session_state.file.id],
        )
        
        # Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    message = st.session_state.client.beta.threads.messages.create(thread_id=st.session_state.thread.id,role="user",content=user_input,file_ids=[st.session_state.file.id])
    run = st.session_state.client.beta.threads.runs.create(thread_id=st.session_state.thread.id,assistant_id=st.session_state.assistant.id)
    # run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant.id,run_id=run.id)
    
    while True:
        run = st.session_state.client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id, run_id=run.id)
        if run.status=="completed":
            messages = st.session_state.client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            break     
    return text


# Openai Assistant API
def conversation_for_data(user_input):
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=os.environ["API_KEY"])
        st.session_state.thread = st.session_state.client.beta.threads.create()
    message = st.session_state.client.beta.threads.messages.create(thread_id=st.session_state.thread.id,role="user",content=user_input)
    run = st.session_state.client.beta.threads.runs.create(thread_id=st.session_state.thread.id,assistant_id=os.environ["DMV_DriveLicence_Chatbot"])
    # run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant.id,run_id=run.id)
    
    while True:
        run = st.session_state.client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id, run_id=run.id)
        if run.status=="completed":
            messages = st.session_state.client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            break     
    return text


def DMV_scenario_scope_chatbot(user_input):
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=os.environ["API_KEY"])
        st.session_state.thread = st.session_state.client.beta.threads.create()
    message = st.session_state.client.beta.threads.messages.create(thread_id=st.session_state.thread.id,role="user",content=user_input)
    run = st.session_state.client.beta.threads.runs.create(thread_id=st.session_state.thread.id,assistant_id=os.environ["DMV_Scenario_Scope"])
    
    while True:
        time.sleep(2)
        
        # Retrieve the run status
        run_status = st.session_state.client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id,run_id=run.id)
        
        print('run status - ',run_status.model_dump_json(indent=4))

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )
            # Loop through messages and print content based on role
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                print(f"{role.capitalize()}: {content}")

                return content
        elif run_status.status == 'requires_action':
                print("Function Calling")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                print('required_actions - ',required_actions)
                tool_outputs = []
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    print("arguments - ",arguments)
                    
                    if func_name == "SQL_agent_calling":
                        output = SQL_agent_calling(arguments["vAR_qestion"])
                        
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    else:
                        raise ValueError(f"Unknown function: {func_name}")
                    
                print("Submitting outputs back to the Assistant...")
                st.session_state.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=st.session_state.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
    
    # print('run status - ',run_status.model_dump_json(indent=4))
    
    # if run_status.status == 'completed':
    #     messages = st.session_state.client.beta.threads.messages.list(
    #                 thread_id=st.session_state.thread_id)
        
    #     for message in messages.data:
    #         role = message.role
    #         content = message.content[0].text.value
    #         print(f'{role}: {content}')
    #         return content
    # elif run_status.status == 'requires_action':
    #     required_action = run_status.required_action.submit_tool_outputs.model_dump()
    #     tools_outputs = []
    #     for action in required_action["tool_calls"]:
    #         func_name = action["function"]["name"]
    #         arguments = json.loads(action["function"]["arguments"])
    #         if func_name == "SQL_agent_calling":
    #             output = SQL_agent_calling(arguments["vAR_qestion"])
    #             tools_outputs.append({
    #                 "tool_call_id": action['id'],
    #                 "output": output
    #             })
    #         else:
    #             print(f"Unknown function name: {func_name}")
        
    #     st.session_state.client.beta.threads.runs.submit_tool_outputs(
    #         thread_id=st.session_state.thread_id,
    #         run_id=run.id,
    #         tool_outputs=tools_outputs
    #     )
    