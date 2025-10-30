import streamlit as st
import requests

st.set_page_config(page_title="Weather Route AI", page_icon="🌦️")

st.title("🌦️ Weather Route AI Assistant")

route_url = st.text_input("Enter your Google Maps route URL")

if st.button("Analyze Route"):
    if route_url:
        try:
            res = requests.get("http://127.0.0.1:8000/route/extract", params={"url": route_url})
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Failed to connect: {e}")
    else:
        st.warning("Please enter a valid Google Maps URL")
