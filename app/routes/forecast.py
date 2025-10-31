# app/routes/forecast.py
from fastapi import APIRouter, Query, HTTPException
from app.services.google_maps import get_route_coordinates
from app.services.routing_service import get_weather_along_route

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/")
def get_forecast(
    url: str = Query(None, description="Google Maps direction URL (optional)"),
    start_lat: float = Query(None, description="Latitude of start point"),
    start_lon: float = Query(None, description="Longitude of start point"),
    end_lat: float = Query(None, description="Latitude of end point"),
    end_lon: float = Query(None, description="Longitude of end point"),
    profile: str = Query("driving-car", description="Routing mode: driving-car, cycling-regular, foot-walking"),
    interval_hours: int = Query(1, description="Time interval (in hours) between forecast points")
):
    """
    Fetch hourly weather data along the actual route.
    Accepts either:
      - A Google Maps direction URL, OR
      - Direct coordinates for start and end points
    """
    try:
        #  1 - Google Maps URL provided
        if url:
            route_coords = get_route_coordinates(url)
            start = route_coords["start"]
            end = route_coords["end"]

            weather_data = get_weather_along_route(start, end, profile=profile, interval_hours=interval_hours)
            return {"success": True, "route": route_coords, "data": weather_data}

        #  2 - Direct lat/lon coordinates provided
        elif None not in (start_lat, start_lon, end_lat, end_lon):
            start = {"lat": start_lat, "lon": start_lon}
            end = {"lat": end_lat, "lon": end_lon}

            weather_data = get_weather_along_route(start, end, profile=profile, interval_hours=interval_hours)
            return {"success": True, "route": {"start": start, "end": end}, "data": weather_data}

        # When No valid input provided
        else:
            raise HTTPException(
                status_code=400,
                detail="Please provide either a Google Maps URL or start/end coordinates."
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
