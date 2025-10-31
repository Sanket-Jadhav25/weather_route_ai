# app/main.py
from fastapi import FastAPI
from app.routes import forecast, route_forecast
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Weather Route AI")

@app.get("/")
def read_root():
    return {"message": "Weather Route AI backend is running 🚀"}

# Include routes
app.include_router(route_forecast.router)
app.include_router(forecast.router)
