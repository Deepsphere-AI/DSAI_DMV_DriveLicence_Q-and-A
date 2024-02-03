import streamlit as st
import os
from openai import OpenAI
from PIL import Image
import os
from src.DSAI_SQL_Agent.agent import SQL_DB_Agent
from src.DSAI_Drivelicence_DataChatbot.data_conversation import DMV_data_conversation_funtion
from src.DSAI_FAQ_Chatbot.PDF_faq_conversation import main_DMV_app_funtion
# from src.DSAI_FAQ_Chatbot.pdf_Q_A_Conversation import DMV_Q_A_Conversation_funtion
from src.DSAI_PDF_File_URL_Conversation.pdf_file_conversation_GCP import url_pdf_file_conversation
from src.DSAI_DMV_Scenarios_Scope.DMV_scenario import DMV_Scenario_scope
from src.DSAI_DMV_General.generalQ_A import general_based_url_conversation

# Set the page configuration

st.set_page_config(layout="wide")

# Add custom CSS to set the zoom level to 90%
st.markdown(
    """
    <style>
        body {
            zoom: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# # Function to create a new thread
# client = OpenAI(api_key=os.environ["API_KEY"])
# def get_or_create_thread_id():
#     if 'thread_id' not in st.session_state:
#         thread = client.beta.threads.create()
#         st.session_state.thread_id = thread.id
#     return st.session_state.thread_id

# # Call the function to get or create the thread_id when the app starts
# thread_id = get_or_create_thread_id()

# Adding (css)stye to application
with open('style/final.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    
# Adding company logo
imcol1, imcol2, imcol3, imcol4 = st.columns((4,3,5,2))

with imcol2:
    # st.write("## ")
    st.image('image/deeplogo.png')
with imcol3:
    st.image('image/image.png')   

st.markdown("<p style='text-align: center; color: black; font-size:25px;'><span style='font-weight: bold'></span>LLM Revolutionizes Driver's License Management</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: blue;margin-top: -10px ;font-size:20px;'><span style='font-weight: bold'></span>GEN AI Simplifies Your DMV Experience</p>", unsafe_allow_html=True)
st.markdown("<hr style=height:2.5px;margin-top:0px;width:100%;background-color:gray;>",unsafe_allow_html=True)

    
#---------Side bar-------#
with st.sidebar:
    st.markdown("<p style='text-align: center; color: white; font-size:25px;'><span style='font-weight: bold; font-family: century-gothic';></span>Solutions Scope</p>", unsafe_allow_html=True)
    vAR_AI_application = st.selectbox("",['Select Application','Data Driven Q&A','Job Aid Q&A (File)','Policy Q&A (URL)','Transactional Q&A (Database)',"General Q&A",'DMV Scenario Scope'],key='application')
    
    # selected = st.selectbox("",['User',"Logout"],key='text')
    vAR_LLM_model = st.selectbox("",['LLM Models',"gpt-3.5-turbo-16k-0613","gpt-4-0314","gpt-3.5-turbo-16k","gpt-3.5-turbo-1106","gpt-4-0613","gpt-4-0314"],key='text_llmmodel')
    vAR_LLM_framework = st.selectbox("",['LLM Framework',"Langchain"],key='text_framework')

    vAR_Library = st.selectbox("",
                    ["Library Used","Streamlit","Image","Pandas","openAI"],key='text1')
    vAR_Gcp_cloud = st.selectbox("",
                    ["GCP Services Used","VM Instance","Computer Engine","Cloud Storage"],key='text2')
    st.markdown("#### ")
    href = """<form action="#">
            <input type="submit" value="Clear/Reset"/>
            </form>"""
    st.sidebar.markdown(href, unsafe_allow_html=True)
    st.markdown("# ")
    st.markdown("<p style='text-align: center; color: White; font-size:20px;'>Build & Deployed on<span style='font-weight: bold'></span></p>", unsafe_allow_html=True)
    s1,s2=st.columns((2,2))
    with s1:
        st.markdown("### ")
        st.image('image/002.png')
    with s2:    
        st.markdown("### ")
        st.image("image/oie_png.png")

if vAR_AI_application == 'Job Aid Q&A (File)':
    main_DMV_app_funtion()
elif vAR_AI_application == 'Transactional Q&A (Database)':
    SQL_DB_Agent()
elif vAR_AI_application == 'Data Driven Q&A':
    DMV_data_conversation_funtion()
elif vAR_AI_application == 'Policy Q&A (URL)':
    url_pdf_file_conversation()
elif vAR_AI_application == 'DMV Scenario Scope':
    DMV_Scenario_scope()
elif vAR_AI_application == 'General Q&A':
    general_based_url_conversation()