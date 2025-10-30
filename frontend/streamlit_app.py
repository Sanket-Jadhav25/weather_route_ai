import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Weather Route AI", page_icon="🌦️")

st.title("🌦️ Weather Route AI Assistant")

route_url = st.text_input("Enter your Google Maps route URL")

if st.button("Analyze Route"):
    if route_url:
        with st.spinner("Analyzing route and fetching weather..."):
            try:
                # Send the route URL to the forecast API
                res = requests.get("http://127.0.0.1:8000/forecast/", params={"url": route_url})
                
                if res.status_code == 200:
                    data = res.json()

                    # Show route info
                    st.subheader("🗺️ Route Information")
                    start = data["route"]["start"]
                    end = data["route"]["end"]
                    st.write(f"**Start:** {start}")
                    st.write(f"**End:** {end}")

                    # Display weather data for start and end
                    st.subheader("🌦️ Weather Forecast (Next 24 Hours)")

                    start_df = pd.DataFrame(data["forecast"]["start_point_forecast"])
                    end_df = pd.DataFrame(data["forecast"]["end_point_forecast"])

                    st.write("**Start Location Forecast:**")
                    st.dataframe(start_df)

                    st.write("**End Location Forecast:**")
                    st.dataframe(end_df)

                else:
                    st.error(f"Error: {res.text}")

            except Exception as e:
                st.error(f"Failed to connect: {e}")
    else:
        st.warning("Please enter a valid Google Maps URL.")
