from app.services.routing.api_client import get_route_from_google
from app.services.routing.sampler import sample_hourly_points
from app.services.weather_service import get_weather_forecast_for_route
from app.services.reverse_geocode import get_place_name  # Now uses OSM (Nominatim)
from app.services.weather_summary import summarize_weather_point


def get_weather_along_route(start, end, profile="driving", interval_hours=1):
    """
    Get enriched weather forecast along a realistic route between start and end points.
    Adds:
      - Place names via reverse geocoding (OpenStreetMap)
      - Human-readable weather summaries using Gemini
    """
    # Step 1: Get route data from Google Directions API
    route_data = get_route_from_google(start["lat"], start["lon"], end["lat"], end["lon"], profile)
    if not route_data or "coordinates" not in route_data:
        raise ValueError("Failed to retrieve valid route data from Google Directions API")

    # Step 2: Sample waypoints roughly 1 hour apart (customizable)
    sampled_points = sample_hourly_points(route_data, interval_hours)
    if not sampled_points:
        raise ValueError("No route points could be sampled")

    # Step 3: Prepare (lat, lon, time_offset_hr) list for weather forecast
    waypoints = [(p["lat"], p["lon"], p["time_offset_hr"]) for p in sampled_points]

    # Step 4: Fetch time-aligned forecasts for each sampled waypoint
    weather_results = get_weather_forecast_for_route(waypoints)

    # Step 5: Enrich with place names and GenAI weather summaries
    weather_along_route = []
    for point, weather in zip(sampled_points, weather_results):
        lat, lon = point["lat"], point["lon"]

        # ✅ Reverse geocoding (OpenStreetMap Nominatim)
        place_name = get_place_name(lat, lon)

        # ✅ AI-based natural-language weather summary
        summary = summarize_weather_point(
            temp=weather.get("temperature"),
            windspeed=weather.get("wind_speed"),
            precipitation=weather.get("precipitation"),
        )

        # ✅ Combine all info into one record
        weather_along_route.append({
            "place": place_name,
            "time_offset_hr": point["time_offset_hr"],
            "coordinates": {"lat": lat, "lon": lon},
            "forecast_time": weather.get("forecast_time"),
            "temperature": weather.get("temperature"),
            "precipitation": weather.get("precipitation"),
            "wind_speed": weather.get("wind_speed"),
            "weathercode": weather.get("weathercode"),
            "summary": summary,
            "error": weather.get("error") if "error" in weather else None
        })

    # Step 6: Return structured, enriched output
    return {
        "start": start,
        "end": end,
        "profile": profile,
        "interval_hours": interval_hours,
        "total_points": len(weather_along_route),
        "weather_along_route": weather_along_route
    }
