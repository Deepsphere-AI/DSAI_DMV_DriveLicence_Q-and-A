from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI

def SQL_agent_calling(vAR_qestion):
    llm = ChatOpenAI(model_name="gpt-4",api_key=os.environ["OPENAI_API_KEY"])
    db = SQLDatabase.from_uri("mysql+pymysql://root:01012001@34.30.129.74:3306/DMV_license")

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    vAR_response = agent_executor.run(vAR_qestion)
    
    return vAR_response