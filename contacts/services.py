import requests
from django.core.cache import cache

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def get_city_coordinates(city_name: str):
    normalized_city = (city_name or "").strip()
    if not normalized_city:
        return None

    cache_key = f"city_coords:{normalized_city.lower()}"
    cached_value = cache.get(cache_key)
    if cached_value:
        return cached_value

    response = requests.get(
        NOMINATIM_URL,
        params={"q": normalized_city, "format": "json", "limit": 1},
        headers={"User-Agent": "contacts-django-app/1.0"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if not data:
        cache.set(cache_key, None, 60 * 60 * 24)
        return None

    coords = {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    cache.set(cache_key, coords, 60 * 60 * 24 * 30)
    return coords


def get_current_weather_for_city(city_name: str):
    normalized_city = (city_name or "").strip()
    if not normalized_city:
        return None

    cache_key = f"weather:{normalized_city.lower()}"
    cached_value = cache.get(cache_key)
    if cached_value:
        return cached_value

    coords = get_city_coordinates(normalized_city)
    if not coords:
        cache.set(cache_key, None, 60 * 10)
        return None

    response = requests.get(
        OPEN_METEO_URL,
        params={
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current_weather": "true",
            "hourly": "relativehumidity_2m",
            "forecast_days": 1,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    current_weather = data.get("current_weather") or {}
    temperature = current_weather.get("temperature")
    windspeed = current_weather.get("windspeed")

    humidity = None
    hourly = data.get("hourly") or {}
    humidity_list = hourly.get("relativehumidity_2m") or []
    if humidity_list:
        humidity = humidity_list[0]

    weather_payload = {
        "temperature": temperature,
        "humidity": humidity,
        "windspeed": windspeed,
    }
    cache.set(cache_key, weather_payload, 60 * 10)
    return weather_payload
