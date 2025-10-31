import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium

# --- Helper functions ---

def plot_route_map(data):
    """Creates a folium map with route points and start/end markers"""
    m = folium.Map(location=[data["data"]["start"]["lat"], data["data"]["start"]["lon"]], zoom_start=6)

    # Plot route markers
    for wp in data["data"]["weather_along_route"]:
        lat = wp["coordinates"]["lat"]
        lon = wp["coordinates"]["lon"]
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue"
        ).add_to(m)

    # Add start and end markers
    folium.Marker(
        [data["data"]["start"]["lat"], data["data"]["start"]["lon"]],
        popup="Start",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        [data["data"]["end"]["lat"], data["data"]["end"]["lon"]],
        popup="End",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)

    return m


def load_weather_data(data):
    """Returns only the next-hour weather forecast for each route point."""
    all_rows = []
    for wp in data["data"]["weather_along_route"]:
        lat = wp["coordinates"]["lat"]
        lon = wp["coordinates"]["lon"]
        offset = wp["time_offset_hr"]

        # Just get the next-hour forecast (first record)
        if wp["weather"]["start_point_forecast"]:
            record = wp["weather"]["start_point_forecast"][0]
            all_rows.append({
                "Hour Offset": offset,
                "Latitude": lat,
                "Longitude": lon,
                "Time": record["time"],
                "Temperature (°C)": record["temperature"],
                "Precipitation (mm)": record["precipitation"],
                "Wind Speed (m/s)": record["wind_speed"],
                "Weather Code": record["weathercode"]
            })
    return pd.DataFrame(all_rows)



# --- Streamlit UI ---

st.set_page_config(page_title="Weather Route AI", page_icon="🌦️")
st.title("🌦️ Weather Route AI Assistant")

route_url = st.text_input("Enter your Google Maps route URL")

# Maintain state across reruns
if "data" not in st.session_state:
    st.session_state["data"] = None

if st.button("Analyze Route"):
    if not route_url:
        st.warning("⚠️ Please enter a valid Google Maps URL.")
    else:
        with st.spinner("Analyzing route and fetching weather..."):
            try:
                res = requests.get("http://127.0.0.1:8000/forecast/", params={"url": route_url})
                if res.status_code != 200:
                    st.error(f"❌ API Error: {res.text}")
                else:
                    data = res.json()
                    if data.get("success"):
                        st.session_state["data"] = data
                    else:
                        st.error("❌ API did not return success.")
            except Exception as e:
                st.error(f"🚨 Failed to connect: {e}")

# --- Display stored data ---
if st.session_state["data"]:
    data = st.session_state["data"]

    st.subheader("🗺️ Route Information")
    st.write(f"**Start:** {data['data']['start']}")
    st.write(f"**End:** {data['data']['end']}")
    st.write(f"**Profile:** {data['data']['profile']}")
    st.write(f"**Interval (hours):** {data['data']['interval_hours']}")
    st.write(f"**Sampled Points:** {data['data']['total_points']}")

    st.subheader("📍 Route Map")
    route_map = plot_route_map(data)
    st_folium(route_map, width=800, height=500)

    st.subheader("🌦️ Weather Along the Route")
    weather_df = load_weather_data(data)
    st.dataframe(weather_df)

    st.subheader("📊 Weather Summary")
    stats = {
        "Min Temp (°C)": weather_df["Temperature (°C)"].min(),
        "Max Temp (°C)": weather_df["Temperature (°C)"].max(),
        "Avg Wind Speed (m/s)": weather_df["Wind Speed (m/s)"].mean(),
        "Total Precipitation (mm)": weather_df["Precipitation (mm)"].sum()
    }
    st.table(pd.DataFrame([stats]))
