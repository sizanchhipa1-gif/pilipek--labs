import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# API Key Streamlit ki settings se aayegi (Safe tareeka)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Aapki company ka naam 
st.title("📦 Pilipek Labs: Order Parser")
st.write("WhatsApp ya Instagram ki chat niche wale dabbe mein paste karein!")

chat_input = st.text_area("Customer Chat:", height=150)

if st.button("Parse Order"):
    if chat_input:
        with st.spinner("Pilipek Labs AI data nikal raha hai..."):
            prompt = f"""
            Extract the following info from the chat text: Customer Name, Phone Number, Full Delivery Address, Product Details, and Size.
            Return STRICTLY as a JSON object with keys: Name, Phone, Address, Product, Size.
            Chat Text: {chat_input}
            """
            try:
                response = model.generate_content(prompt)
                result = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(result)
                st.success("Order Parsed Successfully!")
                df = pd.DataFrame([data])
                st.table(df)
            except Exception as e:
                st.error("Text samajh nahi aaya. Please clear chat paste karein.")
    else:
        st.warning("Pehle khali dabbe mein chat paste karein!")
