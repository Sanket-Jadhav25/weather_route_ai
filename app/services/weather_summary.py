import google.generativeai as genai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"  # or gemini-2.0-flash if available


def summarize_weather_point(temp, windspeed, precipitation):
    """
    Generate a natural-language summary of weather at a location.
    Example: 'Light rain expected with moderate winds.'
    """
    try:
        prompt = (
            f"The temperature is {temp}°C, wind speed is {windspeed} km/h, "
            f"and precipitation is {precipitation} mm. "
            "Describe this weather in 1 short sentence (e.g. 'Light rain expected')."
        )

        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        # ✅ Defensive check
        if not response or not hasattr(response, "text"):
            logger.error(f"Gemini response missing text: {response}")
            return "Weather summary unavailable"

        return response.text.strip()

    except Exception as e:
        logger.exception(f"Gemini API error: {e}")
        return "Weather summary unavailable"
