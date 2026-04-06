import os
import time
import streamlit as st
from streamlit.runtime.secrets import StreamlitSecretNotFoundError # Add this line
from PIL import Image
from dotenv import load_dotenv
# Use the new SDK
from google import genai 
from google.genai import types
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

# Initialize the new Client
#client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 1. Try to get the key from Streamlit Secrets (Cloud)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError, StreamlitSecretNotFoundError):
    # 2. If Secrets fail (Local), fall back to .env
    api_key = os.getenv("GOOGLE_API_KEY")

# 3. Final check: If still no key, show a friendly error
if not api_key:
    st.error("🔑 API Key not found! Please check your .env file locally or Streamlit Secrets in the Cloud.")
    st.stop()

# Initialize the Client
client = genai.Client(api_key=api_key)
def get_gemini_response_with_retry(input_prompt, image_file, retries=3):
    # Use the current stable model: gemini-2.5-flash
    model_id = "gemini-2.5-flash" 
    
    for i in range(retries):
        try:
            # New SDK syntax: client.models.generate_content
            response = client.models.generate_content(
                model=model_id,
                contents=[input_prompt, image_file]
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                st.warning(f"Rate limit hit. Retrying in {2**i} seconds...")
                time.sleep(2**i)
                continue
            raise e
    return "Error: Quota exhausted."

st.set_page_config(page_title="🥗 Healthify AI app updated 2026", layout="centered")
st.header("Healthify App")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # We can pass the PIL image directly to the new SDK
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("Calculate Calories")

input_prompt = """
You are an expert nutritionist. Identify food items and calculate calories.
Format:
1. Item - Calories
Check if it's healthy and provide a % split of Macros (Protein, Carbs, Fats).
"""

if submit:
    if uploaded_file is not None:
        with st.spinner("Analyzing with Gemini 2.5..."):
            try:
                # The new SDK handles the image object directly much easier
                response = get_gemini_response_with_retry(input_prompt, image)
                st.subheader("The Analysis:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please upload an image!")