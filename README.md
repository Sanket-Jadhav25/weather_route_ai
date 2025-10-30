# weather_route_ai
An AI-powered weather route assistant that predicts rain, wind, and temperature along your travel path using Google Maps routes and Open-Meteo forecasts. Built with FastAPI, Streamlit, and SQLite for scalable, real-time trip planning.

## High-level Architecture

## **🚀 Weather Route Risk Forecasting System — Full Architecture**

Here’s the **complete architecture**, including all layers, data flow, and agentic AI integration 👇

---

### **🧱 1\. System Overview Diagram**

graph TD  
    A\[User \- Streamlit UI\] \--\>|Enter Route Link / Source & Destination| B\[FastAPI Backend\]  
    B \--\>|API Call| C\[RouteAgent \- Google Directions API\]  
    C \--\>|Waypoints \+ ETA| D\[WeatherAgent \- Open Meteo API\]  
    D \--\>|Forecast Data| E\[SimulationAgent \- Travel Forecast Timeline\]  
    E \--\>|Structured Route Weather Data| F\[InsightAgent \- Gemini 2.5 Flash\]  
    F \--\>|Natural Language Summary \+ Recommendations| A  
    B \--\>|Store data| G\[(SQLite Database)\]  
    B \--\>|Retrieve history| G  
    A \--\>|Display Route, Charts, Risks| A

---

## **⚙️ 2\. Layer-by-Layer Architecture**

---

### **🖥️ Frontend Layer – Streamlit**

**Purpose:** User interaction and visualization.  
 **Responsibilities:**

* Take **route input** (start, end, date/time, or pasted Google Maps link)

* Call the FastAPI backend for processing

* Display:

  * Map visualization with weather overlay

  * Hour-by-hour forecast timeline

  * LLM-generated recommendation summary

**Core features:**

* `st.map()` or `folium` for route display

* `st.line_chart()` for weather timeline (rain, wind, temperature)

* “Download Report” button for summary

---

### **⚡ Backend Layer – FastAPI**

**Purpose:** Orchestration \+ API endpoint layer.  
 **Responsibilities:**

* Expose REST endpoints:

  * `/analyze_route` → main processing route

  * `/get_history` → past forecasts

  * `/healthcheck`

* Handle async calls to:

  * Google Maps API

  * Open-Meteo API

  * Gemini LLM API

* Manage caching \+ DB transactions

**Endpoints Example:**

@app.post("/analyze\_route")  
async def analyze\_route(start: str, end: str, date: str, time: str):  
    \# Orchestrate agents and return analysis  
    ...

---

### **🧩 Agentic Layer – Core Intelligence**

Each agent is modular, isolated, and testable.

#### **🗺️ 1\. RouteAgent**

* Input: start, end (from user or link)

* Output: coordinates for waypoints (lat/lon)

* API: Google Directions

* Responsibilities:

  * Decode the route polyline

  * Generate “hourly stops” based on ETA per segment

#### **🌦️ 2\. WeatherAgent**

* Input: list of coordinates \+ timestamps

* Output: hourly forecast for each waypoint

* API: Open-Meteo

* Responsibilities:

  * Fetch weather data per location

  * Extract temperature, rain, wind, soil, etc.

#### **⏱️ 3\. SimulationAgent**

* Input: ETA \+ forecast data

* Output: aligned timeline with route

* Responsibilities:

  * Match each waypoint’s ETA with forecast hours

  * Compute risk levels per segment (rain \> 10mm \= high risk)

  * Summarize total journey risk

#### **🧠 4\. InsightAgent (GenAI Layer)**

* Input: structured JSON (route \+ weather \+ risks)

* Output: Natural language explanation

* Model: Gemini 2.5 Flash (free API)

* Responsibilities:

  * Generate readable summaries:

    * “Light rain expected near Lonavala between 10–11 AM.”

    * “Avoid travel between 9–11 AM due to crosswinds near Pune.”

  * Suggest best travel time/day

#### **🚨 5\. AlertAgent (optional future)**

* Watches historical data

* Sends alerts when route risk \> threshold (SMS/email)

---

