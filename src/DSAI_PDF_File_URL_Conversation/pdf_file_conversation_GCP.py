from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from src.DSAI_Utiles.file_save import download_file
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import bs4
import os
from streamlit_chat import message
from dotenv import load_dotenv
load_dotenv() 

def url_pdf_file_conversation():
    col1,col2,col3,col4 = st.columns((2,2.5,3.5,2))
    col11,col22,col33 = st.columns((2,8,2))
    
    with col2:
        st.write('# ')
        st.write('### ')
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input Type</span></p>", unsafe_allow_html=True)
    with col3:
        st.write('## ')
        vAR_URL = st.text_input(" ", placeholder="Enter URL")
    
    if vAR_URL:
        vAR_directory,vAR_num_pages = download_file(vAR_URL)
        loader = PyPDFLoader(vAR_directory)
        document = loader.load()
        
        # split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)
        
        # create a vectorstore from the chunks
        vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

        retriever = vector_store.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-4",api_key=os.environ["OPENAI_API_KEY"])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        # rag_chain.invoke("What is Task Decomposition?")
        with col22:
            st.write('# ')
            st.write('# ')
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
                    vAR_response = rag_chain.invoke(user_input)                 
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(vAR_response)

            if st.session_state['generated']:
                    with response_container:
                        for i in range(len(st.session_state['generated'])):
                            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                            message(st.session_state["generated"][i], key=str(i+55), avatar_style="thumbs")