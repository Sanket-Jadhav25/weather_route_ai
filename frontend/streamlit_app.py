import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium

# --- Helper functions ---

def plot_route_map(data):
    route_points = data["data"]["weather_along_route"]

    # Start point
    start_lat = route_points[0]["coordinates"]["lat"]
    start_lon = route_points[0]["coordinates"]["lon"]

    m = folium.Map(location=[start_lat, start_lon], zoom_start=8)

    # Add route markers
    for wp in route_points:
        coords = wp["coordinates"]
        lat, lon = coords["lat"], coords["lon"]
        place_name = wp.get("place", "Unknown Location")
        summary = wp.get("summary", "")

        popup_text = (
            f"<b>{place_name}</b><br>"
            f"Time Offset: {wp['time_offset_hr']}h<br>"
            f"Temp: {wp['temperature']}°C<br>"
            f"Precipitation: {wp['precipitation']} mm<br>"
            f"Wind: {wp['wind_speed']} km/h<br>"
            f"<i>{summary}</i>"
        )

        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    # Draw polyline along route
    folium.PolyLine(
        [[wp["coordinates"]["lat"], wp["coordinates"]["lon"]] for wp in route_points],
        color="blue",
        weight=3,
        opacity=0.8
    ).add_to(m)

    return m


def load_weather_data(data):
    """Returns weather forecast summary for each sampled route point."""
    all_rows = []
    for wp in data["data"]["weather_along_route"]:
        all_rows.append({
            "Place": wp.get("place", "Unknown"),
            "Hour Offset": wp["time_offset_hr"],
            "Temperature (°C)": wp.get("temperature"),
            "Precipitation (mm)": wp.get("precipitation"),
            "Wind Speed (km/h)": wp.get("wind_speed"),
            "Summary": wp.get("summary", "N/A"),
        })
    return pd.DataFrame(all_rows)


# --- Streamlit UI ---

st.set_page_config(page_title="Weather Route AI", page_icon="🌦️")
st.title("🌦️ Weather Route AI Assistant")

route_url = st.text_input("Enter your Google Maps route URL")

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
    start = data['route']['start']
    end = data['route']['end']
    st.write(f"**Start:** ({start['lat']}, {start['lon']})")
    st.write(f"**End:** ({end['lat']}, {end['lon']})")
    st.write(f"**Interval (hours):** 1")

    st.subheader("📍 Route Map")
    route_map = plot_route_map(data)
    st_folium(route_map, width=800, height=500)

    st.subheader("🌦️ Weather Along the Route")
    weather_df = load_weather_data(data)
    st.dataframe(weather_df)

    st.subheader("📊 Weather Summary")
    if not weather_df.empty:
        stats = {
            "Min Temp (°C)": weather_df["Temperature (°C)"].min(),
            "Max Temp (°C)": weather_df["Temperature (°C)"].max(),
            "Avg Wind Speed (km/h)": weather_df["Wind Speed (km/h)"].mean(),
            "Total Precipitation (mm)": weather_df["Precipitation (mm)"].sum()
        }
        st.table(pd.DataFrame([stats]))
    else:
        st.info("No weather data available.")
