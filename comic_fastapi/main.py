from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from pymongo import MongoClient
from typing import List, Dict
from fastapi.responses import JSONResponse
from ebooklib import epub
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import math
import ebooklib
import os
from google.cloud import firestore
from google.oauth2 import service_account
from typing import List
import tempfile
import uvicorn 
import gunicorn
import requests
import io
import boto3
import re
import base64
import requests
import nltk
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
import openai
nltk.download('punkt')
from pydantic import BaseModel, Field
import nltk
print(nltk.data.path)
app = FastAPI()

chapters_content_global = {}

"""SERVICE_ACCOUNT_FILE = '/Users/anamikabharali/Downloads/Final_Project/comic_fastapi/flowing-perigee-407723-d7fa72ef675f.json'

cred = credentials.Certificate("/Users/anamikabharali/Downloads/Final_Project/comic_fastapi/flowing-perigee-407723-d7fa72ef675f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()"""

"""
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
db = firestore.Client(credentials=credentials, project=credentials.project_id)

db = firestore.Client.from_service_account_json('/Users/anamikabharali/Downloads/Final_Project/comic_fastapi/flowing-perigee-407723-d7fa72ef675f.json')"""



@app.post("/upload-epub/")
async def upload_epub(file: UploadFile = File(...)):
    if not file.filename.endswith('.epub'):
        raise HTTPException(status_code=400, detail="File extension not allowed. Only EPUB files are accepted.")

    # Create a temporary file to store the EPUB file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_file:
        epub_path = temp_file.name
        content = await file.read()  # Read the file content
        temp_file.write(content)  # Write the content to the temp file

    # Read the EPUB file using ebooklib
    book = epub.read_epub(epub_path)

    # Extract chapters content
    chapters_content = extract_chapters(book)

    # Remove the temporary file
    os.unlink(epub_path)

    chapter_titles = list(chapters_content.keys())
    return JSONResponse(content={"chapter_titles": chapter_titles})

  

def extract_chapters(book):
    chapters_content = {}
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):  
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # Find all the header tags that might indicate a chapter start
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            title = header.get_text(strip=True)
            if title:
                chapters_content[title] = soup.get_text(strip=True)
                chapters_content_global[title] = soup.get_text(strip=True)
    return chapters_content

  
@app.post("/segment-chapter/")
async def segment_chapter(chapter_title: str):
    # Check if chapter_title is in chapters_content_global
    if chapter_title not in chapters_content_global:
        available_titles = list(chapters_content_global.keys())
        detail = f"Chapter title not found. Available titles: {available_titles}"
        raise HTTPException(status_code=404, detail=detail)
    
    chapter_content = chapters_content_global[chapter_title]
    segmented_content = segment_chapter_content(chapter_content, chapter_title)
    return JSONResponse(content={"segmented_content": segmented_content})

def segment_chapter_content(chapter_content, chapter_title):
    sentences = sent_tokenize(chapter_content)
    total_sentences = len(sentences)
    part_length = math.ceil(total_sentences / 4)
    parts_dict = {}

    for i in range(4):
        segment_key = f"{chapter_title}-{i+1}"
        start_index = i * part_length
        end_index = start_index + part_length
        parts_dict[segment_key] = ' '.join(sentences[start_index:end_index])

    return parts_dict    


def upload_to_firestore(segmented_data, collection_name):
    try:
        db = firestore.Client()
        for chapter_title, segments in segmented_data.items():
            doc_ref = db.collection(collection_name).document(chapter_title)
            doc_ref.set({'segments': segments})
            print(f"Uploaded data for chapter: {chapter_title}")
        print("Firestore write completed successfully.")
        return True  # Indicates success
    except Exception as e:
        print(f"Firestore write error: {e}")
        return False  # Indicates failure

