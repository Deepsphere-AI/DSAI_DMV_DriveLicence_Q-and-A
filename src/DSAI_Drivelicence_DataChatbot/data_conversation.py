import streamlit as st
from streamlit_chat import message
from src.DSAI_Utiles.Assistant_api import conversation_for_data

def DMV_data_conversation_funtion():
    col11,col22,col33 = st.columns((2,8,2))
    with col22:
        ########################################### chatbot UI###############################################
        if 'history' not in st.session_state:
                st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Greetings! I am DeepSphere Live Agent. How can I help you?"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["We are delighted to have you here in the DeepSphere Live Agent Chat room!"]

        #container for the chat history
        response_container = st.container()

        #container for the user's text input
        container = st.container()
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                
                user_input = st.text_input("Prompt:", placeholder="How can I help you?", key='input')
                submit_button = st.form_submit_button(label='Interact with LLM')
                
            if submit_button and user_input:
                # messages_history.append(HumanMessage(content=user_input))
                vAR_response = conversation_for_data(user_input)                    
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(vAR_response)

        if st.session_state['generated']:
                with response_container:
                    for i in range(len(st.session_state['generated'])):
                        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                        message(st.session_state["generated"][i], key=str(i+55), avatar_style="thumbs")