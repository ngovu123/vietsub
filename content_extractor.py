def extract_contents_from_text(text):
    lines = text.strip().split('\n')
    slides = []
    current_slide = []
    current_content = ""
    recording_content = False

    for line in lines:
        line = line.strip()
        if line.startswith('#Slide:'):
            if current_slide:
                if recording_content:
                    current_slide.append(current_content.strip())
                    recording_content = False
                slides.append(current_slide)
            current_slide = []
        elif line.startswith('#Content:'):
            if recording_content:
                current_slide.append(current_content.strip())
            current_content = ""
            recording_content = True
        elif recording_content:
            if line.startswith('#Slide:'):
                recording_content = False
                current_slide.append(current_content.strip())
                current_content = ""
                slides.append(current_slide)
                current_slide = []
            else:
                current_content += line + '\n'

    if recording_content:
        current_slide.append(current_content.strip())
    if current_slide:
        slides.append(current_slide)
    
    return slides

# Example usage:
# with open('Cache/custom_prompt.txt', 'r', encoding='utf-8') as f:
#     text = f.read()
# slides = extract_contents_from_text(text)
# for idx, slide in enumerate(slides, 1):
#     print(f"Slide {idx} Contents:")
#     for content in slide:
#         print(content)
#     print("\n")
