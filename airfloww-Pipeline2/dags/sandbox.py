import os
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import math
from google.cloud import firestore




user_input = {
    "epub_path": Param(default="/opt/airflow/dags/pg64317.epub", type='string', minLength=5, maxLength=255),
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

def file_reader(**kwargs):
    epub_path = kwargs["params"]["epub_path"]
    book = epub.read_epub(epub_path)

    chapters_content = {}
    # Iterate through each item in the EPUB file
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # Find all the header tags that might indicate a chapter start
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            title = header.get_text(strip=True)
            if title:
                chapters_content[title] = soup.get_text()

    # Now chapters_content has all chapters' text indexed by their title
    return chapters_content

def segmentation(**kwargs):
    parts_dict = {}
    original_dict = file_reader(**kwargs)

    # Extracting book name from the epub_path
    epub_path = kwargs["params"]["epub_path"]
    book_name = os.path.splitext(os.path.basename(epub_path))[0].replace(' ', '_')

    book = epub.read_epub(epub_path)
    index_headings = ['contents', 'chapters', 'index']  # Common index page headings
    chapter_titles = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            if any(heading in soup.text.lower() for heading in index_headings):
                links = soup.find_all('a')
                for link in links:
                    chapter_title = link.get_text().strip()
                    if chapter_title:
                        chapter_titles.append(chapter_title)
                break

    for key, value in original_dict.items():
        if key in chapter_titles:
            sentences = sent_tokenize(value)
            total_sentences = len(sentences)
            part_length = math.ceil(total_sentences / 4)

            for i in range(4):
                segment_key = f"{book_name}-{key}-{i+1}"
                start_index = i * part_length
                end_index = start_index + part_length
                parts_dict[segment_key] = ' '.join(sentences[start_index:end_index])

    return parts_dict


def upload_to_firestore(**kwargs):
    db = firestore.Client()
    segmented_data = segmentation(**kwargs)  # Call your segmentation function

    for chapter_title, segments in segmented_data.items():
        doc_ref = db.collection('collection').document(chapter_title)
        doc_ref.set({'segments': segments})

with dag:
    file_reader_task = PythonOperator(
        task_id="file_reader",
        python_callable=file_reader,
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

    file_reader_task >> segmentation_task >> upload_to_firestore_task >> bye_world_task
