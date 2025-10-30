# app/routes/route_forecast.py
from fastapi import APIRouter, HTTPException, Query
from app.services import google_maps

router = APIRouter(prefix="/route", tags=["Route"])

@router.get("/extract")
def extract_route(url: str = Query(..., description="Google Maps route URL")):
    """
    Extracts start and end coordinates from a Google Maps URL.
    """
    try:
        coords = google_maps.get_route_coordinates(url)
        return {
            "success": True,
            "start": coords["start"],
            "end": coords["end"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
