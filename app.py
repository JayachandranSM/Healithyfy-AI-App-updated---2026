from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as pdf

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    # Debugging: Print the response to understand its structure
    print(response)  # Check what type `response` is and how to access its attributes
    return response.text  # Assuming `.text` is the correct way to access the generated text

def get_pdf_content(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

input_prompt = """
You act like a skilled or very experienced ATS (Applicant Tracking System) with deep understanding of tech field
software engineering, Data Analyst, Data Science, big data engineer, Product Manager, HR and Business Analyst. Your task is to evaluate the resume
based on the given job description. You must consider the job market is very competitive and you should 
provide best assistance for improving the resume. Assign the percentage matching based on the JD
and the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure 
{{"JD Match":%, "MissingKeywords":[],"Profile Summary":""}}
"""

st.title('ATS App')
st.text("Improve Your Resume with ATS Assistance")
jd = st.text_area("Copy & Paste The JD here")
uploaded_file = st.file_uploader("Upload Your Resume", type='pdf', help='Please upload the pdf')

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = get_pdf_content(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader("The Response is below")
        st.write(response)
