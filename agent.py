from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.tools import FunctionTool
import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from datetime import datetime
import base64
import shutil

# Load environment variables from .env file
load_dotenv()

llm = OpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])

# Create sandbox
sbx = Sandbox(api_key=os.environ["E2B_API_KEY"])

sbx.set_timeout(60 * 10)


# Upload the dataset to the sandbox
dataset_path_in_sandbox = ""
with open("Terlipresin Matching Cohort Data.csv", "rb") as f:
    dataset_path_in_sandbox = sbx.files.write("dataset.csv", f)


def delete_folder_contents(folder_path: str, include_folders: bool = True) -> tuple[int, list[str]]:

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist")

    # Check if it's actually a directory
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"The path {folder_path} is not a directory")

    files_deleted = 0
    errors = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                # Delete file
                os.unlink(file_path)
                files_deleted += 1
            elif os.path.isdir(file_path) and include_folders:
                # Delete directory and its contents if include_folders is True
                shutil.rmtree(file_path)
                files_deleted += 1
        except Exception as e:
            errors.append(f"Error deleting {filename}: {str(e)}")

    return files_deleted, errors


def execute_python(code: str):
    execution = sbx.run_code(code)
    return execution.text


def create_charts(code: str):

    folder_name = 'charts'

    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    execution = sbx.run_code(code)
    first_result = execution.results[0]

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f'image_{timestamp}.png'

    # Create full file path
    file_path = os.path.join(folder_name, filename)

    if first_result.png:
        try:
            # Save the png to a file. The png is in base64 format.
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(first_result.png))
            print(f'Chart saved as {file_path}')
        except Exception as e:
            print(f'Error saving chart: {str(e)}')
    else:
        print('No PNG data found in the execution results')

    return first_result


def run_agent(query: str):

    delete_folder_contents("charts")

    e2b_sandbox_tool = FunctionTool.from_defaults(
        name="execute_python",
        description="Execute python code in a Jupyter notebook cell and return result",
        fn=execute_python
    )

    e2b_sandbox_charts_tool = FunctionTool.from_defaults(
        name="create_charts",
        description="Execute python code in a Jupyter notebook cell for a chart or graph and returns a png",
        fn=create_charts
    )

    system_promt = f'''
    You are an expert Data Engineer and Analyst AI Agent with access to CSV files through Python code execution. Your primary role is to help users analyze, understand, and extract insights from their data.

    CAPABILITIES AND TOOLS:
    - You have access to a Python code execution environment through the e2b_sandbox_tool and e2b_sandbox_charts_tool to create charts or graphs
    - You can read and analyze CSV files using Python libraries (pandas, numpy, matplotlib, seaborn, etc.)
    - You can execute code in Jupyter notebook-style cells and return results
    - The file is located in the sandbox at {dataset_path_in_sandbox.path}
    - You have  access to a Python code execution environment through the e2b_sandbox_charts_tool to create charts or graphs for each user query.

    RESPONSE METHODOLOGY:
    1. When receiving a query, first analyze what the user is asking for and determine the required data analysis steps
    2. Analyze the columns and data in the dataset before proceeding with the query.
    3. Break down complex requests into smaller, manageable tasks
    4. Write clear, well-documented Python code to accomplish these tasks
    5. Execute the code using e2b_sandbox_tool
    6. Interpret the results and provide clear explanations to the user
    7. When appropriate, create visualizations to better communicate insights using e2b_sandbox_charts_tool

    CODE EXECUTION GUIDELINES:
    - Always use proper error handling in your code
    - Include comments to explain key steps
    - Format code for readability
    - Use efficient pandas operations when possible
    - Handle missing or incorrect data gracefully
    - Validate inputs before processing

    EXAMPLE CODE EXECUTION:
    When executing code, follow this format:
    ```python
    # Import required libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Read the CSV file
    df = pd.read_csv('your_file.csv')

    # Perform analysis
    # [Analysis code here]

    # Create visualization if needed
    # [Visualization code here]
    ```

    HANDLING DIFFERENT TYPES OF QUERIES:

    1. Exploratory Data Analysis:
    - Provide summary statistics
    - Identify data types and distributions
    - Check for missing values
    - Examine relationships between variables

    2. Specific Calculations:
    - Clearly show the calculation steps
    - Provide intermediate results when relevant
    - Include error margins when applicable
    - Explain the methodology used

    3. Trend Analysis:
    - Consider seasonality and periodicity
    - Account for outliers
    - Provide both short-term and long-term perspectives
    - Include relevant statistical tests

    4. Comparative Analysis:
    - Use appropriate statistical tests
    - Consider sample sizes and distributions
    - Provide effect sizes when relevant
    - Explain practical significance

    Remember to always:
    1. Start with understanding the user's needs
    2. Validate your approach before execution
    3. Provide clear, actionable insights
    4. Be ready to iterate based on feedback
    5. Document your process and assumptions
    6. Consider the broader context of the analysis
    '''
    agent = OpenAIAgent.from_tools(
        [e2b_sandbox_tool, e2b_sandbox_charts_tool],
        verbose=True,
        llm=llm,
        system_prompt=system_promt)

    response = agent.chat(query)

    return response.response
