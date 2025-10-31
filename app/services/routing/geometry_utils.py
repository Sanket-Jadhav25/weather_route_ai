import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance (in km) between two points on Earth.
    """
    R = 6371.0  # Radius of Earth in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def interpolate_points(start, end, num_points=None, distance_km=None):
    """
    Interpolate coordinates between start and end either by:
    - `num_points`: fixed number of equally spaced points
    - `distance_km`: interval distance (creates points every X km)
    """
    lat1, lon1 = start["lat"], start["lon"]
    lat2, lon2 = end["lat"], end["lon"]

    # Compute number of points if using distance-based sampling
    if distance_km is not None:
        total_distance = haversine_distance(lat1, lon1, lat2, lon2)
        num_points = max(1, int(total_distance // distance_km))

    if not num_points or num_points < 1:
        return []

    lat_step = (lat2 - lat1) / (num_points + 1)
    lon_step = (lon2 - lon1) / (num_points + 1)

    points = [
        {"lat": lat1 + lat_step * i, "lon": lon1 + lon_step * i}
        for i in range(1, num_points + 1)
    ]

    return points
