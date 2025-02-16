import streamlit as st

from brain import get_me_an_answer

# --- App Configuration ---
st.set_page_config(
    page_title="Terlipressin Q&A",
    page_icon="💉",  
    layout="centered",  
    initial_sidebar_state="collapsed", 
)

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 800px;
        padding-top: 20px;
        padding-right: 20px;
        padding-left: 20px;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;  /* Green border */
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stTextArea > div > div > textarea {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- App Header ---
st.title("Ask Quantum 👨‍⚕️ 💉")
st.markdown("Get instant answers about Terlipressin, powered by Quantum AI.")  # Added a subtitle

# --- Question Input ---
question_input = st.text_input("Enter your question:", placeholder="e.g., What are the common side effects of Terlipressin?")

# --- Display Answer ---
if question_input:
    with st.spinner("Thinking..."):  # Added a spinner
        answer = get_me_an_answer(question_input, st.secrets["GEMINI_API_KEY"])
    st.markdown("### Answer:")  # More prominent answer heading
    st.info(answer) # Changed to st.info for a cleaner look.  Consider st.markdown for more formatting control
    st.text_area("Answer:", answer, height=200) #alternative if you want to keep text_area


# --- Footer (Optional) ---
st.markdown("---")
st.markdown(
    """
    **Disclaimer:** This information is for informational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional for any health concerns or before making any decisions related to your health or treatment.
    """
)