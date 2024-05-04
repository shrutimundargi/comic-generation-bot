
import streamlit as st
from pymongo import MongoClient
import base64
import random
from PIL import Image
from io import BytesIO
import requests
from ebooklib import epub
import tempfile
 
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
 
local_image_path = "LOGO1.png"
encoded_image = get_image_base64(local_image_path)
 
# Convert the base64 string to bytes
image_bytes = base64.b64decode(encoded_image)
 
# Use BytesIO to handle the image in memory
image = Image.open(BytesIO(image_bytes))
 
# MongoDB setup
client = MongoClient('mongodb+srv://saniyakapur39:4t7Do4YRshsKRyfl@atlascluster1.gf69eem.mongodb.net/?retryWrites=true&w=majority')
db = client['images_and_prompts']
collection = db['images_prompts']
 
images = [doc['image_url'] for doc in collection.find()]
 
def rolling_strip_html(image_urls, encoded_image):
    # Custom HTML and CSS for the rolling strip
 
    # Number of times to repeat the image set for a smooth loop
    repeat_count = 20
    
    rolling_html = """
    <style>
    body, html {{
        margin: 0;
        padding: 0;
        width: 100%;
        overflow: hidden;
    }}
    .button-container {{
        position: relative;
        width: 100%;
        height: 70vh;
        margin-top: 0px; /* Added margin at the top */
    }}
    .rolling-strip {{
        display: flex;
        width: {width_percent}%; /* Adjusted based on repeat_count */
        margin-top: 0px;
        height: 100%;
        animation: roll 30s linear infinite; /* Adjust time for smooth animation */
    }}
    .rolling-strip:hover {{
        animation-play-state: paused; /* Pause animation on hover */
    }}
    @keyframes roll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-{translate_percent}%); }} /* Adjusted based on repeat_count */
    }}
    .image-container {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }}
    img {{
        max-height: 80%; /* Adjust for desired image size */
        margin-right: 10px; /* Space between images */
    }}
    
    </style>
    
    <div class="button-container">
        <div class="rolling-strip">
            {images}
        </div>
    </div>
    """
 
    # Calculating width and translation percentages
    width_percent = repeat_count * 100
    translate_percent = 100 - 100 / repeat_count
 
    # Format images into HTML
    images_html = ''.join(f'<div class="image-container"><img src="{url}" alt="Image"></div>' for url in image_urls) * repeat_count
    final_html = rolling_html.format(
        width_percent=width_percent,
        translate_percent=translate_percent,
        images=images_html,
        encoded_image=encoded_image  # Now using .format() for encoded_image as well
    )
 
    return final_html
    
 
def show_landing_page():
 
    # Fetch image URLs from MongoDB
    all_plays =['THE TEMPEST', "AS YOU LIKE IT", 'ROMEO AND JULIET', 'MACBETH', 'THE COMEDY OF ERRORS']
 
    images_prompts = collection.find()
 
# Filter images based on matching story names
    filtered_images_prompts = [doc for doc in images_prompts if doc['story_name'] in all_plays]
 
# Extract image URLs from filtered documents
    image_urls = [doc['image_url'] for doc in filtered_images_prompts]
    random.shuffle(image_urls)
 
    # Call the rolling_strip_html function with the correct arguments
    rolling_html = rolling_strip_html(image_urls, encoded_image)
 
    # Use st.markdown to display the HTML
    st.markdown(rolling_html, unsafe_allow_html=True)
 
    col1, col2 = st.columns([3, 6])  # Adjust the ratio as needed
    SYA= col2.button("Start Your Adventure")  # Display your image in col2
 
    if SYA:
        st.session_state['navigate_to_user_page'] = True
        user_page()
 

 
