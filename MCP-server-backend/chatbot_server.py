import os
import httpx
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
NEWSDATA_KEY = os.getenv("NEWSDATA_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# MCP server and FastAPI app
mcp = FastMCP("WeatherNewsMCP")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Store tool functions for manual access
tool_functions = {}

# ======================
# MCP Tools
# ======================

@mcp.tool()
async def getWeather(city: str) -> Dict[str, Any]:
    """Fetch weather for any city worldwide using Open-Meteo API (free, no API key needed)."""
    try:
        # First, get coordinates using OpenStreetMap Nominatim (free geocoding)
        geocode_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": city, "format": "json", "limit": 1}
        
        async with httpx.AsyncClient() as client:
            # Get coordinates
            geo_resp = await client.get(geocode_url, params=params, timeout=10.0)
            geo_data = geo_resp.json()
            
            if not geo_data:
                return {"error": f"City '{city}' not found."}
            
            lat = float(geo_data[0]["lat"])
            lon = float(geo_data[0]["lon"])
            display_name = geo_data[0].get("display_name", city)

            # Get weather data from Open-Meteo (free, global coverage)
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m",
                "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
                "forecast_days": 1,
                "timezone": "auto"
            }
            
            weather_resp = await client.get(weather_url, params=weather_params, timeout=10.0)
            weather_data = weather_resp.json()
            
            if "current" not in weather_data:
                return {"error": "Weather data not available for this location"}
            
            current = weather_data["current"]
            daily = weather_data["daily"]
            
            # Weather code mapping (WMO codes used by Open-Meteo)
            weather_codes = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
                55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
                67: "Heavy freezing rain", 71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
                77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
                82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
                95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }
            
            weather_desc = weather_codes.get(current.get("weather_code", 0), "Unknown")
            
            return {
                "city": city,
                "location": display_name,
                "temperature": round(current.get("temperature_2m", 0), 1),
                "temperatureUnit": "°C",
                "humidity": current.get("relative_humidity_2m", 0),
                "windSpeed": current.get("wind_speed_10m", 0),
                "windDirection": current.get("wind_direction_10m", 0),
                "weather": weather_desc,
                "forecast": {
                    "maxTemp": round(daily["temperature_2m_max"][0], 1) if daily.get("temperature_2m_max") else None,
                    "minTemp": round(daily["temperature_2m_min"][0], 1) if daily.get("temperature_2m_min") else None,
                    "precipitation": daily["precipitation_sum"][0] if daily.get("precipitation_sum") else 0
                },
                "coordinates": {"lat": lat, "lon": lon}
            }
            
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}

# Register tool function manually for access
tool_functions["getWeather"] = getWeather

@mcp.tool()
async def getNews(topic: str) -> Dict[str, Any]:
    """Fetch news from NewsData.io free API."""
    try:
        url = "https://newsdata.io/api/1/news"
        params = {"apikey": NEWSDATA_KEY, "q": topic, "language": "en", "country": "us", "page": 0}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10.0)
            data = resp.json()
        
        articles = data.get("results", [])[:3]
        return {
            "topic": topic, 
            "headlines": [
                {"title": a.get("title"), "link": a.get("link")} 
                for a in articles if a.get("title")
            ]
        }
    except Exception as e:
        return {"error": f"Failed to fetch news: {str(e)}"}

# Register tool function manually for access
tool_functions["getNews"] = getNews

# ======================
# Chatbot Endpoint
# ======================

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    """Chat endpoint: user sends message, OpenRouter decides tool usage."""
    try:
        # Define tools for OpenRouter function calling
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "getWeather",
                    "description": "Get current weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name"
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "getNews",
                    "description": "Get latest news for a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "News topic"
                            }
                        },
                        "required": ["topic"]
                    }
                }
            }
        ]

        # OpenRouter API call
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-4o-mini",  # Using OpenAI model via OpenRouter
            "messages": [
                {"role": "user", "content": req.message}
            ],
            "tools": tools,
            "tool_choice": "auto"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            result = response.json()
            
            # Check if there are tool calls
            if "choices" in result and result["choices"]:
                message = result["choices"][0]["message"]
                
                if "tool_calls" in message and message["tool_calls"]:
                    # Process tool calls
                    tool_call = message["tool_calls"][0]
                    tool_name = tool_call["function"]["name"]
                    
                    import json
                    args = json.loads(tool_call["function"]["arguments"])
                    
                    # Execute the tool function
                    if tool_name in tool_functions:
                        tool_result = await tool_functions[tool_name](**args)
                        
                        # Send result back to OpenRouter for final response
                        follow_up_payload = {
                            "model": "openai/gpt-4o-mini",
                            "messages": [
                                {"role": "user", "content": req.message},
                                {"role": "assistant", "content": "", "tool_calls": message["tool_calls"]},
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call["id"],
                                    "content": json.dumps(tool_result)
                                }
                            ]
                        }
                        
                        follow_up_response = await client.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=follow_up_payload,
                            timeout=30.0
                        )
                        
                        follow_up_result = follow_up_response.json()
                        
                        return {
                            "answer": follow_up_result["choices"][0]["message"]["content"],
                            "tool_result": tool_result
                        }
                    else:
                        return {"error": f"Tool '{tool_name}' not found"}
                
                # No tool calls, return direct response
                return {"answer": message["content"]}
            else:
                return {"error": "No response from OpenRouter"}
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "error": f"Chat processing failed: {str(e)}", 
            "details": error_details
        }

# ======================
# Health Check Endpoint
# ======================

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "message": "MCP Server is running"
    }

@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "tools": list(tool_functions.keys()),
        "openrouter_configured": bool(OPENROUTER_KEY),
        "newsdata_configured": bool(NEWSDATA_KEY)
    }

# ======================
# Run Server
# ======================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
