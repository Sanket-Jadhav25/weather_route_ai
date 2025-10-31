# app/routes/forecast.py
from fastapi import APIRouter, Query, HTTPException
from app.services.google_maps import get_route_coordinates  # keep your existing google_maps.py
from app.services.routing_service import get_weather_along_route
import logging
import traceback

# Initialize logger
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/")
def get_forecast(
    url: str = Query(None, description="Google Maps direction URL (optional)"),
    start_lat: float = Query(None, description="Latitude of start point"),
    start_lon: float = Query(None, description="Longitude of start point"),
    end_lat: float = Query(None, description="Latitude of end point"),
    end_lon: float = Query(None, description="Longitude of end point"),
    profile: str = Query("driving", description="Routing mode: driving, walking, bicycling, or transit"),
    interval_hours: int = Query(1, description="Time interval (in hours) between forecast points")
):
    """
    Fetch hourly weather data along the actual route.
    Accepts either:
      - A Google Maps direction URL, OR
      - Direct coordinates for start and end points
    """
    try:
        # 1️⃣ Case: URL is provided
        if url:
            waypoints = get_route_coordinates(url)
            if not waypoints:
                raise ValueError("No route waypoints found")

            # Handle coordinate extraction (now list of dicts)
            if isinstance(waypoints, dict) and "coordinates" in waypoints:
                coords = waypoints["coordinates"]
            else:
                coords = waypoints

            print("DEBUG: waypoints =", waypoints)
            print("DEBUG: coords =", coords)

            # ✅ Fix: access dict keys instead of tuple indices
            start = {"lat": coords[0]["lat"], "lon": coords[0]["lon"]}
            end = {"lat": coords[-1]["lat"], "lon": coords[-1]["lon"]}

            weather_data = get_weather_along_route(start, end, profile=profile, interval_hours=interval_hours)
            return {
                "success": True,
                "route_source": "Google Maps URL",
                "route": {"start": start, "end": end},
                "data": weather_data
            }

        # 2️⃣ Case: Direct coordinates provided
        elif None not in (start_lat, start_lon, end_lat, end_lon):
            start = {"lat": start_lat, "lon": start_lon}
            end = {"lat": end_lat, "lon": end_lon}

            weather_data = get_weather_along_route(start, end, profile=profile, interval_hours=interval_hours)
            return {
                "success": True,
                "route_source": "manual coordinates",
                "route": {"start": start, "end": end},
                "data": weather_data
            }

        # 3️⃣ No valid input
        else:
            raise HTTPException(status_code=400, detail="Please provide either a Google Maps URL or start/end coordinates.")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("🔥 Unexpected error in /forecast route:")
        traceback.print_exc()   # shows full error stack trace in terminal
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
