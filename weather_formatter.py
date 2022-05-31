from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    return f"{weather.city}, temperature {weather.temperature}°C, " \
           f"{weather.weather_type.value}\n" \
           f"Sunrise: {weather.sunrise.strftime('%H:%M')}\n" \
           f"Sunset: {weather.sunset.strftime('%H:%M')}\n"


if __name__ == "__main__":
    from datetime import datetime
    from weather_api_service import WeatherType

    print(format_weather(Weather(
        temperature=20,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.now(),
        sunset=datetime.now(),
        city="Krasnodar"
    )))
