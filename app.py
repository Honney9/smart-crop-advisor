import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# --- Configure Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Streamlit page settings ---
st.set_page_config(page_title="🌾 Smart Crop Advisor", page_icon="🌱", layout="centered")
st.title("🌾 Smart Crop Advisory Chatbot")

st.write(
    "Welcome! 👋 I’m your Smart Crop Advisor. "
    "Enter your location, soil and weather conditions, and I’ll suggest suitable crops "
    "and farming practices."
)

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please check your .env file.")
else:
    st.success("✅ Google API Key loaded successfully!")

# --- Input form ---
with st.form("crop_form"):
    location = st.text_input("📍 Enter your location (e.g., Odisha, India)")
    soil_type = st.selectbox(
        "🌱 Select soil type",
        ["Clay", "Sandy", "Loamy", "Black", "Laterite", "Red", "Other"],
    )
    rainfall = st.number_input("🌧️ Average annual rainfall (in mm)", min_value=0, max_value=2000, value=800)
    temperature = st.number_input("🌡️ Average temperature (°C)", min_value=0, max_value=50, value=30)
    soil_ph = st.number_input("🧪 Soil pH level", min_value=0.0, max_value=14.0, value=7.0)
    submit = st.form_submit_button("Get Advice")

# --- When user submits ---
if submit:
    with st.spinner("Analyzing conditions..."):
        prompt = f"""
        You are an expert crop advisor.
        Suggest the top 3 most suitable crops for the following conditions:
        - Location: {location}
        - Soil type: {soil_type}
        - Average rainfall: {rainfall} mm
        - Average temperature: {temperature}°C
        - Soil pH: {soil_ph}

        For each crop, provide:
        1. Crop name
        2. Recommended variety (if any)
        3. Basic fertilizer (NPK) guidance
        4. Ideal planting time
        5. Common pest/disease to watch out for

        Give concise, practical advice in a farmer-friendly tone.
        """

        response = model.generate_content(prompt)

    st.subheader("🌿 Crop Recommendations:")
    st.markdown(response.text)

st.markdown("---")
st.caption("Powered by Google Gemini 🌱 | Built with Streamlit")