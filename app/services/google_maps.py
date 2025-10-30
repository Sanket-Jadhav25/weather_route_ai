import re
import requests

def parse_google_maps_url(url: str):
    """
    Extracts start and end place names from a Google Maps URL.
    Example: https://www.google.com/maps/dir/Mumbai/Kolhapur
    """
    # Use regex that also supports encoded characters and query params
    match = re.search(r"/maps/dir/([^/]+)/([^/?#]+)", url)
    if not match:
        raise ValueError("Invalid Google Maps URL format. Expected format: https://www.google.com/maps/dir/City1/City2")

    # Decode URL parts and replace '+' with spaces
    start = match.group(1).replace("+", " ").replace("%20", " ")
    end = match.group(2).replace("+", " ").replace("%20", " ")
    return {"start": start.strip(), "end": end.strip()}


def geocode_location(location: str):
    """
    Converts a location name to latitude and longitude using Open-Meteo Geocoding API.
    If the API fails to find it, retries with simplified name (first word).
    """
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def request_location(query):
        params = {"name": query, "count": 1, "language": "en", "format": "json"}
        try:
            response = requests.get(geo_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                top_result = data["results"][0]
                return {"lat": top_result["latitude"], "lon": top_result["longitude"]}
        except requests.RequestException:
            pass
        return None

    # Try full name
    result = request_location(location)
    if result:
        return result

    # Retry with simplified version
    simplified = location.split(",")[0].strip()
    result = request_location(simplified)
    if result:
        return result

    raise ValueError(f"Could not geocode location: {location}")


def get_route_coordinates(url: str):
    """
    Parses the Google Maps URL, geocodes both start and end locations,
    and returns coordinates for both.
    """
    locations = parse_google_maps_url(url)
    start_coords = geocode_location(locations["start"])
    end_coords = geocode_location(locations["end"])
    return {"start": start_coords, "end": end_coords}
