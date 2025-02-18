import streamlit as st
import os
from datetime import datetime
import glob
from agent import run_agent


def get_latest_image():
    """Get the most recent image from the charts folder."""
    try:
        # Get list of all PNG files in the charts folder
        image_files = glob.glob("charts/*.png")
        if not image_files:
            return None

        # Sort by creation time and get the most recent
        latest_image = max(image_files, key=os.path.getctime)
        return latest_image
    except Exception as e:
        st.error(f"Error accessing images: {str(e)}")
        return None


def main():
    # Set page config
    st.set_page_config(
        page_title="Quantum Pharma Analysis",
        page_icon="💊",
        layout="wide"
    )

    # Title and description
    st.title("🔬 Quantum Pharma Analysis")
    st.markdown("""
    This tool helps analyze pharmaceutical data using advanced AI techniques.
    Enter your question below to get insights from the data.
    """)

    # Input box for question
    question = st.text_area(
        "Enter your question:",
        height=100,
        placeholder="e.g., What is the average age of patients in the study?"
    )

    # Add a submit button
    if st.button("Analyze", type="primary"):
        if question:
            try:
                # Show loading spinner while processing
                with st.spinner("Analyzing data..."):
                    # Get response from agent
                    response = run_agent(question)

                    # Display the response in a nice format
                    st.markdown("### Analysis Results")
                    st.write(response)

                    # Check for and display any generated images
                    latest_image = get_latest_image()
                    if latest_image:
                        st.markdown("### Generated Visualization")
                        st.image(latest_image)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question to analyze.")


if __name__ == "__main__":
    main()
