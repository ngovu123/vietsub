import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from pptx import Presentation
from Cache.default_prompt import prompt
from content_extractor import extract_contents_from_text
from layout_report_tool import supporting_parameters

load_dotenv()
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found. Please set it in your environment variables.")

genai.configure(api_key=api_key)

def get_bot_response(topic: str, theme: str) -> tuple:
    """
    Generates a PowerPoint presentation based on the provided topic and theme.

    Parameters:
    topic (str): The topic for the presentation.
    theme (str): The theme for the presentation.

    Returns:
    tuple: A tuple containing the path to the generated PowerPoint file and the filename.
    """
    user_text = topic
    input_string = re.sub(r'[^\w\s.\-\(\)]', '', user_text).replace("\n", "")
    number = int(theme)

    if number not in range(1, 10):
        number = 1

    filename_prompt = f"Generate a short, descriptive filename based on the following input: \"{user_text}\"."
    
    # Sử dụng API một cách chính xác
    response = genai.generate_text(filename_prompt)  # Hoặc phương thức phù hợp
    filename = response.text.replace(" ", "_")
    pptx_file_name = f"{filename}.pptx"
    pptx_file_path = f"myapp/static/presentations/{pptx_file_name}"

    presentation = Presentation()
    layout_indices, layout_indices_, index_content_placeholders = supporting_parameters(theme)

    for i, content_placeholder_indices in enumerate(index_content_placeholders):
        slide = presentation.slides.add_slide(presentation.slide_layouts[layout_indices[i]])
        slide.shapes.title.text = topic
        
        for index in content_placeholder_indices:
            content_prompt = prompt(input_string, index)
            response = genai.generate_text(content_prompt)  # Hoặc phương thức phù hợp
            slide_content = response.text or "No content generated."
            slide.shapes[index].text = slide_content

    presentation.save(pptx_file_path)
    return pptx_file_path, pptx_file_name
