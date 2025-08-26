from typing import Any, Iterable, Generator
class Event:
    def __init__(self):
        self.recent_timestamp = 0 # default value for the timestamp
        self.station_temp = {} # station_name: (min_temp, max_temp)
    def insert_event(self, station_name, timestamp, temperature) -> None:
        # update the timestamp for the station
        # we know the timestamp is increasing.
        # Therefore as the stream continues the most recent one is the one provided
        self.recent_timestamp = timestamp
        # update the min and max temperature for a station:
        if self.station_temp.get(station_name, None) is None:
        # station has no temperature uses current one as min and max
            self.station_temp[station_name] = (temperature, temperature)
        else:
            min_temp, max_temp = self.station_temp[station_name]
            min_temp = min(min_temp, temperature)
            max_temp = max(max_temp, temperature)
            self.station_temp[station_name] = (min_temp, max_temp)
    def get_info(self) -> dict[str, Any]:
        result = {"type": "snapshot", "stations": {}, 'asOf': self.recent_timestamp}
        for station, (min_temp, max_temp) in self.station_temp.items():
            result['stations'][station] = {"high": max_temp, "low": min_temp}
        return result
    def reset(self) -> dict[str, Any]:
        result = {"type": "reset", "asOf": self.recent_timestamp}
        self.recent_timestamp = 0
        self.station_temp = {}
        return result

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    event = Event()
    for line in events:
        if not line.get("type"):
            raise ValueError("An event did not have the 'type' key in it's json")
        if line['type'] == "sample":
            event.insert_event(line['stationName'], line['timestamp'], line['temperature'])
        elif (line["type"] == "control" and line['command'] == "snapshot" and
            event.recent_timestamp == 0 and not event.station_temp):
            continue
        elif line["type"] == "control" and line['command'] == "snapshot":
            yield event.get_info()
        elif (line["type"] == "control" and line['command'] == "reset"
            and event.recent_timestamp == 0 and not event.station_temp):
            continue
        elif line["type"] == "control" and line['command'] == "reset":
            yield event.reset()
        else:
            raise ValueError("An event did not have the correct type or command")
