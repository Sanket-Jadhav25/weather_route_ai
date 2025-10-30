# app/routes/forecast.py
from fastapi import APIRouter, Query, HTTPException
from app.services.weather_service import get_weather_forecast
from app.services.google_maps import get_route_coordinates

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/")
def get_forecast(
    url: str = Query(None, description="Google Maps direction URL (optional)"),
    start_lat: float = Query(None, description="Latitude of start point"),
    start_lon: float = Query(None, description="Longitude of start point"),
    end_lat: float = Query(None, description="Latitude of end point"),
    end_lon: float = Query(None, description="Longitude of end point"),
):
    """
    Fetch hourly weather data for a given route.
    Accepts either:
      - Google Maps direction URL, OR
      - Direct coordinates for start and end points
    """
    try:
        # Case 1: Google Maps URL provided
        if url:
            route_coords = get_route_coordinates(url)
            start = route_coords["start"]
            end = route_coords["end"]

            forecast_data = get_weather_forecast(
                start["lat"], start["lon"],
                end["lat"], end["lon"]
            )

            return {
                "success": True,
                "route": route_coords,
                "forecast": forecast_data
            }

        # Case 2: Coordinates provided directly
        elif None not in (start_lat, start_lon, end_lat, end_lon):
            forecast_data = get_weather_forecast(start_lat, start_lon, end_lat, end_lon)
            return {"success": True, "forecast": forecast_data}

        else:
            raise HTTPException(
                status_code=400,
                detail="Please provide either a Google Maps URL or start/end coordinates."
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