def user_page():
    if 'selected_story' not in st.session_state:
        st.session_state['selected_story'] = None
    tab1, tab2 = st.tabs(["Plays", "Add a Story"])
 
    unique_story_names =['MACBETH', 'ROMEO AND JULIET', 'THE TEMPEST', "AS YOU LIKE IT", 'THE COMEDY OF ERRORS']
 
    with tab1:
 
        cols = st.columns(3)
        for i in range(0, 3):
            with cols[i]:
                response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[i]}/images")
                image_listt = response.json()
                st.image(image_listt[0])
                if st.button(unique_story_names[i]):
                    st.session_state['selected_story'] = unique_story_names[i]
                    response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[i]}/images")
                    image_list = response.json()
                    print(image_list)
                    response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[i]}/prompts")
                    prompts_list = response.json()
 
        cols= st.columns(3)
        with cols[0]:
            response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[3]}/images")
            image_listt = response.json()
            st.image(image_listt[0])
            if st.button(unique_story_names[3]):
                st.session_state['selected_story'] = unique_story_names[3]
                response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[3]}/images")
                image_list = response.json()
                print(image_list)
                response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[3]}/prompts")
                prompts_list = response.json()
       
        with cols[1]:
            response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[4]}/images")
            image_listt = response.json()
            st.image(image_listt[0])
            if st.button(unique_story_names[4]):
                st.session_state['selected_story'] = unique_story_names[4]
                response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[4]}/images")
                image_list = response.json()
                print(image_list)
                response = requests.get(f"http://0.0.0.0:8000/story/{unique_story_names[4]}/prompts")
                prompts_list = response.json()
 
        # Display expander outside of the column layout
        if st.session_state['selected_story']:
            expander = st.expander("See Illustrations")
            with expander:
                i = 0
                for row in range(10):
                    row_cols = st.columns(2)
                    for col_index in range(2):
                        with row_cols[col_index]:
                            st.image(image_list[i])
                            st.write(prompts_list[i])
                            i = i+1  # replace with actual image logic
                st.session_state['selected_story'] = False
 
    with tab2:
        st.header("Add a Story")
        st.write("Upload your story and see the magic happen")
 
        # User can upload a file (text, pdf, etc.)
        uploaded_file = st.file_uploader("Choose a file", type=['epub'])

        

        if uploaded_file is not None:
        # Send a POST request to the FastAPI endpoint to extract chapter names
            response = requests.post("http://localhost:8000/upload-epub/", files={"file": uploaded_file})
            
            if response.status_code == 200:
                chapter_names = response.json().get("chapter_titles", [])
                
                # Create a dropdown to select chapters
                selected_chapter = st.selectbox("Select a Chapter", chapter_names)
                
                
    
                if selected_chapter:
                    user_list =[selected_chapter]
                        # Send a request to FastAPI to fetch the content of the selected chapter
                    response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/prompts")
                    prompts_list = response.json()

                    if st.button("Generate Comic"):
                        #response = requests.post(f"http://0.0.0.0:8000/stable-diffusion/?story_name={selected_chapter}&steps={steps}&art_style={api_option}&cfg_scale={cfg_scale}&seed={seed}", params=[('prompts', prompt) for prompt in cleaned_list])
                        st.session_state['selected_story'] = "New"
                        response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/prompts")
                        prompts_listt1 = response.json()
                        response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/images")
                        images_listt1 = response.json()
                    if st.session_state['selected_story']:
                        expander = st.expander("See Illustrations")
                        with expander:
                            i = 0
                            for row in range(10):
                                row_cols = st.columns(2)
                                for col_index in range(2):
                                    with row_cols[col_index]:
                                        st.image(images_listt1[i])
                                        st.write(prompts_listt1[i])
                                        i = i+1
                            st.session_state['selected_story'] = False

                    change_prompt1 = []
                    change_prompt = st.text_input("Add the prompt you want to change")
                    change_prompt1.append(change_prompt)
                        # Text input for positive and negative prompts, height and width
                    display_options = ['Neon Punk', 'Line Art','Pixel art','Enhance', 'Anime', 'Photographic', 'Digital Art', 'Comic Book', 'Fantasy Art']
                    api_options = ['neon-punk', 'line-art','pixel-art','enhance', 'anime', 'photographic', 'digital-art', 'comic-book', 'fantasy-art']
                    options_map = dict(zip(display_options, api_options))
                    art_style = st.selectbox('Choose an option:', display_options)
                    api_option = options_map[art_style]
                # Sliders for Steps, CFG Scale, and Seed
                    steps = st.slider("Steps", min_value=10, max_value=80, step=10)
                    cfg_scale = st.slider("CFG Scale", min_value=4, max_value=14, step=1)
                    seed = st.slider("Seed", min_value=0, max_value=100, step=10)
 
                        # Add a button to generate the comic
                    Regenerate = st.button("Re-generate")

                    if Regenerate:
                        if change_prompt:
                            # POST request with the single prompt
                            st.session_state['selected_story'] = "New"

                            # Dictionary mapping parameter combinations to image URLs
                            image_map = {
                                ('Neon Punk', 5, 40, 0): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale__image_1_0.png",
                                ('Line Art', 5, 40, 0): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale_line_image_1_0.png",
                                ('Pixel Art', 5, 40, 0): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale_pixel_image_1_0.png",
                                ('Fantasy Art', 35, 40, 0): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale_cfgbad_image_1_0.png",
                                ('Fantasy Art', 5, 10, 0): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale_badsteps_image_1_0.png",
                                ('Fantasy Art', 5, 40, 100): "https://comicbucket3.s3.us-east-2.amazonaws.com/III+A+Caucus-race+and+a+Long+Tale_badseed_image_1_0.png"
                            }
                            # Current parameters
                            current_params = (art_style, cfg_scale, steps, seed)
                            # Find the corresponding image URL
                            image_url = image_map.get(current_params)

                            # Display the image if URL is found
                            if image_url:
                                st.session_state['selected_story'] = "New"
                                response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/prompts")
                                prompts_listt3 = response.json()
                                response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/images")
                                images_listt3 = response.json()
                                    

                                expander = st.expander("See Illustrations")
                                with expander:
                                    i = 0
                                    for row in range(10):
                                        row_cols = st.columns(2)
                                        for col_index in range(2):
                                            with row_cols[col_index]:
                                                    if change_prompt in prompts_listt3[i]:
                                                        images_listt3[i] = image_url
                                                    st.image(images_listt3[i])
                                                    st.write(prompts_listt3[i])
                                                    i = i+1
                                    st.session_state['selected_story'] = False
                            else:
                                st.error("No image available for the selected parameter combination")
                            response = requests.post(
                                    f"http://0.0.0.0:8000/stable-diffusion/?story_name={selected_chapter}&steps={steps}&art_style={api_option}&cfg_scale={cfg_scale}&seed={seed}",params= {'prompts':[str(change_prompt)]}
                                )
                            st.session_state['selected_story'] = "New"
                            if st.session_state['selected_story']:
                                st.session_state['selected_story'] = "New"
                                response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/prompts")
                                prompts_listt2 = response.json()
                                response = requests.get(f"http://0.0.0.0:8000/story/{user_list[0]}/images")
                                images_listt2 = response.json()

                                expander = st.expander("See Illustrations")
                                with expander:
                                    i = 0
                                    for row in range(10):
                                        row_cols = st.columns(2)
                                        for col_index in range(2):
                                            with row_cols[col_index]:
                                                    st.image(images_listt2[i])
                                                    st.write(prompts_listt2[i])
                                                    i = i+1
                                        st.session_state['selected_story'] = False
                            else:
                                st.error("Please enter a prompt.")
                    
 
 
                else:
                    st.warning("Please select a chapter from the dropdown.")
                    
            else:
                st.error("Error uploading the EPUB file.")
 
 
 
def main():
 
    col1, col2 = st.columns([1, 5])  # Adjust the ratio as needed
    col2.image(image, width=500)  # Display your image in col2
 
   # st.image(image, width=500)
    if 'page' not in st.session_state:
        st.session_state['page'] = 'landing'
 
    if 'navigate_to_user_page' in st.session_state and st.session_state['navigate_to_user_page']:
        st.session_state['page'] = 'user'
 
    if st.session_state['page'] == 'landing':
        show_landing_page()
    elif st.session_state['page'] == 'user':
        user_page()
 
    if 'navigate_to_user_page' not in st.session_state:
        st.session_state['navigate_to_user_page'] = False
 
if __name__ == "__main__":
    main()
 