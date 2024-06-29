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
        raise FileNotFoundEroor("File not uploaded") 

st.header("Healthify App")  
uploaded_file=st.file_uploader("Upload an Image",type=["jpg","png","jpeg"])   
image=''
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Upload Image", use_column_width=True)

submit=st.button("Click here to know total calories of the uploaded image")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the uploaded image
and calculate the total calroies, also provide the details of every food items with calories intake
in the below formt

     1. Item 1 - No of calories
     2. Item 2 - No of calories  
......
......

finally you can also mention whethere the food is healthy or not and also
mention the percentage split of the ratio of protains,carbohydrates,fats,fiber,sugar,minerals,vitamins and
other import things required in our diet
"""

if submit:
    image_date = get_image_content(uploaded_file)
    response=get_gemini_response(input_prompt,image_date)
    st.markdown("The Response is")
    st.write(response)