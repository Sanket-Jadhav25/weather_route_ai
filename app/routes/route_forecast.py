# app/routes/route_forecast.py
from fastapi import APIRouter, HTTPException, Query
from app.services.google_maps import get_route_coordinates  # ✅ import the correct function

router = APIRouter(prefix="/route", tags=["Route"])

@router.get("/extract")
def extract_route(url: str = Query(..., description="Google Maps route URL")):
    """
    Extracts start and end coordinates from a Google Maps URL.
    """
    try:
        coords = get_route_coordinates(url)  # ✅ call the function directly
        return {
            "success": True,
            "start": coords["start"],
            "end": coords["end"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
