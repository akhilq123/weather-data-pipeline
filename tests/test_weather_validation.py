import pytest
from src.transform.weather_validation import validate_weather
from src.transform.weather_validation import validate_date

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



@pytest.mark.parametrize(
    "temperature_max, temperature_min, precipitation, wind_speed_max, expected",
    [
        (5, 10, 0, 20, False),
        (15,8,-10,20,False),
        (15,8,0,-10,False)
    ]
)
def test_validate_weather_invalid_numeric_values(temperature_max, temperature_min, precipitation, wind_speed_max, expected):
    weather_record={
        "location":"test",
        "date": "2026-11-24",
        "temperature_max": temperature_max,
        "temperature_min": temperature_min,
        "precipitation": precipitation,
        "wind_speed_max": wind_speed_max
    }

    assert validate_weather(weather_record)==expected

def test_validate_weather_empty_location():
     record={
                "location": "",
                "date": "2026-11-24",
                "temperature_max": 15,
                "temperature_min": 8,
                "precipitation": 0,
                "wind_speed_max": 10
     }
     assert validate_weather(record)==False

def test_validate_weather_missing_date():
    record={
                    "location": "Toronto",
                    "date": None,
                    "temperature_max": 15,
                    "temperature_min": 8,
                    "precipitation": 0,
                    "wind_speed_max": 10
         }
    assert validate_weather(record)==False

def test_validate_weather_whitespace_location():
    record={
                        "location": " ",
                        "date": "2026-11-24",
                        "temperature_max": 15,
                        "temperature_min": 8,
                        "precipitation": 0,
                        "wind_speed_max": 10
    }
    assert validate_weather(record)==False

def test_validate_weather_missing_location_key():
    record={
                            "date": "2026-11-24",
                            "temperature_max": 15,
                            "temperature_min": 8,
                            "precipitation": 0,
                            "wind_speed_max": 10
        }
    assert validate_weather(record)==False

def test_validate_weather_missing_temperature_max_key():
    record={
                            "location": "Toronto",
                            "date": "2026-11-24",
                            "temperature_min": 8,
                            "precipitation": 0,
                            "wind_speed_max": 10
        }
    assert validate_weather(record)==False

def test_validate_weather_temperature_max_string():
    record = {
        "location": "Toronto",
        "date": "2026-11-25",
        "temperature_max": "15",
        "temperature_min": 8,
        "precipitation": 0,
        "wind_speed_max": 10
    }

    assert validate_weather(record) == False

def test_validate_weather_precipitation_string():
    record = {
        "location": "Toronot",
        "date": "2026-11-25",
        "temperature_max": 15,
        "temperature_min": 8,
        "precipitation": "5",
        "wind_speed_max": 10
    }

    assert validate_weather(record) == False


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2026-11-25", True),
        ("25-11-2026", False),
        ("2026-13-25", False),
        ("2026/11/25", False),
        (None, False)
    ]
)
def test_validate_date(date,expected):
    assert validate_date(date)==expected