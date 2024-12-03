import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from gradio_client import Client
import json

def generate(outline, characters, settings):
    prompt = f"""Hello! I would like to request a 4-paragraph and 700-word per paragraph story and a cover image prompt for sd3 in JSON format described later in the prompt with the following detailed outline:\n\n{outline}\n\nCharacters: {characters}\n\nSettings: {settings}\n\nPlease generate the story with the following detailed JSON format: p1, p2, p3, p4: Keys for story paragraphs; title: Key for story title; prompt: for the cover image its value is the image prompt nothing else. Please do not include any other text in the output. Thank you. Only the JSON is needed or it will break the whole system and make us lose 10 million dollars. Please don't say 'Full response: Here is the requested output in JSON format:' or 'Here is the full response.' Only JSON. If you give plain text, it will not work and count as an error and we will lose customers. Please do not give text. You are not ChatGPT. Don't say 'Here is the full JSON.' You are not an assistant; you are used by an AI. Thank you.\n\n"""

    client = Client("Be-Bo/llama-3-chatbot_70b")
    try:
        hikaye = client.predict(
            message=prompt,
            api_name="/chat"
        )
        return hikaye
    except Exception as e:
        st.error(f"Error generating story: {e}")
        return None

def cover(prompt, api_key):
    model = "mann-e/Mann-E_Turbo"
    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    data = {"inputs": prompt}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        if response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower():
            image = Image.open(BytesIO(response.content))
            return image
        else:
            st.error("Failed to fetch a valid cover image.")
            return None
    except Exception as e:
        st.error(f"Error generating cover image: {e}")
        return None

def parse_story_response(response):
    title = response.get('title', 'Untitled')
    p1 = response.get('p1', 'Paragraph 1 not available.')
    p2 = response.get('p2', 'Paragraph 2 not available.')
    p3 = response.get('p3', 'Paragraph 3 not available.')
    p4 = response.get('p4', 'Paragraph 4 not available.')
    prompt = response.get('prompt', '')
    
    return title, p1, p2, p3, p4, prompt

# Streamlit UI
st.title('Story Generator by Vishal')

api_key = st.text_input("Enter your API Key",
