import streamlit as st
from io import BytesIO
import time
import os
from custome_function_main import get_bot_response


def generate_ppt(topic: str, theme: str) -> tuple:
    """
    Function to generate the PowerPoint presentation based on the selected topic and theme.

    Parameters:
    topic (str): The topic for the PowerPoint presentation.
    theme (str): The selected theme for the PowerPoint presentation.

    Returns:
    tuple: A tuple containing the PPT file path and the PPT file name.
    """
    design = {
        "Theme A": "Design-1",
        "Theme B": "Design-2",
        "Theme C": "Design-3",
        "Theme D": "Design-4",
        "Theme E": "Design-5",
        "Theme F": "Design-6",
        "Theme G": "Design-7",
        "Custom Theme 1": "Design-8",
        "Custom Theme 2": "Design-9",
    }

    print(topic, design[theme])
    ppt_path, ppt_name = get_bot_response(topic, design[theme])
    return ppt_path, ppt_name


def main() -> None:
    """
    Main function to create the Streamlit UI for AI-Enhanced Presentation Maker.
    """
    st.title("AI-Enhanced Presentation Maker by Gemini")
    topic = st.text_input("Enter your topic:")
    themes = ["Theme A", "Theme B", "Theme C", "Theme D", "Theme E", "Theme F", "Theme G", "Custom Theme 1", "Custom Theme 2"]
    theme = st.selectbox("Select a theme:", themes)

    if st.button("Create"):
        if topic:
            progress_bar = st.progress(0)
            st.text('Initializing...')
            st.text('Generating Prompt...')
            for percent_complete in range(100):
                time.sleep(0.10)
                progress_bar.progress(percent_complete)
            st.success(f"Prompt for '{topic}' generated successfully!")
            st.warning("Wait! Slides for PPT are being generated...")

            progress_bar = st.progress(0)
            st.text('Generating PPT Slides...')
            for percent_complete in range(100):
                time.sleep(0.10)
                progress_bar.progress(percent_complete)

            ppt_path, ppt_name = generate_ppt(topic, theme)
            st.success(f"PPT Slides for '{topic}' created successfully!")

            with open(ppt_path, "rb") as f:
                ppt_bytes = f.read()

            st.download_button(
                label=f"Download {os.path.basename(ppt_path)}",
                data=ppt_bytes,
                file_name=os.path.basename(ppt_path),
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )


if __name__ == "__main__":
    main()