import certifi
client = MongoClient('mongodb+srv://saniyakapur39:4t7Do4YRshsKRyfl@atlascluster1.gf69eem.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
# Set up MongoDB connection
#client = MongoClient('mongodb+srv://saniyakapur39:4t7Do4YRshsKRyfl@atlascluster1.gf69eem.mongodb.net/?retryWrites=true&w=majority')    
db = client['images_and_prompts']
collection = db['images_prompts']

# Utility function to get data from MongoDB


@app.get("/story/{story_name}/images", response_model=List[str])
async def get_story_images(story_name: str):
    data = get_story_data(story_name)
    if not data:
        raise HTTPException(status_code=404, detail="Story not found")
    return [entry["image_url"] for entry in data if "image_url" in entry]

def get_story_data(story_name: str):
    # Using a regular expression for case-insensitive substring matching
    regex = re.compile(story_name, re.IGNORECASE)
    result = collection.find({"story_name": regex})
    return list(result)  # Converting the cursor to a list
 
@app.get("/story/{story_name}/prompts", response_model=List[str])
async def get_story_prompts(story_name: str):
    data = get_story_data(story_name)
    if not data:
        raise HTTPException(status_code=404, detail="Story not found")
    return [entry["prompt"] for entry in data if "prompt" in entry]

@app.get("/story/{story_name}/alternating")
async def get_story_alternating(story_name: str):
    data = get_story_data(story_name)
    if not data:
        raise HTTPException(status_code=404, detail="Story not found")

    # Generate alternating list of image URLs and prompts
    alternating_list = []
    for entry in data:
        if "image_url" in entry and "prompt" in entry:
            alternating_list.append(entry["image_url"])
            alternating_list.append(entry["prompt"])

    return alternating_list




# Set up OpenAI
os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.getenv('OPENAI_API_KEY')
 
@app.get("/retrieve-data-from-firestore/")
async def retrieve_from_firestore(play_name: str = Query(..., description="Name of the play")):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/anamikabharali/Downloads/Final_Project/comic_fastapi/flowing-perigee-407723-d7fa72ef675f.json"
    cred = credentials.Certificate("/Users/anamikabharali/Downloads/Final_Project/comic_fastapi/flowing-perigee-407723-d7fa72ef675f.json")
    firebase_admin.initialize_app(cred)
    
    db = firestore.Client()
    collection_ref = db.collection('alice-in-wonderland')
    documents = collection_ref.stream()
    parts = []
    for doc in documents:
        if play_name in doc.id:
            parts.append(doc.to_dict().get('segments'))
 
        comic_prompts = []
        for part in parts:
            comic_prompts.extend(get_questions(part))
 
        return {"comic_prompts": comic_prompts}
    

def get_questions(part):
    prompt_output = generate_prompt(part)  # Assuming you have a generate_prompt function

    if not prompt_output:
        return []

    separated_prompts = [prompt.strip() for prompt in re.split(r'\n\d+\. Image prompt: ', prompt_output) if prompt]
    return separated_prompts

def generate_prompt(part):
    # Define your prompt generation logic here
    client = openai.Completion.create(
        engine="text-davinci-003",  # Use a valid engine name for completions
        prompt=f"""this text is a story, how to chunk this text like this when you want to use those chunks to form prompts for image generation to form a comic strip out of the whole text. Give me image prompts in such a way that I can create a sensible comic strip out of those image prompts. Keep it kid-friendly. Give 5 chunks in format: \n 1. Image prompt: "{part}"
2. Image prompt: "Text example"
3. Image prompt: "Text example"\n""",
        temperature=1,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the content of the response
    prompt_output = client.choices[0].text
    return prompt_output

class StoryPrompts(BaseModel):
    prompts: List[str] = Field(...)

@app.post("/stable-diffusion/")
async def stable_diffusion_endpoint(request_data: List[str],story_name: str, steps: int, art_style: str, cfg_scale: int, seed: int):
    try:
        separated_prompts = request_data
        image_number = 1

        for prompt in separated_prompts:
            print(image_number)
            try:
                api_call(prompt, image_number,steps, art_style, cfg_scale, seed, story_name)
            except Exception as e:
                print(f"An error occurred: {e}")
            image_number += 1


        return {"message": "Image generation process started"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

def api_call(prompt, image_number, steps, art_style, cfg_scale, seed, story_name):

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
        "steps": steps,
        "width": 1024,
        "height": 1024,
        "seed": seed,
        "cfg_scale": cfg_scale,
        "samples": 1,
        "style_preset": f"{art_style}",
        "text_prompts": [
        {
            "text": f"{prompt}",
            "weight": 1
        },
        {
            "text": "blurred, bad, disfigured",
            "weight": -1
        }
        ],
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-WQENOrNAra9W9P0YZUKOixOhyJxYpP8yAwyH4gEwrixzgmZT",
}

    response = requests.post(
        url,
        headers=headers,
        json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json() # Repl
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAVDTWAS7LAKLGAFPF'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = []
        for i, image in enumerate(data["artifacts"]):
            file_path = os.path.join(temp_dir, f'{story_name}_badseed_image_{image_number}_{i}.png')
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            s3_client = boto3.client('s3')
            bucket_name = 'comicbucket3'
            s3_client.upload_file(file_path, bucket_name, f'{story_name}_badseed_image_{image_number}_{i}.png')




def prompt_engineering(**kwargs):
    os.environ['OPENAI_API_KEY'] = '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'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    parts = retrieve_from_firestore(**kwargs)

    comic_prompts = []

    client = openai()

    def get_questions(text):

            response = client.chat.completions.create(
            model="gpt-4",
            messages=[
            {
            "role": "system",
            "content": """this text is a story, how to chunk this text like this when you want to use those chunks to form prompts for image generation to form a comic strip out of the whole text. Give me image prompts in such a way that I can create a sensible comic strip out of those image prompts. Keep it kid-friendly. Give 5 chunks in format: \n 1. Image prompt: "Text example"
    2. Image prompt: "Text example"
    3. Image prompt: "Text example"\n"""
            },
            {
            "role": "user",
            "content": f"\"\"\"\n{text}\n\"\"\""
            }
            ],
            temperature=1,
            max_tokens=800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )

            first_choice = response.choices[0]
            message_content = first_choice.message.content

            print("==========")
            print(message_content)

            return message_content


    for part in enumerate(parts):
        comic_prompts.append(get_questions(part))
    
    separated_prompts = [prompt.strip() for text in comic_prompts for prompt in re.split(r'\n\d+\. Image prompt: ', text) if prompt]


    return separated_prompts


class StoreImagesAndPromptsRequest(BaseModel):
    image_folder_path: str
    story_name: str

@app.post("/store-images-and-prompts/")
async def store_images_and_prompts_endpoint(request_data: StoreImagesAndPromptsRequest):
    try:
        image_folder_path = request_data.image_folder_path
        story_name = request_data.story_name

        separated_prompts = prompt_engineering(story_name=story_name)  # You should provide the appropriate parameters here

        """ # Set up MongoDB connection
        client = MongoClient('mongodb+srv://saniyakapur39:4t7Do4YRshsKRyfl@atlascluster1.gf69eem.mongodb.net/?retryWrites=true&w=majority')
        db = client['images_and_prompts']
        collection = db['images_prompts']"""

        # Set up S3 client
        s3_client = boto3.client('s3')
        bucket_name = 'comicbucket3'

        def is_valid_image(filename):
            parts = filename.split('_')
            if len(parts) == 3 and parts[0] == 'image' and parts[2].endswith('.png'):
                try:
                    int(parts[1])
                    return True
                except ValueError:
                    return False
            return False

        image_files = sorted(
            filter(is_valid_image, os.listdir(image_folder_path)),
            key=lambda x: int(x.split('_')[1])
        )

        num_iterations = min(len(image_files), len(separated_prompts))

        for i in range(num_iterations):
            image_file = image_files[i]
            text = separated_prompts[i]
            image_path = os.path.join(image_folder_path, image_file)

            s3_client.upload_file(image_path, bucket_name, image_file)

            image_url = f'https://{bucket_name}.s3.amazonaws.com/{image_file}'

            # Store the reference in MongoDB
            document = {
                'image_name': image_file,
                'prompt': text,
                'image_url': image_url,
                'story_name': story_name
            }
            collection.insert_one(document)

        return {"message": "Images and prompts stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)


