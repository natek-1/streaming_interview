from . import weather

def test_replace_me():
    assert [
        {"type": "snapshot", "asOf": 1672531200000,
         "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 37.1}}}
    ] == list(weather.process_events([
        {"type": "sample",
         "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "snapshot"}
    ]))
    assert [
        {"type": "snapshot", "asOf": 1672531260000,
         "stations": {"Foster Weather Station": {"high": 45.2, "low": 32.1}}}
    ] == list(weather.process_events([
        {"type": "sample", "stationName":
            "Foster Weather Station", "timestamp": 1672531200000,
            "temperature": 37.1},
        {"type": "sample",
         "stationName": "Foster Weather Station",
         "timestamp": 1672531230000, "temperature": 32.1},
        {"type": "sample",
         "stationName": "Foster Weather Station",
         "timestamp": 1672531260000, "temperature": 45.2},
        {"type": "control", "command": "snapshot"}
    ]))
    assert [
        {"type": "snapshot", "asOf": 1672531230000, "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 37.1},
            "Oak Street Beach Station": {"high": 42.0, "low": 42.0}
        }}
    ] == list(weather.process_events([
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "sample", "stationName": "Oak Street Beach Station",
         "timestamp": 1672531230000, "temperature": 42.0},
        {"type": "control", "command": "snapshot"}
    ]))
    assert [
        {"type": "reset", "asOf": 1672531200000}
    ] == list(weather.process_events([
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "reset"}
    ]))
    assert [
        {"type": "reset", "asOf": 1672531200000}
    ] == list(weather.process_events([
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "reset"},
        {"type": "control", "command": "snapshot"}
    ]))
    assert [
        {"type": "reset", "asOf": 1672531200000},
        {"type": "snapshot", "asOf": 1672531300000,
         "stations": {"New Station": {"high": 50.0, "low": 50.0}}}
    ] == list(weather.process_events([
        {"type": "sample", "stationName":
            "Foster Weather Station", "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "reset"},
        {"type": "sample", "stationName": "New Station",
         "timestamp": 1672531300000, "temperature": 50.0},
        {"type": "control", "command": "snapshot"}
    ]))
    assert not list(weather.process_events([
        {"type": "control", "command": "snapshot"}
    ]))
    assert [
        {"type": "snapshot", "asOf": 1672531230000, "stations": {
            "Station A": {"high": 40.0, "low": 35.0},
            "Station B": {"high": 38.0, "low": 38.0}
        }},
        {"type": "reset", "asOf": 1672531230000},
        {"type": "snapshot", "asOf": 1672531300000, "stations": {
            "Station C": {"high": 60.0, "low": 55.0}
        }}
    ] == list(weather.process_events([
        {"type": "sample", "stationName": "Station A",
         "timestamp": 1672531200000, "temperature": 35.0},
        {"type": "sample", "stationName": "Station A",
         "timestamp": 1672531210000, "temperature": 40.0},
        {"type": "sample", "stationName": "Station B",
         "timestamp": 1672531230000, "temperature": 38.0},
        {"type": "control", "command": "snapshot"},
        {"type": "control", "command": "reset"},
        {"type": "sample", "stationName": "Station C",
         "timestamp": 1672531280000, "temperature": 55.0},
        {"type": "sample", "stationName": "Station C",
         "timestamp": 1672531300000, "temperature": 60.0},
        {"type": "control", "command": "snapshot"}
    ]))
