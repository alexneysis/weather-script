from __future__ import annotations

import json
import ssl
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from typing import NamedTuple, Literal
from urllib import request
from urllib.error import URLError

from config import OPENWEATHER_URL
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude
    )
    return _parse_openweather_response(openweather_response)


def _get_openweather_response(longitude: float, latitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context

    url = OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)

    try:
        return request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
        return Weather(
            temperature=_parse_temperature(openweather_dict),
            weather_type=_parse_weather_type(openweather_dict),
            sunrise=_parse_sun_time(openweather_dict, "sunrise"),
            sunset=_parse_sun_time(openweather_dict, "sunset"),
            city=_parse_city(openweather_dict),
        )
    except JSONDecodeError:
        raise ApiServiceError


def _parse_temperature(openweather_dict: dict) -> int:
    try:
        return round(openweather_dict["main"]["temp"])
    except KeyError:
        raise ApiServiceError


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError

    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "804": WeatherType.CLOUDS,
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(openweather_dict: dict,
                    time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    try:
        return datetime.fromtimestamp(openweather_dict["sys"][time])
    except KeyError:
        raise ApiServiceError


def _parse_city(openweather_dict: dict) -> str:
    try:
        return openweather_dict["name"]
    except KeyError:
        raise ApiServiceError


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))
