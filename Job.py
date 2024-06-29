from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as pdf

# Ensure that the API key is retrieved correctly
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key is missing. Please set it in the .env file.")

genai.configure(api_key=api_key)

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text  # Assuming `.text` is the correct way to access the generated text

def get_pdf_content(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

input_prompt1 = """
 You are an experienced HR manager,your task is to review the provided resume against the given job description. 
 Please share your professional evaluation on whether the resume aligns with the job description. 
 Highlight the strengths and weaknesses of the resume in relation to the specified job description.
 resume: {text}
 job description: {jd}
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any of the following roles 
software engineering or Data Analyst or Data Science or big data engineer or  Product Manager or HR or Business Analyst
and ATS functionality as well. Your task is to give the percentage of match if the resume matches to the job description with 
a high accuracy rate.First output the percentage match then followed by list of keywords that are missing.
Also, your need to evaluate the resume against the provided job description.further, provide recommendations for 
enhancing the candidate's skills and identify which areas require further development.
resume: {text}
job description: {jd}
"""

st.title('ATS App')
st.text("Improve Your Resume with ATS Assistance")
jd = st.text_area("Copy & Paste The JD here")
uploaded_file = st.file_uploader("Upload Your Resume in Pdf Only", type='pdf', help='Please upload the pdf')

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Summarize About the Resume & Sugges to improvise skills")

submit2 = st.button("Percentage match & Important Keywords Missing?")

if submit1:
    if uploaded_file is not None:
        text = get_pdf_content(uploaded_file)
        prompt = input_prompt1.format(text=text, jd=jd)
        response = get_gemini_response(prompt)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

if submit2:
    if uploaded_file is not None:
        text = get_pdf_content(uploaded_file)
        prompt = input_prompt2.format(text=text, jd=jd)
        response = get_gemini_response(prompt)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
