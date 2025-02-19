import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os

from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])


def get_me_an_answer(question):
    # llm = ChatOpenAI(openai_api_key=key)
    df = pd.read_csv("Terlipresin Matching Cohort Data.csv")

    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-4o",
                   openai_api_key=os.environ["OPENAI_API_KEY"]),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors="This ask is a little beyond my intelligence, and I have traied to Not get creative and make up answer. So sorry I could not help at this time!",
        allow_dangerous_code=True
    )

    return agent.run(question)
