import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance (in km) between two points on Earth.
    """
    R = 6371.0  # Radius of Earth (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def interpolate_points(start, end, num_points):
    """
    Linearly interpolate coordinates between start and end.
    Returns a list of evenly spaced coordinates.
    """
    lat1, lon1 = start["lat"], start["lon"]
    lat2, lon2 = end["lat"], end["lon"]

    lat_step = (lat2 - lat1) / (num_points + 1)
    lon_step = (lon2 - lon1) / (num_points + 1)

    points = []
    for i in range(1, num_points + 1):
        points.append({
            "lat": lat1 + lat_step * i,
            "lon": lon1 + lon_step * i
        })
    return points
