from app.services.routing.geometry_utils import haversine_distance

def sample_hourly_points(route_data, interval_hours=1, avg_speed_kmh=60):
    """
    Sample coordinates along the route based on travel time intervals.

    Args:
        route_data (dict): Contains list of route coordinates.
        interval_hours (float): Sampling interval (in hours).
        avg_speed_kmh (float): Assumed average travel speed in km/h.

    Returns:
        list: Sampled points with 'lat', 'lon', and 'time_offset_hr'.
    """
    coordinates = route_data.get("coordinates", [])
    if len(coordinates) < 2:
        return []

    sampled_points = [{"lat": coordinates[0]["lat"], "lon": coordinates[0]["lon"], "time_offset_hr": 0}]
    total_distance = 0.0
    time_accumulated = 0.0
    total_time_hr = 0.0

    for i in range(1, len(coordinates)):
        prev, curr = coordinates[i - 1], coordinates[i]
        segment_km = haversine_distance(prev["lat"], prev["lon"], curr["lat"], curr["lon"])
        total_distance += segment_km
        time_accumulated += segment_km / avg_speed_kmh
        total_time_hr += segment_km / avg_speed_kmh

        # Add a sampled point every interval_hours of travel time
        if time_accumulated >= interval_hours:
            sampled_points.append({
                "lat": curr["lat"],
                "lon": curr["lon"],
                "time_offset_hr": round(total_time_hr, 2)
            })
            time_accumulated = 0.0

    # ✅ Ensure the destination point is always included
    last_point = coordinates[-1]
    if sampled_points[-1]["lat"] != last_point["lat"] or sampled_points[-1]["lon"] != last_point["lon"]:
        sampled_points.append({
            "lat": last_point["lat"],
            "lon": last_point["lon"],
            "time_offset_hr": round(total_time_hr, 2)
        })

    return sampled_points
