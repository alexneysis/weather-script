from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    return Coordinates(latitude=-10.0, longitude=-1.0)
