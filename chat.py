import vertexai
import streamlit as st
import datetime
import os
from PIL import Image
from io import BytesIO
from vertexai.preview.vision_models import ImageGenerationModel

model = ImageGenerationModel.from_pretrained("imagegeneration@002")

# Display the page title
st.title("Image generation using Imagen2")

# The welcome message that is displayed to the user when they first open the app
# The chat_message component formats the display with background colors
# and Avatars appropriate for the entity that provided the text

with st.chat_message("assistant"):
    welcome = "Welcome to the image generation app. Please use responsibly"
    st.markdown(f"{welcome}")

# Gets the user's prompt and displays it in the chat area
if prompt := st.chat_input("What would you like to create?"):
    with st.chat_message("user"):
        st.markdown(prompt)

        response = model.generate_images(
            prompt=prompt,
            number_of_images=3
        )
        for i, image in enumerate(response.images):
            st.image(image._image_bytes, width=300, caption="Generated Image")
            st.download_button(
                label="Download Image",
                data=image._image_bytes,
                file_name=f"generated_image_{i+1}.png",
                mime="image/png"
            )