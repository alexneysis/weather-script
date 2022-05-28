from typing import NamedTuple

import requests

from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    response = _get_info_from_ipinfo()
    coordinates = _parse_coordinates_from_ipinfo(response)
    return coordinates


def _get_info_from_ipinfo() -> dict:
    url = "https://ipinfo.io"
    response = requests.get(url)
    if not response.ok:
        raise CantGetCoordinates("Can't get GPS coordinates from site")

    return response.json()


def _parse_coordinates_from_ipinfo(ipinfo_response: dict) -> Coordinates:
    try:
        lat, lon = map(_parse_coordinate, ipinfo_response["loc"].split(","))
        return Coordinates(latitude=lat, longitude=lon)
    except KeyError:
        raise CantGetCoordinates("Can't parse GPS coordinates")


def _parse_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates("Can't parse value of coordinates")
