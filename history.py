import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict, List

from weather_api_service import Weather
from weather_formatter import format_weather


class WeatherStorage:
    """ Interface for any storage saving weather """

    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage(WeatherStorage):
    """ Store weather in plain text file """

    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now_datetime = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now_datetime}\n{formatted_weather}")


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JsonFileWeatherStorage(WeatherStorage):
    def __init__(self, json_file: Path):
        self._json_file = json_file
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history = self._read_history()
        history.append({
            "date": str(datetime.now()),
            "weather": format_weather(weather)
        })
        self._write(history)

    def _init_storage(self) -> None:
        if not self._json_file.exists():
            self._json_file.write_text("[]")

    def _read_history(self) -> List[HistoryRecord]:
        with open(self._json_file, "r") as f:
            return json.load(f)

    def _write(self, history: List[HistoryRecord]) -> None:
        with open(self._json_file, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """ Save weather in the storage """
    storage.save(weather)
