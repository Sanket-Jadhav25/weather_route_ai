import requests
from datetime import datetime, timedelta

def get_weather_forecast_for_route(waypoints, hours_limit: int = 24):
    """
    Fetches time-aligned weather forecasts for each waypoint along the route
    using the Open-Meteo API.

    Args:
        waypoints (list of tuples): [(lat, lon, hours_from_start), ...]
        hours_limit (int): Maximum forecast horizon in hours (default 24)

    Returns:
        list of dict: Each dict contains location, ETA hours, and weather forecast
    """

    base_url = "https://api.open-meteo.com/v1/forecast"
    results = []

    for lat, lon, hours_from_start in waypoints:
        # Skip waypoints too far in the future
        if hours_from_start > hours_limit:
            results.append({
                "latitude": lat,
                "longitude": lon,
                "hours_from_start": hours_from_start,
                "error": f"Forecast beyond {hours_limit}h not available"
            })
            continue

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,precipitation,weathercode,wind_speed_10m",
            "timezone": "auto"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            hourly = data.get("hourly", {})

            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            precips = hourly.get("precipitation", [])
            winds = hourly.get("wind_speed_10m", [])
            codes = hourly.get("weathercode", [])

            # Find forecast closest to ETA (current_time + hours_from_start)
            current_time = datetime.utcnow()
            target_time = current_time + timedelta(hours=hours_from_start)

            # Convert all forecast times to datetime for comparison
            time_objs = [datetime.fromisoformat(t) for t in times]
            closest_idx = min(
                range(len(time_objs)),
                key=lambda i: abs(time_objs[i] - target_time)
            )

            results.append({
                "latitude": lat,
                "longitude": lon,
                "hours_from_start": hours_from_start,
                "forecast_time": times[closest_idx],
                "temperature": temps[closest_idx],
                "precipitation": precips[closest_idx],
                "wind_speed": winds[closest_idx],
                "weathercode": codes[closest_idx],
            })

        except requests.exceptions.RequestException as e:
            results.append({
                "latitude": lat,
                "longitude": lon,
                "hours_from_start": hours_from_start,
                "error": f"Network error while fetching data: {e}"
            })
        except Exception as e:
            results.append({
                "latitude": lat,
                "longitude": lon,
                "hours_from_start": hours_from_start,
                "error": f"Unexpected error: {e}"
            })

    return results
