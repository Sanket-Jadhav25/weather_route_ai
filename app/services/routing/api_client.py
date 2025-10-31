import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_route_from_google(start_lat, start_lon, end_lat, end_lon, profile="driving"):
    """
    Fetch route from Google Directions API and return coordinates in normalized format.
    """
    api_key = GOOGLE_MAPS_API_KEY
    if not api_key:
        raise ValueError("Google Maps API key not found in environment variables")

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{start_lat},{start_lon}",
        "destination": f"{end_lat},{end_lon}",
        "mode": profile,
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("🔗 Request URL:", response.url)
    print("📡 API Status:", data.get("status"))
    print("⚠️ Error message:", data.get("error_message"))

    if data.get("status") != "OK":
        raise ValueError(f"Google Directions API error: {data.get('status')} - {data.get('error_message')}")

    if not data["routes"]:
        raise ValueError("No routes found in Google Directions API response")

    overview_polyline = data["routes"][0]["overview_polyline"]["points"]
    coordinates = decode_polyline(overview_polyline)

    return {"coordinates": coordinates, "total_points": len(coordinates)}


def decode_polyline(polyline_str):
    """
    Decode a Google Maps encoded polyline string into a list of {lat, lon} dictionaries.
    """
    index, lat, lon = 0, 0, 0
    coordinates = []

    while index < len(polyline_str):
        for coord in [lat, lon]:
            shift, result = 0, 0
            while True:
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            d = ~(result >> 1) if (result & 1) else (result >> 1)
            if coord is lat:
                lat += d
            else:
                lon += d
        coordinates.append({"lat": lat / 1e5, "lon": lon / 1e5})

    return coordinates
