import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):  # Corrected here
        text += str(reader.pages[page].extract_text())  # Extract text from each page
    return text

input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) 
with a deep understanding in accounting, sales, telesales, marketing, social media, mobile developemnt. Your task
is to evaluate the resume based on the given job description. You must consider the job market is 
very competitive and you should provide best assistance for improving the resumes. Assign the 
precentage Matching based on Jd and the missing keywords with high accuracy

resume:{text}
description: {jd}

I want the response in on single string having the structure
{{"JD Match ": "%", "MissingKeywords:[]", "Profile Summary": ""}}
"""

st.title("Smart ATS For Horeca smart ")
st.text("The resume ATS results")
jd = st.text_area("Paste the job Description")
uploaded_files = st.file_uploader("Upload your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_files is not None:
        text = input_pdf_text(uploaded_files)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))  # Make sure to format the prompt with the input text and job description
        st.subheader(response)