### **🧮 Data Layer – SQLite**

**Purpose:** Store and manage user & forecast data.  
 **Schema Example:**

TABLE users (  
    id INTEGER PRIMARY KEY,  
    name TEXT,  
    email TEXT  
);

TABLE routes (  
    id INTEGER PRIMARY KEY,  
    start TEXT,  
    end TEXT,  
    date TEXT,  
    time TEXT,  
    created\_at TIMESTAMP  
);

TABLE forecasts (  
    id INTEGER PRIMARY KEY,  
    route\_id INTEGER,  
    location TEXT,  
    eta TEXT,  
    rain\_mm REAL,  
    wind\_speed REAL,  
    temp REAL,  
    risk\_level TEXT,  
    FOREIGN KEY(route\_id) REFERENCES routes(id)  
);

**Optional add-ons:**

* Cache Open-Meteo results to reduce API calls

* Store user travel history

* Save LLM recommendations

---

### **🧠 LLM Integration – Gemini 2.5 Flash**

**Purpose:** Transform structured weather data into intelligent advice  
 **Endpoints:**

* `/v1beta/models/gemini-2.5-flash:generateContent`

**Prompt Template Example:**

prompt \= f"""  
Analyze the following route weather data and write travel advice.

Route: {start} → {end}  
Forecast:  
{json.dumps(forecast\_data, indent=2)}

Explain risks and suggest the best time to travel.  
"""

---

### **🧰 Support Systems**

| Feature | Tool | Purpose |
| ----- | ----- | ----- |
| **Logging** | Python `logging` | Debug \+ error trace |
| **Task Queue** | `FastAPI BackgroundTasks` | Long route async processing |
| **Env Management** | `.env + python-dotenv` | Secure API keys |
| **Testing** | `pytest` | Unit tests for each agent |
| **Version Control** | `Git + GitHub` | Full commit history |
| **Deployment** | Docker \+ Compose | Run Streamlit \+ FastAPI \+ SQLite stack |

---

## **🧭 3\. Data Flow Example (Mumbai → Kolhapur)**

1️⃣ User enters route in Streamlit  
     ↓  
2️⃣ FastAPI receives input → calls RouteAgent  
     ↓  
3️⃣ RouteAgent fetches waypoints & ETA  
     ↓  
4️⃣ WeatherAgent fetches hourly forecasts per waypoint  
     ↓  
5️⃣ SimulationAgent aligns ETA \+ weather to create risk profile  
     ↓  
6️⃣ InsightAgent (Gemini) converts risk data into human summary  
     ↓  
7️⃣ Streamlit displays charts, map, and AI summary  
     ↓  
8️⃣ SQLite logs this query for historical lookup

---

## **📦 4\. Folder Structure**

weather\_route\_forecast/  
│  
├── app/  
│   ├── main.py                  \# Entry point for FastAPI  
│   ├── api/  
│   │   ├── routes.py            \# All API routes  
│   │   ├── schemas.py           \# Pydantic models  
│   │   ├── services.py          \# Business logic (e.g., route parsing, weather fetching)  
│   │   ├── genai\_assistant.py   \# LLM reasoning (future integration)  
│   │   └── \_\_init\_\_.py  
│   │  
│   ├── core/  
│   │   ├── config.py            \# Environment variables, constants  
│   │   ├── utils.py             \# Helper utilities  
│   │   └── \_\_init\_\_.py  
│   │  
│   ├── db/  
│   │   ├── database.py          \# SQLite connection setup  
│   │   ├── models.py            \# SQLAlchemy ORM models  
│   │   └── crud.py              \# Database operations  
│   │  
│   └── \_\_init\_\_.py  
│  
├── streamlit\_app/  
│   ├── ui.py                    \# Streamlit frontend (interacts with FastAPI)  
│   └── \_\_init\_\_.py  
│  
├── tests/  
│   ├── test\_api.py  
│   ├── test\_ui.py  
│   └── \_\_init\_\_.py  
│  
├── .env                         \# API keys, DB URL, etc.  
├── requirements.txt  
├── Dockerfile  
├── docker-compose.yml  
└── README.md  
