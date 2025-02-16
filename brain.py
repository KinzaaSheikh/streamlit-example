import os
import pandas as pd
from dotenv import load_dotenv
from litellm import completion
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Load environment variables from .env file
load_dotenv()

# Retrieve the GEMINI_API_KEY from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Set the GEMINI_API_KEY for LiteLLM
os.environ["GEMINI_API_KEY"] = gemini_api_key

def get_me_an_answer(question):
    # Load your CSV data into a DataFrame
    df = pd.read_csv("Terlipresin Matching Cohort Data.csv")

    # Initialize the ChatOpenAI model with LiteLLM
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response = completion(model="gemini-2.0-flash", messages=messages)
    print(response['choices'][0]['message']['content'])

    # Create a pandas DataFrame agent
    agent = create_pandas_dataframe_agent(
        response,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=(
            "This ask is a little beyond my intelligence, and I have tried to "
            "not get creative and make up an answer. So sorry I could not help at this time!"
        ),
    )

    # Run the agent with the provided question
    return agent.run(question)
