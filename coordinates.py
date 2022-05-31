import json
import ssl
from json import JSONDecodeError
from typing import NamedTuple, Literal
from urllib import request
from urllib.error import URLError

from config import IPINFO_URL
from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    response = _get_ipinfo_response()
    coordinates = _parse_ipinfo_response(response)
    return coordinates


def _get_ipinfo_response() -> dict:
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        return request.urlopen(IPINFO_URL).read()
    except URLError:
        raise CantGetCoordinates


def _parse_ipinfo_response(ipinfo_response: dict) -> Coordinates:
    try:
        ipinfo_dict = json.loads(ipinfo_response)
        lat, lon = map(_parse_coordinate, _parse_coordinates(ipinfo_dict).split(","))
        return Coordinates(latitude=lat, longitude=lon)
    except KeyError:
        raise CantGetCoordinates("Can't parse GPS coordinates")
    except JSONDecodeError:
        raise CantGetCoordinates


def _parse_coordinates(ipinfo_dict: [Literal["loc"], str]) -> str:
    try:
        return ipinfo_dict["loc"]
    except KeyError:
        raise CantGetCoordinates


def _parse_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates("Can't parse value of coordinates")
