import requests

def get_place_name(lat, lon):
    """
    Return a human-readable place name for given coordinates using OpenStreetMap (Nominatim).
    This avoids Google API costs and works globally.
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "zoom": 10,  # 10 = city/town level; 18 = street level
            "addressdetails": 1
        }
        headers = {"User-Agent": "weather-route-ai/1.0 (contact@example.com)"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "display_name" in data:
            return data["display_name"]
        else:
            return f"({lat:.2f}, {lon:.2f})"

    except Exception as e:
        print(f"Reverse geocode error for ({lat},{lon}): {e}")
        return f"({lat:.2f}, {lon:.2f})"
