from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai 
import os
from PIL import Image
#from PyPDF2 import PdfReader

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input_prompt,image[0]])
    return response.text


def get_image_content(uploaded_file):
    if uploaded_file is not None:
        image_byte_data=uploaded_file.getvalue()

        image_parts = [
            {   
                "mime_type":uploaded_file.type, 
                "data":image_byte_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded") 
    

st.set_page_config(page_title="FoodAnalyzer")
st.markdown("<h1 style='text-align: center;'>FoodAnalyzer App</h1>", unsafe_allow_html=True)

age = st.number_input("Enter Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Select Gender", options=["Male", "Female", "Other"])
weight = st.number_input("Enter Weight in (kg)", min_value=0.0, step=0.1) 
Height = st.number_input("Enter Height in (cm)", min_value=0.0, step=0.1) 

uploaded_file=st.file_uploader("Upload an Image",type=["jpg","png","jpeg"])   
image=''
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

col1, col2, col3 = st.columns([7, 2, 7])
with col2:
    submit = st.button("Analyze")

input_prompt = f"""
You are an expert nutritionist. Please analyze the food items from the uploaded image and calculate the
total calories. Also provide the details of every food item with calorie intake in the following format:

         1. Item 1 - Number of calories
         2. Item 2 - Number of calories  
         3. Item 3 - Number of calories
         4. Item 4 - Number of calories  
......
......

Also, consider the user inputted {age}, {gender}, {weight}, {Height} and mention whether the food is healthy or not 
for the inputted {age}, {gender}, {weight},{Height}. Additionally, mention the percentage split of the ratio of proteins, carbohydrates, fats, fiber, sugar, minerals, vitamins, and
other important nutrients required in our diet. Do not confuse and show {weight} with {Height} or {Height} with {weight}"""


if submit:
    image_date = get_image_content(uploaded_file)
    response=get_gemini_response(input_prompt,image_date)
    st.subheader("The Response is")
    st.write(response)

    