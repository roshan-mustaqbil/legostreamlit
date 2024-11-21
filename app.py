import streamlit as st
import requests
import io
from PIL import Image

# Set up the API URLs and headers
captioning_api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
image_generation_api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

# Function to query the image captioning API
def query_captioning_api(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    response = requests.post(captioning_api_url, headers=headers, data=data)
    return response.json()

# Function to query the image generation API
def query_image_generation_api(prompt):
    payload = {"inputs": prompt}
    response = requests.post(image_generation_api_url, headers=headers, json=payload)
    return response.content

# Streamlit UI
st.title("AI Image to Lego Minifigure Generator")
st.write("Upload an image to convert it into a Lego minifigure styled image.")

# File uploader for image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    input_image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(input_image, caption='Uploaded Image', use_column_width=True)

    # Save the uploaded image temporarily
    temp_file_path = "temp_image.jpg"
    input_image.save(temp_file_path)

    # Generate prompt from the uploaded image
    with st.spinner("Generating prompt from the uploaded image..."):
        caption_response = query_captioning_api(temp_file_path)
        prompt = caption_response.get("caption", "an image")  # Fallback to a default prompt if captioning fails
    
    st.write(f"Generated Prompt: {prompt}")

    # Modify the prompt for Lego minifigure style
    lego_prompt = f"a lego-minifigurine of {prompt}"
    
    # Generate the Lego minifigure styled image
    if st.button("Generate Lego Minifigure Styled Image"):
        with st.spinner("Generating Lego minifigure styled image..."):
            image_bytes = query_image_generation_api(lego_prompt)
            output_image = Image.open(io.BytesIO(image_bytes))

        # Display the generated image
        st.image(output_image, caption='Generated Lego Minifigure Styled Image', use_column_width=True)

# Note: Remember to handle exceptions and edge cases in production code.