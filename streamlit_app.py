# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st

# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI

# from brain import get_me_an_answer

# st.title("Ask Quantum about Terlipressin 👨‍⚕️ 💉")

# question_input = st.text_input("Question:")

# if question_input:
#     answer = get_me_an_answer(question_input)
#     st.text_area("Answer:", answer)
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from brain import get_me_an_answer

# Initialize session state for managing input state and answer
if 'disabled' not in st.session_state:
    st.session_state.disabled = False
if 'answer' not in st.session_state:
    st.session_state.answer = None

st.title("Ask Quantum about Terlipressin 👨‍⚕️ 💉")

# Create container for input elements
input_container = st.container()

with input_container:
    # Create text area for input
    question_input = st.text_area(
        "Question:",
        disabled=st.session_state.disabled,
        key="question_input"
    )

    # Add "Ask" button
    if st.button("Ask", disabled=st.session_state.disabled):
        if question_input:
            # Disable input while processing
            st.session_state.disabled = True
            st.session_state.answer = None

            # Rerun to show disabled state
            st.rerun()

# Handle answer generation and display
if st.session_state.disabled and st.session_state.answer is None:
    # Get the answer
    answer = get_me_an_answer(question_input)

    # Store answer in session state
    st.session_state.answer = answer

    # Re-enable input
    st.session_state.disabled = False

    # Rerun to show enabled state and answer
    st.rerun()

# Display answer if available
if st.session_state.answer:
    st.markdown("**Answer:**")
    st.markdown(st.session_state.answer)
