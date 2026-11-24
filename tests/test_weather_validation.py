import pytest
from src.transform.weather_validation import validate_weather

def test_validate_weather_valid_record():
    record={
        "location": "Toronto",
        "date": "2026-11-24",
        "temperature_max": 15,
        "temperature_min": 8,
        "precipitation": 0,
        "wind_speed_max": 20
    }
    assert validate_weather(record)==True

def test_validate_weather_invalid_record():
    record={
            "location": "Toronto",
            "date": "2026-11-24",
            "temperature_max": 5,
            "temperature_min": 10,
            "precipitation": 0,
            "wind_speed_max": 20
        }
    assert validate_weather(record)==False

def test_validate_weather_negative_precipitation():
    record={
                "location": "Toronto",
                "date": "2026-11-24",
                "temperature_max": 15,
                "temperature_min": 8,
                "precipitation": -10,
                "wind_speed_max": 20
        }
    assert validate_weather(record) ==False

def test_validate_weather_negative_wind_speed():
    record={
            "location": "Toronto",
            "date": "2026-11-24",
            "temperature_max": 15,
            "temperature_min": 8,
            "precipitation": 0,
            "wind_speed_max": -10
        }
    assert validate_weather(record) ==False

@pytest.mark.parametrize(
    "temperature_max, temperature_min, precipitation, wind_speed_max, expected",
    [
        (5, 10, 0, 20, False),
        (15,8,-10,20,False),
        (15,8,0,-10,False)
    ]
)
def test_parameterisation(temperature_max, temperature_min, precipitation, wind_speed_max, expected):
    weather_record={
        "location":"test",
        "date": "2026-11-24",
        "temperature_max": temperature_max,
        "temperature_min": temperature_min,
        "precipitation": precipitation,
        "wind_speed_max": wind_speed_max
    }

    assert validate_weather(weather_record)==expected