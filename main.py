import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.environ.get("AISTUDIO_API_KEY"))

# Set up the model
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro-vision-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

st.title("Insta Captioner @ SXC")

image_uploaded = st.file_uploader("Upload an Image")

if image_uploaded is not None:
    st.image(image_uploaded)

    if st.button("Generate Caption", type="primary", use_container_width=True):
        prompt_parts = [
            "Generate a short captivating and inspiring Instagram post in one paragraph that resonates with users and encourages them to take positive action. The post should include a compelling message and relevant hashtags to maximize its viral potential and impact in Markdown text format.\n\n",
            {"mime_type": image_uploaded.type, "data": image_uploaded.getvalue()},
            "\n",
        ]

        response = model.generate_content(prompt_parts)
        st.markdown(response.text)
