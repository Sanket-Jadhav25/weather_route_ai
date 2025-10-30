import requests

def get_weather_forecast(start_lat: float, start_lon: float, end_lat: float, end_lon: float, hours: int = 24):
    """
    Fetches hourly weather forecast for both the start and end locations using Open-Meteo API.
    
    Args:
        start_lat (float): Latitude of the starting point
        start_lon (float): Longitude of the starting point
        end_lat (float): Latitude of the destination
        end_lon (float): Longitude of the destination
        hours (int): Number of hours of forecast to fetch (default 24)
    
    Returns:
        dict: Hourly forecast data for start and end points or an error message.
    """

    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "hourly": "temperature_2m,precipitation,weathercode,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        # Start point forecast
        params["latitude"], params["longitude"] = start_lat, start_lon
        response_start = requests.get(base_url, params=params)
        response_start.raise_for_status()
        start_data = response_start.json()

        # End point forecast
        params["latitude"], params["longitude"] = end_lat, end_lon
        response_end = requests.get(base_url, params=params)
        response_end.raise_for_status()
        end_data = response_end.json()

        # Parse limited number of hours (for example, first 24 hours)
        def extract_hourly_subset(data):
            hourly = data.get("hourly", {})
            subset = []
            for i in range(min(hours, len(hourly.get("time", [])))):
                subset.append({
                    "time": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "precipitation": hourly["precipitation"][i],
                    "wind_speed": hourly["wind_speed_10m"][i],
                    "weathercode": hourly["weathercode"][i]
                })
            return subset

        return {
            "start_point_forecast": extract_hourly_subset(start_data),
            "end_point_forecast": extract_hourly_subset(end_data)
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error while fetching data: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
