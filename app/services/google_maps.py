import requests
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_route_coordinates(google_maps_url: str):
    """
    Extracts route information (waypoints, step durations) using Google Maps Directions API.
    Input: A Google Maps route URL
    Output: List of tuples [(latitude, longitude, cumulative_hours_from_start), ...]
    """
    # Example: Extract origin and destination from the shared URL
    # URL format: https://www.google.com/maps/dir/Mumbai/Kolhapur
    try:
        parts = google_maps_url.split("/dir/")[1].split("/")
        origin, destination = parts[0], parts[1]
    except Exception:
        raise ValueError("Invalid Google Maps URL format. Expected format: https://www.google.com/maps/dir/Origin/Destination")

    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"

    response = requests.get(directions_url)
    data = response.json()

    if data["status"] != "OK":
        raise ValueError(f"Google Maps API error: {data['status']}")

    route = data["routes"][0]["legs"][0]

    # --- Capture waypoints along with cumulative time ---
    waypoints = []
    total_time = 0

    for step in route["steps"]:
        lat = step["end_location"]["lat"]
        lng = step["end_location"]["lng"]
        duration_seconds = step["duration"]["value"]
        total_time += duration_seconds
        waypoints.append({
            "lat": lat,
            "lon": lng,
            "time_offset_hr": round(total_time / 3600, 1)
    })
    return waypoints
