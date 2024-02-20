import os
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
from bs4 import BeautifulSoup
import re
import requests
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import math
from dotenv import load_dotenv
load_dotenv()
from google.cloud import firestore






dag = DAG(
    dag_id="sandbox",
    schedule="0 0 * * *",   
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["labs", "damg7245"],
)

def data_scraping():
  url = 'https://www.gutenberg.org/files/1430/1430-h/1430-h.htm'
  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')
  text = soup.get_text()
  textfull=text

  # Step 1: Find the position of "CONTENTS"
  contents_pos = text.find("CONTENTS")

  # Step 2: Extract the text after "CONTENTS"
  # We add len("CONTENTS") to start after the word "CONTENTS", and we assume a certain number of characters to capture, which you may need to adjust
  stories_text = text[contents_pos + len("CONTENTS"):].strip()

  # Step 3: Split the text to get individual story names
  # Assuming each story name is separated by a newline character
  story_names = stories_text.split('\n')

  # Remove any empty lines or irrelevant lines after the story names
  # This step may need adjustment based on the actual format of your text
  story_names = [name for name in story_names if name.strip() and 'other identifying feature of non-story text' not in name]

  # Now story_names contains the list of story names
  story_names = story_names[2:22]

  pos = text.find("PLATES")
  textafter = ""

  #if pos != -1:  # Check if the phrase was found
  textafter = text[pos:]
  content=textafter

  # A dictionary to store the sections, using story names as keys
  story_sections = {}
  prev_name = None

  for name in story_names:
      # Escape any special characters in the story name
      escaped_name = re.escape(name)

      if prev_name:
          # Split the text at the current story name and get the latter part for further splitting
          parts = re.split(escaped_name, textafter, maxsplit=1)
          textafter = parts[1] if len(parts) > 1 else ""
          story_sections[prev_name] = parts[0].strip()
      prev_name = name

  # Add the last section after the final story name
  story_sections[prev_name] = textafter.strip()

  for story, content in story_sections.items():
      print(f"Story: {story}")
      print("Content:")
      print(content[:100])  # Printing the entire content of the story
      print("\n---\n")  # Adding a separator for readability

  # Remove "Story Name 1" using del
  if "A MIDSUMMER NIGHT'S DREAM" in story_sections:
      del story_sections["A MIDSUMMER NIGHT'S DREAM"]

  if "ALL'S WELL THAT ENDS WELL" in story_sections:
      del story_sections["ALL'S WELL THAT ENDS WELL"]
  
  selected_keys = ['THE TEMPEST', "AS YOU LIKE IT", 'ROMEO AND JULIET', 'MACBETH', 'THE COMEDY OF ERRORS']

  # Creating the new dictionary with only the selected keys
  final_story = {k: story_sections[k] for k in selected_keys if k in story_sections}

  return final_story


def segmentation():
    parts_dict = {}
    original_dict = data_scraping()
    for key, value in original_dict.items():
        sentences = sent_tokenize(value)
        # Determining the length of each part
        total_sentences = len(sentences)
        part_length = math.ceil(total_sentences / 4)

        # Dividing the sentences into four parts
        parts = [sentences[i:i + part_length] for i in range(0, total_sentences, part_length)]
        for i in range(0,4):
            new_key = f'{key}-Part{i+1}' 
            parts_dict[new_key] = parts[i]
    
    return parts_dict
  
  

def upload_to_firestore():
    db = firestore.Client()
    segmented_data = segmentation()  # Call your segmentation function

    for play_name, segments in segmented_data.items():
        doc_ref = db.collection('plays').document(play_name)
        doc_ref.set({'segments': segments})

with dag:
    data_scraping_task = PythonOperator(
        task_id="data_scraping",
        python_callable=data_scraping,
        dag=dag,
    )

    segmentation_task = PythonOperator(
        task_id='segmentation',
        python_callable=segmentation,
        dag=dag,
    )

    upload_to_firestore_task = PythonOperator(
        task_id='upload_to_firestore',
        python_callable=upload_to_firestore,
        dag=dag,
    )

    bye_world_task = BashOperator(
        task_id="bye_world",
        bash_command='echo "Bye from airflow"'
    )

    data_scraping_task >> segmentation_task >> upload_to_firestore_task >> bye_world_task
