from app.services.routing.api_client import get_route_from_google
from app.services.routing.sampler import sample_hourly_points
from app.services.weather_service import get_weather_forecast


def get_weather_along_route(start, end, profile="driving", interval_hours=1):
    """
    Get weather forecast along a realistic route between start and end points.
    Uses Google Directions API for routing and Open-Meteo for weather.
    """
    route_data = get_route_from_google(start["lat"], start["lon"], end["lat"], end["lon"], profile)

    if not route_data or "coordinates" not in route_data:
        raise ValueError("Failed to retrieve valid route data from Google Directions API")

    sampled_points = sample_hourly_points(route_data, interval_hours)
    if not sampled_points:
        raise ValueError("No route points could be sampled")

    weather_along_route = []
    for point in sampled_points:
        lat, lon = point["lat"], point["lon"]
        weather = get_weather_forecast(lat, lon, lat, lon)
        weather_along_route.append({
            "time_offset_hr": point["time_offset_hr"],
            "coordinates": {"lat": lat, "lon": lon},
            "weather": weather
        })

    return {
        "start": start,
        "end": end,
        "profile": profile,
        "interval_hours": interval_hours,
        "total_points": len(weather_along_route),
        "weather_along_route": weather_along_route
    }
