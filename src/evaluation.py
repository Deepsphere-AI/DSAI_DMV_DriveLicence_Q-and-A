import os
import pdfplumber
import streamlit as st
from openai import OpenAI
import pandas as pd
import json
from dotenv import load_dotenv
load_dotenv()

final_marks = []
final_feedback = []
final_text = []
result = ''
final_result = []


folder_path = r"C:\Users\svikr\OneDrive\Desktop\LVA - Course 4 - FInal Assessment ( Lab)"  # Replace with your folder path
import os
import PyPDF2

def extract_text_from_pdfs(folder_path):
    final_text = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            pdf_text = ''
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"  # Add a newline after each page for better readability
            final_text.append(pdf_text)
    return final_text

# Replace 'your_folder_path' with the path to the folder containing your PDFs
extracted_texts = extract_text_from_pdfs(folder_path)
client = OpenAI(api_key=os.environ["API_KEY"])
thread = client.beta.threads.create()
a = 0
for i in extracted_texts:
    a = a+1
    print(a)
    message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=i)
    run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id="asst_KCsBUwjjEZXxYSTZEGXf3B5D")
    # run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant.id,run_id=run.id)
    
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status=="completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            result = latest_message.content[0].text.value
            break
    print(result)
    final_result.append(result)
    data = [eval(item) for item in final_result]
    df = pd.DataFrame(data)
    excel_file = 'Marks_and_Feedback.xlsx'
    df.to_excel(excel_file, index=False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

            
            
            

            

            
            
