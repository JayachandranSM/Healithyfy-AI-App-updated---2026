from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai 
import os
from PyPDF2 import PdfReader

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.generativeModel("gemini-pro")
    response=model.generative_content(input)
    return response.text


def get_pdf_content(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text
    
prompt_template = """
You are an experienced ATS (Applicant Tracking System) expert. Your task is to evaluate 
candidate profiles (Data Analyst, Data Scientist, Product Manager, HR, Business Analyst) against
a given job description. Analyze and compare the skills, experience, and qualifications listed in
the profiles to the requirements outlined in the job description. Provide a detailed analysis of
each candidate's suitability for the job. You must consider the job market is competitive and you should 
provide the best assistance for improving the resume. Assign the percentage matching based on the JD
and the missing keywords with a high level of accuracy.
resume: {text}
JD: {jd}
"""



st.title('ATS App')
st.text("Improve Your Resume with ATS Assistance")
jd=st.text_area("Copy & Paste The JD here")
uploaded_file = st.file_uploader("Upload Your Resume",type='pdf')
submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=get_pdf_content(uploaded_file)
        response=get_gemini_response(text)
        st.header("The Response is below")
        st.write(response)


