from app.services.routing.geometry_utils import haversine_distance

def sample_hourly_points(route_data, interval_hours=1, avg_speed_kmh=60):
    """
    Sample coordinates along the route based on travel time intervals.
    interval_hours: sampling frequency (in hours)
    avg_speed_kmh: assumed average vehicle speed
    """
    coordinates = route_data.get("coordinates", [])
    if len(coordinates) < 2:
        return []

    sampled_points = [{"lat": coordinates[0]["lat"], "lon": coordinates[0]["lon"], "time_offset_hr": 0}]
    total_distance = 0
    time_accumulated = 0

    for i in range(1, len(coordinates)):
        prev, curr = coordinates[i - 1], coordinates[i]
        segment_distance = haversine_distance(prev["lat"], prev["lon"], curr["lat"], curr["lon"])
        total_distance += segment_distance
        time_accumulated += segment_distance / avg_speed_kmh  # time in hours

        if time_accumulated >= interval_hours:
            sampled_points.append({
                "lat": curr["lat"],
                "lon": curr["lon"],
                "time_offset_hr": round(len(sampled_points) * interval_hours, 2)
            })
            time_accumulated = 0

    return sampled_points
