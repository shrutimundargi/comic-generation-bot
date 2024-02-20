from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
import openai
from openai import OpenAI
import requests
import base64
import re
from pymongo import MongoClient
from google.cloud import storage
import os
from google.cloud import firestore
import boto3



user_input = {
    "play_name": Param(default="MACBETH", type='string', minLength=5, maxLength=255),
}

dag = DAG(
    dag_id="sandbox",
    schedule="0 0 * * *",   
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["labs", "damg7245"],
    params=user_input,
)

def retrieve_from_firestore(**kwargs):
    db = firestore.Client()
    collection_ref = db.collection('plays')  
    documents = collection_ref.stream()

    chapter_name = kwargs["params"]["play_name"]
    parts = []
    for doc in documents:
        if chapter_name in doc.id:
            parts.append(doc.to_dict().get('segments'))
            print(f'Matching {doc.id} => {doc.to_dict()}')
        else:
            print(f'Non-matching {doc.id}')
    return parts

def prompt_engineering(**kwargs):
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
    openai.api_key = os.getenv('OPENAI_API_KEY')
    parts = retrieve_from_firestore(**kwargs)

    comic_prompts = []

    client = OpenAI()

    def get_questions(text):

            response = client.chat.completions.create(
            model="gpt-4",
            messages=[
            {
            "role": "system",
            "content": """this text is a story, how to chunk this text like this when you want to use those chunks to form prompts for image generation to form a comic strip out of the whole text. Give me image prompts in such a way that I can create a sensible comic strip out of those image prompts. Keep it kid-friendly. Give 5 chunks exactly in format: \n "1. Image prompt: Text example 2. Image prompt: Text example 3. Image prompt: Text example..."\n"""
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

def api_call(prompt, image_number):

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "style_preset": "fantasy-art",
        "text_prompts": [
        {
            "text": f"{prompt}",
            "weight": 1
        },
        {
            "text": "blurred, bad, disfigured, black and white",
            "weight": -1
        }
        ],
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": os.getenv("SD_KEY"),
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    
    # make sure the out directory exists
    if not os.path.exists("/opt/airflow/dags/out"):
        os.makedirs("/opt/airflow/dags/out")

    for i, image in enumerate(data["artifacts"]):
        with open(f'/opt/airflow/dags/out/image_{image_number}_{i}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))


def stable_diffusion(**kwargs):
    separated_prompts = prompt_engineering(**kwargs)
    image_number = 1
    
    for prompt in separated_prompts:
        print(image_number)
        try:
            api_call(prompt, image_number)    
        except Exception as e:
            print(f"An error occurred: {e}")
        image_number += 1


def store_images_and_prompts(**kwargs):
    image_folder_path = "/opt/airflow/dags/out"
    separated_prompts = prompt_engineering(**kwargs)

    # Set up MongoDB connection
    client = MongoClient('')
    db = client['images_and_prompts']
    collection = db['images_prompts']

    # Set up S3 client
    s3_client = boto3.client('s3')
    bucket_name = ''

    def is_valid_image(filename):
        parts = filename.split('_')
        if len(parts) == 3 and parts[0] == 'image' and parts[2].endswith('.png'):
            try:
                int(parts[1])
                return True
            except ValueError:
                return True
        return True

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
            'story_name': kwargs["params"]["play_name"] # Storing the URL of the image
        }
        collection.insert_one(document)





with dag:
    retrieve_from_firestore_task = PythonOperator(
        task_id="retrieve_from_firestore",
        python_callable=retrieve_from_firestore,
        dag=dag,
    )

    prompt_engineering_task = PythonOperator(
        task_id="prompt_engineering",
        python_callable=prompt_engineering,
        dag=dag,
    )

    stable_diffusion_task = PythonOperator(
        task_id='stable_diffusion',
        python_callable=stable_diffusion,
        dag=dag,
    )

    store_images_and_prompts_task = PythonOperator(
        task_id='store_images_and_prompts',
        python_callable=store_images_and_prompts,
        dag=dag,
    )

    

    bye_world_task = BashOperator(
        task_id="bye_world",
        bash_command='echo "Bye from airflow"'
    )

    retrieve_from_firestore_task >> prompt_engineering_task >> stable_diffusion_task >> store_images_and_prompts_task >> bye_world_task






