from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(openai_api_key="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")

from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import pandas as pd
from langchain.llms import OpenAI


def get_me_an_answer(question):
  df = pd.read_csv("Neosporin_Patients.csv")

  agent = create_pandas_dataframe_agent(
      ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key="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"),
      df,
      verbose=True,
      agent_type=AgentType.OPENAI_FUNCTIONS,
  )

  return agent.run(question)


