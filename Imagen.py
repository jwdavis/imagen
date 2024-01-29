import re
import streamlit as st

from vertexai.preview.vision_models import ImageGenerationModel
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(
    page_title='ROI Imagen App',
    page_icon='./static/ROISquareLogo.png',
)
    
def get_file_name(prompt, image_number):
    """
    Generate a file name for an image based on the given prompt and image number.

    Args:
        prompt (str): The prompt used to generate the file name.
        image_number (int): The image number.

    Returns:
        str: The generated file name in the format "<prompt>_<image_number>.png".
    """
    no_punct = re.sub(r'[^\w\s]', '', prompt)
    words = no_punct.split()
    first_five_words = words[:2]
    new_string = '_'.join(first_five_words)
    new_string = new_string.lower()
    return f"{new_string}_{image_number}.png"

def show_images(response):
    """
    Display a list of images and provide download buttons for each image.

    Parameters:
    - response: The response object containing a list of images to display.

    Returns:
    None
    """
    if response is None:
        return
    cols = st.columns(len(response.images), gap="small")
    clicks = [None for _ in range(len(response.images))]
    for i, image in enumerate(response.images):
        cols[i].image(image._image_bytes, use_column_width=True)
        clicks[i] = cols[i].download_button(
            label="Download", 
            type="primary",
            data=image._image_bytes,
            file_name=get_file_name(st.session_state['prompt'], i),
            mime="image/png"
        )

def generate_images(prompt):
    """
    Generates images based on the given prompt.

    Args:
        prompt (str): The prompt for generating the images.

    Returns:
        tuple: A tuple containing the generated images and any error that occurred during the generation process.
            The generated images are returned as a response.
            If an error occurs, it is returned as an error dictionary.
    """
    response = None
    error = None
    try:
        # consider implementing base_image
        model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=3,
            guidance_scale=21
        )
    except Exception as e:
        error = {"error": e}
    return response, error

def clear_state():
    """
    Clears all the keys in the session state dictionary.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Generate top of page formatting
st.image(
    "https://www.roitraining.com/wp-content/uploads/2017/02/ROI-logo.png",
    width=300
)
st.title("Google GenAI image creation")
st.markdown(
    """<h5>Please use responsibly and in moderation.
    <a href="https://cloud.google.com/vertex-ai/docs/generative-ai/image/usage-guidelines" 
    target="_blank" rel="noopener noreferrer" style="text-decoration: none;">
    <sup style="font-size: 10px;color:black;vertical-align: middle;">&#9432;</sup></a></h5>""",
    unsafe_allow_html=True,
)
add_vertical_space(1)

last_prompt = st.session_state.get("prompt", None)
col1, col2 = st.columns([0.86, 0.14], gap="small")
with col1:
    if prompt := st.text_input(":sunglasses: What would you like to see?"):
        if prompt != last_prompt:
            clear_state()
            st.session_state["prompt"] = prompt

        if "response" not in st.session_state:
            with st.spinner("Generating images..."):
                response, error = generate_images(prompt)
            if error:
                st.write(f":broken_heart:. {error['error']}")
                st.write("Try a different prompt.")
                st.session_state["prompt"] = ""
                st.stop()
            st.session_state["response"] = response
        else:
            response = st.session_state["response"]
with col2:
    container = st.container()
    st.markdown("<br>", unsafe_allow_html=True)
    st.button(
        label=":arrows_counterclockwise: Rerun",
        on_click=clear_state
    )

add_vertical_space(1)
show_images(st.session_state.get("response", None))